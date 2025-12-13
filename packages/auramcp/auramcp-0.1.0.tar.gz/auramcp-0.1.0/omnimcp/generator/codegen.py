"""
MCP Code Generator - Generate Python MCP server code from tool definitions.

Creates complete, runnable MCP server packages using FastMCP.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from omnimcp.generator.converter import MCPTool, MCPToolParameter, ParameterLocation
from omnimcp.generator.parser import HTTPMethod


@dataclass
class GeneratedFile:
    """A generated file."""
    path: str  # Relative path within the package
    content: str


@dataclass
class GeneratedServer:
    """Complete generated MCP server package."""
    name: str
    version: str = "0.1.0"
    files: list[GeneratedFile] = field(default_factory=list)

    def write(self, output_dir: Path) -> None:
        """Write all files to the output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        for gen_file in self.files:
            file_path = output_dir / gen_file.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(gen_file.content)

    def get_file(self, path: str) -> GeneratedFile | None:
        """Get a generated file by path."""
        for f in self.files:
            if f.path == path:
                return f
        return None


class MCPCodeGenerator:
    """Generate Python MCP server code."""

    # Python type mapping from JSON Schema types
    TYPE_MAP = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "list",
        "object": "dict",
        "null": "None",
    }

    def __init__(
        self,
        include_types: bool = True,
        include_examples: bool = True,
        max_tools_per_file: int = 50,
    ):
        """
        Initialize the code generator.

        Args:
            include_types: Generate types.py with Pydantic models
            include_examples: Include example values in docstrings
            max_tools_per_file: Split tools across files if exceeded
        """
        self.include_types = include_types
        self.include_examples = include_examples
        self.max_tools_per_file = max_tools_per_file

    def generate(
        self,
        tools: list[MCPTool],
        server_name: str,
        base_url: str,
        version: str = "0.1.0",
        description: str = "",
        auth_type: str | None = None,
        env_var_name: str | None = None,
    ) -> GeneratedServer:
        """
        Generate complete MCP server package.

        Args:
            tools: List of MCP tools to generate
            server_name: Name of the server (e.g., "slack")
            base_url: Base URL for API requests
            version: Package version
            description: Package description
            auth_type: Type of auth (oauth2, api_key, bearer, basic)
            env_var_name: Override for environment variable name (e.g., SLACK_BOT_TOKEN)

        Returns:
            GeneratedServer with all package files
        """
        package_name = f"omnimcp_{server_name}"

        server = GeneratedServer(
            name=server_name,
            version=version,
        )

        # Generate package files
        server.files.append(self._generate_pyproject(
            package_name, server_name, version, description
        ))
        server.files.append(self._generate_readme(
            server_name, description, auth_type, env_var_name
        ))
        server.files.append(self._generate_init(package_name))
        server.files.append(self._generate_main(package_name))
        server.files.append(self._generate_client(
            package_name, base_url, auth_type, env_var_name
        ))
        server.files.append(self._generate_server(
            package_name, server_name, tools, auth_type
        ))

        if self.include_types:
            server.files.append(self._generate_types(package_name, tools))


        return server

    def _generate_pyproject(
        self,
        package_name: str,
        server_name: str,
        version: str,
        description: str,
    ) -> GeneratedFile:
        """Generate pyproject.toml."""
        content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{package_name}"
version = "{version}"
description = "{description or f'OmniMCP server for {server_name.title()} API'}"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
authors = [
    {{ name = "OmniMCP Team" }}
]
keywords = ["mcp", "{server_name}", "api", "llm", "claude"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "httpx>=0.25.0",
    "mcp>=1.0.0",
    "pydantic>=2.0.0",
]

[project.scripts]
{package_name} = "{package_name}.server:main"

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]
'''
        return GeneratedFile(path="pyproject.toml", content=content)

    def _generate_readme(
        self,
        server_name: str,
        description: str,
        auth_type: str | None,
        env_var_override: str | None = None,
    ) -> GeneratedFile:
        """Generate README.md."""
        title = server_name.title()

        # Use override if provided, otherwise determine based on auth type
        if env_var_override:
            env_var_name = env_var_override
        elif auth_type == "oauth2":
            env_var_name = f"{server_name.upper()}_ACCESS_TOKEN"
        elif auth_type == "api_key":
            env_var_name = f"{server_name.upper()}_API_KEY"
        elif auth_type == "bearer":
            env_var_name = f"{server_name.upper()}_TOKEN"
        else:
            env_var_name = f"{server_name.upper()}_API_KEY"

        # Generate auth section based on type
        if auth_type == "oauth2":
            auth_section = f'''## Authentication

This server uses OAuth2 authentication. Set the following environment variable:

```bash
export {env_var_name}=your_access_token
```

To obtain an access token, follow the OAuth2 flow in the {title} API documentation.
'''
        elif auth_type == "api_key":
            auth_section = f'''## Authentication

This server uses API key authentication. Set the following environment variable:

```bash
export {env_var_name}=your_api_key
```
'''
        elif auth_type == "bearer":
            auth_section = f'''## Authentication

This server uses Bearer token authentication. Set the following environment variable:

```bash
export {env_var_name}=your_token
```
'''
        else:
            auth_section = ""

        content = f'''# OmniMCP {title} Server

{description or f'MCP server for the {title} API, auto-generated by OmniMCP.'}

## Installation

```bash
pip install omnimcp-{server_name}
```

{auth_section}

## Usage

### As a standalone server

```bash
python -m omnimcp_{server_name}
```

### With Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{{
  "mcpServers": {{
    "{server_name}": {{
      "command": "python",
      "args": ["-m", "omnimcp_{server_name}"],
      "env": {{
        "{env_var_name}": "your_token_here"
      }}
    }}
  }}
}}
```

### Programmatic usage

```python
from omnimcp_{server_name} import mcp

# Run the server
mcp.run()
```

## Generated

This server was auto-generated by [OmniMCP](https://github.com/omnimcp/omnimcp) on {datetime.now().strftime("%Y-%m-%d")}.
'''
        return GeneratedFile(path="README.md", content=content)

    def _generate_init(self, package_name: str) -> GeneratedFile:
        """Generate __init__.py."""
        content = f'''"""
{package_name} - OmniMCP Server

Auto-generated MCP server.
"""

from {package_name}.server import mcp

__all__ = ["mcp"]
'''
        return GeneratedFile(
            path=f"src/{package_name}/__init__.py",
            content=content
        )

    def _generate_main(self, package_name: str) -> GeneratedFile:
        """Generate __main__.py for python -m support."""
        content = f'''"""Entry point for python -m {package_name}."""

from {package_name}.server import main

if __name__ == "__main__":
    main()
'''
        return GeneratedFile(
            path=f"src/{package_name}/__main__.py",
            content=content
        )

    def _generate_client(
        self,
        package_name: str,
        base_url: str,
        auth_type: str | None,
        env_var_override: str | None = None,
    ) -> GeneratedFile:
        """Generate client.py with HTTP client configuration."""
        server_name = package_name.replace("omnimcp_", "")

        if auth_type == "bearer" or auth_type == "oauth2":
            # Use override env var if provided, otherwise generate default
            if env_var_override:
                token_var = env_var_override
            elif auth_type == "oauth2":
                token_var = f"{server_name.upper()}_ACCESS_TOKEN"
            else:
                token_var = f"{server_name.upper()}_TOKEN"
            auth_code = f'''
def get_auth_headers() -> dict[str, str]:
    """Get authentication headers."""
    token = os.environ.get("{token_var}")
    if not token:
        raise ValueError("{token_var} environment variable required")
    return {{"Authorization": f"Bearer {{token}}"}}
'''
        elif auth_type == "api_key":
            # Use override env var if provided
            api_key_var = env_var_override or f"{server_name.upper()}_API_KEY"
            auth_code = f'''
def get_auth_headers() -> dict[str, str]:
    """Get authentication headers."""
    api_key = os.environ.get("{api_key_var}")
    if not api_key:
        raise ValueError("{api_key_var} environment variable required")
    return {{"X-API-Key": api_key}}
'''
        else:
            auth_code = '''
def get_auth_headers() -> dict[str, str]:
    """Get authentication headers."""
    return {}
'''

        content = f'''"""
HTTP client configuration for {package_name}.

Production-ready with:
- Automatic retries with exponential backoff
- Rate limit handling
- Proper error responses
- Support for both JSON and form-urlencoded
"""

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import httpx

BASE_URL = "{base_url}"

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds
RATE_LIMIT_RETRY_DELAY = 5.0  # seconds
{auth_code}

class APIError(Exception):
    """API request error with details."""
    def __init__(self, message: str, status_code: int | None = None, response_data: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {{}}


@asynccontextmanager
async def get_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Get configured HTTP client with authentication."""
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers=get_auth_headers(),
        timeout=30.0,
    ) as client:
        yield client


async def make_request(
    method: str,
    path: str,
    params: dict | None = None,
    json_body: dict | None = None,
    form_data: dict | None = None,
    headers: dict | None = None,
    use_form: bool = True,
) -> dict[str, Any]:
    """
    Make an authenticated API request with retry logic.

    Args:
        method: HTTP method (GET, POST, etc.)
        path: API endpoint path
        params: Query parameters
        json_body: JSON request body (used if use_form=False)
        form_data: Form data (used if use_form=True, defaults to json_body)
        headers: Additional headers
        use_form: Use form-urlencoded instead of JSON (default True for compatibility)

    Returns:
        Response JSON data

    Raises:
        APIError: If the request fails after retries
    """
    last_error = None

    # Use form_data if provided, otherwise use json_body for form submission
    body_data = form_data if form_data is not None else json_body

    for attempt in range(MAX_RETRIES):
        try:
            async with get_client() as client:
                # Prepare request kwargs
                request_kwargs: dict[str, Any] = {{
                    "method": method,
                    "url": path,
                    "params": params,
                    "headers": headers,
                }}

                # Add body based on content type preference
                if body_data:
                    if use_form:
                        # Filter out None values for form data
                        clean_data = {{k: v for k, v in body_data.items() if v is not None}}
                        request_kwargs["data"] = clean_data
                    else:
                        request_kwargs["json"] = body_data

                response = await client.request(**request_kwargs)

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = float(response.headers.get("Retry-After", RATE_LIMIT_RETRY_DELAY))
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(retry_after)
                        continue

                # Handle server errors with retry
                if response.status_code >= 500:
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                        continue

                # Parse response
                if response.status_code == 204 or not response.content:
                    return {{"ok": True, "success": True}}

                try:
                    data = response.json()
                except Exception:
                    data = {{"raw_response": response.text}}

                # Check for API-level errors (many APIs return 200 with error in body)
                if isinstance(data, dict):
                    # Handle Slack-style errors
                    if data.get("ok") is False:
                        error_msg = data.get("error", "Unknown API error")
                        raise APIError(
                            f"API error: {{error_msg}}",
                            status_code=response.status_code,
                            response_data=data
                        )

                # Raise for HTTP errors
                if response.status_code >= 400:
                    error_msg = data.get("error", data.get("message", f"HTTP {{response.status_code}}"))
                    raise APIError(
                        f"Request failed: {{error_msg}}",
                        status_code=response.status_code,
                        response_data=data
                    )

                return data

        except httpx.TimeoutException as e:
            last_error = APIError(f"Request timeout: {{e}}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                continue

        except httpx.RequestError as e:
            last_error = APIError(f"Request error: {{e}}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                continue

        except APIError:
            raise

        except Exception as e:
            last_error = APIError(f"Unexpected error: {{e}}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                continue

    # All retries exhausted
    if last_error:
        raise last_error
    raise APIError("Request failed after all retries")
'''
        return GeneratedFile(
            path=f"src/{package_name}/client.py",
            content=content
        )

    def _generate_server(
        self,
        package_name: str,
        server_name: str,
        tools: list[MCPTool],
        auth_type: str | None,
    ) -> GeneratedFile:
        """Generate server.py with all MCP tools."""
        # Group tools by tag for organization
        tools_by_tag: dict[str, list[MCPTool]] = {}
        for tool in tools:
            tag = tool.tags[0] if tool.tags else "general"
            if tag not in tools_by_tag:
                tools_by_tag[tag] = []
            tools_by_tag[tag].append(tool)

        tool_functions = []
        for tag, tag_tools in sorted(tools_by_tag.items()):
            # Add section comment
            tool_functions.append(f"\n# {'=' * 60}")
            tool_functions.append(f"# {tag.title()} Tools")
            tool_functions.append(f"# {'=' * 60}\n")

            for tool in tag_tools:
                tool_functions.append(self._generate_tool_function(tool))

        tools_code = "\n".join(tool_functions)

        content = f'''"""
OmniMCP Server for {server_name.title()}

Auto-generated from OpenAPI specification.

Usage:
    python -m {package_name}
"""

from mcp.server.fastmcp import FastMCP

from {package_name}.client import make_request, APIError

# Initialize MCP server
mcp = FastMCP("{server_name}")

{tools_code}

def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
'''
        return GeneratedFile(
            path=f"src/{package_name}/server.py",
            content=content
        )

    def _generate_tool_function(self, tool: MCPTool) -> str:
        """Generate a single tool function."""
        # Build function signature
        params = self._build_function_params(tool)
        signature = f"async def {tool.name}({params}) -> dict:"

        # Build docstring
        docstring = self._build_docstring(tool)

        # Build function body
        body = self._build_function_body(tool)

        # Combine
        lines = [
            "@mcp.tool()",
            signature,
            docstring,
            body,
        ]

        return "\n".join(lines) + "\n"

    def _build_function_params(self, tool: MCPTool) -> str:
        """Build function parameter signature."""
        # Sort parameters: required first, then optional
        sorted_params = sorted(tool.parameters, key=lambda p: (not p.required, p.name))

        params = []
        for param in sorted_params:
            python_type = self.TYPE_MAP.get(param.type, "Any")

            if param.required:
                params.append(f"{param.name}: {python_type}")
            else:
                default = self._format_default(param.default, param.type)
                params.append(f"{param.name}: {python_type} = {default}")

        return ",\n    ".join(params) if params else ""

    def _format_default(self, default: Any, param_type: str) -> str:
        """Format default value for Python code."""
        if default is None:
            return "None"
        if param_type == "string":
            return f'"{default}"'
        if param_type == "boolean":
            return "True" if default else "False"
        return repr(default)

    def _build_docstring(self, tool: MCPTool) -> str:
        """Build function docstring."""
        lines = ['    """']

        # Main description
        desc = tool.description.replace('"""', '\\"\\"\\"')
        for line in desc.split('\n'):
            lines.append(f"    {line}")

        # Parameters section
        if tool.parameters:
            lines.append("")
            lines.append("    Args:")
            for param in tool.parameters:
                param_desc = param.description.replace('\n', ' ')
                lines.append(f"        {param.name}: {param_desc}")

        # Returns section
        lines.append("")
        lines.append("    Returns:")
        lines.append("        API response data")

        lines.append('    """')
        return "\n".join(lines)

    def _build_function_body(self, tool: MCPTool) -> str:
        """Build function body for API call with error handling."""
        lines = []

        # Build path with substitutions
        path = tool.path
        path_params = tool.path_parameters
        if path_params:
            for param in path_params:
                original = param.original_name or param.name
                path = path.replace(f"{{{original}}}", f"{{{param.name}}}")
            lines.append(f'    path = f"{path}"')
        else:
            lines.append(f'    path = "{path}"')

        # Build query params
        query_params = tool.query_parameters
        if query_params:
            lines.append("    params = {}")
            for param in query_params:
                original = param.original_name or param.name
                if param.required:
                    lines.append(f'    params["{original}"] = {param.name}')
                else:
                    lines.append(f"    if {param.name} is not None:")
                    lines.append(f'        params["{original}"] = {param.name}')
        else:
            lines.append("    params = None")

        # Build body
        body_params = tool.body_parameters
        if body_params:
            lines.append("    body = {}")
            for param in body_params:
                original = param.original_name or param.name
                if param.required:
                    lines.append(f'    body["{original}"] = {param.name}')
                else:
                    lines.append(f"    if {param.name} is not None:")
                    lines.append(f'        body["{original}"] = {param.name}')
        elif tool.body_schema:
            lines.append("    body = {}  # TODO: Handle raw body schema")
        else:
            lines.append("    body = None")

        # Make request with error handling
        lines.append("")
        lines.append("    try:")
        lines.append(f'        return await make_request("{tool.method.value.upper()}", path, params=params, json_body=body)')
        lines.append("    except APIError as e:")
        lines.append('        return {"ok": False, "error": str(e), "status_code": e.status_code, "details": e.response_data}')

        return "\n".join(lines)

    def _generate_types(
        self,
        package_name: str,
        tools: list[MCPTool],
    ) -> GeneratedFile:
        """Generate types.py with Pydantic models (placeholder)."""
        content = f'''"""
Type definitions for {package_name}.

Auto-generated from OpenAPI schemas.
"""

from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Generic API response wrapper."""
    success: bool = True
    data: Any = None
    error: str | None = None


# TODO: Generate specific models from OpenAPI schemas
'''
        return GeneratedFile(
            path=f"src/{package_name}/types.py",
            content=content
        )
