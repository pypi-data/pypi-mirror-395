# OmniMCP - Universal MCP Server Generator

Generate MCP (Model Context Protocol) servers from any OpenAPI specification. Connect LLM agents to Slack, GitHub, Notion, Stripe, and 100+ other APIs instantly.

## How It Works

OmniMCP is a **generator tool** that creates standalone MCP server packages:

1. **Install OmniMCP** → The generator CLI
2. **Run `omnimcp generate <provider>`** → Creates a new Python package (e.g., `omnimcp_slack`)
3. **Install the generated package** → `pip install -e .` in the output folder
4. **Run the MCP server** → `python -m omnimcp_slack`

Each generated server is independent and can be distributed separately.

## Features

- **Parse OpenAPI 2.0 & 3.x** - Automatically handles both Swagger and OpenAPI specs
- **Generate MCP Servers** - Creates complete, runnable Python packages with FastMCP
- **Auth Ready** - Pre-configured authentication for popular APIs (OAuth2, API Key, Bearer)
- **CLI & Programmatic** - Use from command line or import as a library
- **LLM Enhancement** - Optional Claude-powered review and description enhancement

## Installation

```bash
pip install omnimcp
```

For LLM review features:
```bash
pip install omnimcp[llm]
```

## Quick Start

### 1. Generate a Server

```bash
# Generate MCP server for Slack
omnimcp generate slack --output ./servers

# Generate with LLM review (optional)
omnimcp generate notion --review --output ./servers

# List available providers
omnimcp list

# Search for APIs
omnimcp list --search "email"

# Get provider info
omnimcp info github
```

### 2. Install and Run the Generated Server

Each generated server is a standalone pip package. After generation:

```bash
# Navigate to the generated server
cd servers/slack

# Install the generated package
pip install -e .

# Set the required environment variable (shown after generation)
export SLACK_BOT_TOKEN=xoxb-your-token

# Run the MCP server
python -m omnimcp_slack
```

### 3. Connect to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "slack": {
      "command": "python",
      "args": ["-m", "omnimcp_slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token"
      }
    }
  }
}
```

> **Note:** The environment variable name depends on the provider and auth type.
> The CLI will show you the exact variable name after generation.

## Programmatic Usage

```python
from omnimcp.generator import OpenAPIParser, MCPConverter, MCPCodeGenerator

# Parse an OpenAPI spec
parser = OpenAPIParser()
parsed = parser.parse("https://api.example.com/openapi.json")

# Convert to MCP tools
converter = MCPConverter()
tools = converter.convert(parsed)

# Generate server code
generator = MCPCodeGenerator()
server = generator.generate(
    tools=tools,
    server_name="myapi",
    base_url=parsed.base_url,
    auth_type="bearer",
)

# Write to disk
server.write("./output/myapi")
```

## Supported Providers

### Tier 1 (Production Ready)
- Slack
- GitHub
- Notion
- Stripe
- Airtable
- HubSpot
- Trello
- Discord

### Tier 2 (Auto-generated + Reviewed)
- Asana, Linear, Jira
- Zendesk, Intercom
- Mailchimp, SendGrid, Twilio
- Shopify, Zoom, Calendly
- And 30+ more...

### Tier 3 (Fully Automated)
- All 2000+ APIs from APIs.guru

## Development

```bash
# Clone and install
git clone https://github.com/omnimcp/omnimcp.git
cd omnimcp
pip install -e ".[dev]"

# Run tests
pytest

# Run example
python scripts/generate_example.py
```

## Environment Variables

```bash
# For LLM review (optional)
ANTHROPIC_API_KEY=sk-ant-...

# Per-provider credentials (names shown after generation)
SLACK_BOT_TOKEN=xoxb-...          # Slack (OAuth2/Bot token)
GITHUB_TOKEN=ghp_...              # GitHub (Bearer token)
NOTION_TOKEN=secret_...           # Notion (Bearer token)
STRIPE_API_KEY=sk_test_...        # Stripe (API Key)
AIRTABLE_TOKEN=pat...             # Airtable (Bearer token)
```

> **Tip:** Run `omnimcp info <provider>` to see the required environment variable.

## Architecture

```
omnimcp/
├── generator/          # Core generator engine
│   ├── parser.py       # OpenAPI 2.0/3.x parsing
│   ├── converter.py    # OpenAPI → MCP tools
│   ├── codegen.py      # Python code generation
│   └── reviewer.py     # LLM enhancement
├── auth/               # Authentication layer
│   ├── registry.py     # Auth config management
│   ├── handlers.py     # OAuth2, API Key, Bearer
│   └── configs/        # Per-provider YAML configs
├── specs/              # Spec management
│   ├── fetcher.py      # APIs.guru + first-party
│   └── registry.py     # Provider index
└── cli.py              # Command-line interface
```

## License

MIT
