"""
OmniMCP Command Line Interface

Generate MCP servers from OpenAPI specs.

Usage:
    omnimcp generate <provider> [--output=<dir>] [--review] [--test]
    omnimcp generate-all [--tier=<tier>] [--output=<dir>]
    omnimcp list [--search=<query>]
    omnimcp info <provider>
    omnimcp test <provider> [--live]
"""

from __future__ import annotations

import asyncio
import functools
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from omnimcp.generator import OpenAPIParser, MCPConverter, MCPCodeGenerator
from omnimcp.specs import SpecFetcher, SpecRegistry
from omnimcp.specs.registry import ProviderTier
from omnimcp.auth import AuthRegistry

console = Console()


def coro(f):
    """Decorator to run async functions with asyncio.run()."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@click.group()
@click.version_option(version="0.1.0", prog_name="omnimcp")
def cli():
    """OmniMCP - Universal MCP Server Generator

    Generate MCP servers from any OpenAPI specification.
    """
    pass


@cli.command()
@click.argument("provider")
@click.option("--output", "-o", default="./output", help="Output directory")
@click.option("--review", is_flag=True, help="Use LLM to review and enhance")
@click.option("--test", "run_test", is_flag=True, help="Run tests after generation")
@click.option("--auth-type", type=click.Choice(["oauth2", "api_key", "bearer", "basic"]),
              help="Override auth type")
@coro
async def generate(provider: str, output: str, review: bool, run_test: bool, auth_type: str | None):
    """Generate MCP server for a provider.

    Example:
        omnimcp generate slack --output ./my-servers
    """
    output_dir = Path(output)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Fetch spec
        task = progress.add_task(f"Fetching OpenAPI spec for {provider}...", total=None)
        fetcher = SpecFetcher()
        try:
            spec = await fetcher.fetch_spec(provider)
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            return
        progress.update(task, description=f"[green]✓[/green] Fetched spec for {provider}")

        # Parse spec
        task = progress.add_task("Parsing OpenAPI specification...", total=None)
        parser = OpenAPIParser()
        parsed = parser.parse(spec)
        progress.update(task, description=f"[green]✓[/green] Parsed {len(parsed.endpoints)} endpoints")

        # Convert to MCP tools
        task = progress.add_task("Converting to MCP tools...", total=None)
        converter = MCPConverter()
        tools = converter.convert(parsed)
        # Filter deprecated
        tools = converter.filter_deprecated(tools)
        progress.update(task, description=f"[green]✓[/green] Generated {len(tools)} MCP tools")

        # Get auth config
        auth_registry = AuthRegistry()
        auth_config = auth_registry.get_config(provider)
        detected_auth = auth_type
        if not detected_auth and auth_config:
            detected_auth = auth_config.auth_type.value

        # Determine environment variable name - prefer auth config if available
        env_var = None
        if auth_config:
            # Use the actual env var from auth config
            if auth_config.env_vars.access_token:
                env_var = auth_config.env_vars.access_token
            elif auth_config.env_vars.api_key:
                env_var = auth_config.env_vars.api_key
        
        # Fallback to generated name if no auth config
        if not env_var:
            if detected_auth == "oauth2":
                env_var = f"{provider.upper()}_ACCESS_TOKEN"
            elif detected_auth == "api_key":
                env_var = f"{provider.upper()}_API_KEY"
            elif detected_auth == "bearer":
                env_var = f"{provider.upper()}_TOKEN"
            else:
                env_var = f"{provider.upper()}_API_KEY"

        # Generate code
        task = progress.add_task("Generating Python code...", total=None)
        generator = MCPCodeGenerator()
        server = generator.generate(
            tools=tools,
            server_name=provider,
            base_url=parsed.base_url,
            version="0.1.0",
            description=parsed.description,
            auth_type=detected_auth,
            env_var_name=env_var,
        )

        # Write files
        server_dir = output_dir / provider
        server.write(server_dir)
        progress.update(task, description=f"[green]✓[/green] Generated server at {server_dir}")

    # Summary
    console.print()
    console.print(Panel(
        f"[bold green]Successfully generated MCP server for {provider}![/bold green]\n\n"
        f"Location: {server_dir}\n"
        f"Tools: {len(tools)}\n"
        f"Auth: {detected_auth or 'none'}\n"
        f"[bold yellow]Required env var: {env_var}[/bold yellow]\n\n"
        f"To run:\n"
        f"  cd {server_dir}\n"
        f"  pip install -e .\n"
        f"  export {env_var}=your_token\n"
        f"  python -m omnimcp_{provider}",
        title="Generation Complete",
    ))


@cli.command("generate-all")
@click.option("--tier", type=click.Choice(["tier1", "tier2", "all"]), default="tier1",
              help="Provider tier to generate")
@click.option("--output", "-o", default="./output", help="Output directory")
@coro
async def generate_all(tier: str, output: str):
    """Generate servers for multiple providers.

    Example:
        omnimcp generate-all --tier=tier1 --output ./servers
    """
    registry = SpecRegistry()

    if tier == "tier1":
        providers = registry.list_by_tier(ProviderTier.TIER1)
    elif tier == "tier2":
        providers = registry.list_by_tier(ProviderTier.TIER2)
    else:
        providers = registry.list_enabled()

    console.print(f"[bold]Generating {len(providers)} servers...[/bold]\n")

    successful = []
    failed = []

    for entry in providers:
        try:
            console.print(f"  Generating {entry.display_name}...", end=" ")
            # Run generate for each provider
            await _generate_single(entry.name, Path(output))
            console.print("[green]✓[/green]")
            successful.append(entry.name)
        except Exception as e:
            console.print(f"[red]✗ {e}[/red]")
            failed.append((entry.name, str(e)))

    # Summary
    console.print()
    console.print(f"[bold]Results:[/bold]")
    console.print(f"  [green]✓ Successful: {len(successful)}[/green]")
    if failed:
        console.print(f"  [red]✗ Failed: {len(failed)}[/red]")
        for name, error in failed:
            console.print(f"    - {name}: {error}")


async def _generate_single(provider: str, output_dir: Path) -> None:
    """Generate a single server (internal helper)."""
    fetcher = SpecFetcher()
    spec = await fetcher.fetch_spec(provider)

    parser = OpenAPIParser()
    parsed = parser.parse(spec)

    converter = MCPConverter()
    tools = converter.convert(parsed)
    tools = converter.filter_deprecated(tools)

    auth_registry = AuthRegistry()
    auth_config = auth_registry.get_config(provider)
    auth_type = auth_config.auth_type.value if auth_config else None

    generator = MCPCodeGenerator()
    server = generator.generate(
        tools=tools,
        server_name=provider,
        base_url=parsed.base_url,
        auth_type=auth_type,
    )

    server.write(output_dir / provider)


@cli.command("list")
@click.option("--search", "-s", help="Search query")
@click.option("--tier", type=click.Choice(["tier1", "tier2", "tier3", "all"]), default="all",
              help="Filter by tier")
@coro
async def list_providers(search: str | None, tier: str):
    """List available providers.

    Example:
        omnimcp list --search email
    """
    if search:
        # Search APIs.guru
        fetcher = SpecFetcher()
        providers = await fetcher.search(search)

        if not providers:
            console.print(f"[yellow]No providers found matching '{search}'[/yellow]")
            return

        table = Table(title=f"Search Results for '{search}'")
        table.add_column("Provider", style="cyan")
        table.add_column("Title")
        table.add_column("Description")

        for p in providers[:20]:  # Limit to 20 results
            desc = p.description[:50] + "..." if len(p.description) > 50 else p.description
            table.add_row(p.name, p.title, desc)

        console.print(table)
    else:
        # List from registry
        registry = SpecRegistry()

        if tier == "all":
            providers = registry.list_enabled()
        else:
            providers = registry.list_by_tier(ProviderTier(tier))

        table = Table(title="Available Providers")
        table.add_column("Provider", style="cyan")
        table.add_column("Name")
        table.add_column("Tier", style="green")
        table.add_column("Auth")

        for p in providers:
            table.add_row(p.name, p.display_name, p.tier.value, p.auth_type)

        console.print(table)
        console.print(f"\n[dim]Total: {len(providers)} providers[/dim]")
        console.print("[dim]Use 'omnimcp list --search <query>' to search APIs.guru[/dim]")


@cli.command()
@click.argument("provider")
@coro
async def info(provider: str):
    """Show provider info and auth requirements.

    Example:
        omnimcp info slack
    """
    # Check registry first
    registry = SpecRegistry()
    entry = registry.get(provider)

    # Get auth config
    auth_registry = AuthRegistry()
    auth_config = auth_registry.get_config(provider)

    # Get spec info
    fetcher = SpecFetcher()
    provider_info = await fetcher.get_provider_info(provider)

    if not entry and not provider_info:
        console.print(f"[red]Provider '{provider}' not found[/red]")
        console.print("[dim]Try 'omnimcp list --search <query>' to find it[/dim]")
        return

    # Build info panel
    lines = []

    if entry:
        lines.append(f"[bold]Name:[/bold] {entry.display_name}")
        lines.append(f"[bold]Tier:[/bold] {entry.tier.value}")
        if entry.base_url:
            lines.append(f"[bold]Base URL:[/bold] {entry.base_url}")
    elif provider_info:
        lines.append(f"[bold]Name:[/bold] {provider_info.display_name}")
        if provider_info.description:
            lines.append(f"[bold]Description:[/bold] {provider_info.description[:200]}")

    if auth_config:
        lines.append("")
        lines.append("[bold cyan]Authentication:[/bold cyan]")
        lines.append(f"  Type: {auth_config.auth_type.value}")
        if auth_config.docs_url:
            lines.append(f"  Docs: {auth_config.docs_url}")
        if auth_config.env_vars.api_key:
            lines.append(f"  Env var: {auth_config.env_vars.api_key}")
        elif auth_config.env_vars.access_token:
            lines.append(f"  Env var: {auth_config.env_vars.access_token}")

        if auth_config.quirks:
            lines.append("")
            lines.append("[bold yellow]Notes:[/bold yellow]")
            for quirk in auth_config.quirks:
                lines.append(f"  - {quirk}")

    console.print(Panel("\n".join(lines), title=f"Provider: {provider}"))


@cli.command()
@click.argument("provider")
@click.option("--live", is_flag=True, help="Run tests against live API")
def test(provider: str, live: bool):
    """Test generated server.

    Example:
        omnimcp test slack
    """
    console.print(f"[yellow]Testing not yet implemented[/yellow]")
    console.print(f"[dim]Would test server for {provider}[/dim]")
    if live:
        console.print("[dim]Would run live API tests[/dim]")


@cli.command()
@click.argument("provider")
@click.option("--pypi", is_flag=True, help="Publish to PyPI")
@click.option("--npm", is_flag=True, help="Publish to npm")
def publish(provider: str, pypi: bool, npm: bool):
    """Publish server to package registries.

    Example:
        omnimcp publish slack --pypi
    """
    console.print(f"[yellow]Publishing not yet implemented[/yellow]")
    if pypi:
        console.print(f"[dim]Would publish omnimcp-{provider} to PyPI[/dim]")
    if npm:
        console.print(f"[dim]Would publish @omnimcp/{provider} to npm[/dim]")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
