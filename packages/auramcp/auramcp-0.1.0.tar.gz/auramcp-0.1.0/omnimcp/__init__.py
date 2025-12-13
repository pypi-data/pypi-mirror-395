"""OmniMCP - Universal MCP Server Generator

Build MCP servers from any OpenAPI spec.
"""

__version__ = "0.1.0"

from omnimcp.generator.parser import OpenAPIParser, ParsedSpec
from omnimcp.generator.converter import MCPConverter, MCPTool
from omnimcp.generator.codegen import MCPCodeGenerator, GeneratedServer, GeneratedFile

__all__ = [
    "OpenAPIParser",
    "ParsedSpec",
    "MCPConverter",
    "MCPTool",
    "MCPCodeGenerator",
    "GeneratedServer",
    "GeneratedFile",
    "__version__",
]
