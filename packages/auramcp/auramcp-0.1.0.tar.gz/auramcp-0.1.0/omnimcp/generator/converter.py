"""
MCP Converter - Convert OpenAPI endpoints to MCP tool definitions.

Transforms parsed OpenAPI specs into MCP-compatible tool structures.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from omnimcp.generator.parser import (
    Endpoint,
    HTTPMethod,
    Parameter,
    ParameterLocation,
    ParsedSpec,
    RequestBody,
)


class ToolCategory(str, Enum):
    """Categories for MCP tools."""
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ACTION = "action"
    ADMIN = "admin"


@dataclass
class MCPToolParameter:
    """A parameter for an MCP tool."""
    name: str
    description: str
    type: str  # JSON Schema type
    required: bool = False
    default: Any = None
    enum: list[Any] | None = None
    format: str | None = None
    # Where this param goes in the HTTP request
    location: ParameterLocation = ParameterLocation.QUERY
    # Original name if different from sanitized name
    original_name: str | None = None

    def to_json_schema(self) -> dict[str, Any]:
        """Convert to JSON Schema property."""
        schema: dict[str, Any] = {
            "type": self.type,
            "description": self.description,
        }
        if self.default is not None:
            schema["default"] = self.default
        if self.enum:
            schema["enum"] = self.enum
        if self.format:
            schema["format"] = self.format
        return schema


@dataclass
class MCPTool:
    """MCP tool definition generated from an OpenAPI endpoint."""
    name: str
    description: str
    parameters: list[MCPToolParameter] = field(default_factory=list)
    category: ToolCategory = ToolCategory.READ

    # HTTP request details
    method: HTTPMethod = HTTPMethod.GET
    path: str = ""
    base_url: str = ""
    content_type: str = "application/json"

    # Original endpoint info
    operation_id: str = ""
    tags: list[str] = field(default_factory=list)
    deprecated: bool = False

    # Body schema if POST/PUT/PATCH
    body_schema: dict[str, Any] | None = None
    body_required: bool = False

    @property
    def required_parameters(self) -> list[str]:
        """Get names of required parameters."""
        return [p.name for p in self.parameters if p.required]

    @property
    def path_parameters(self) -> list[MCPToolParameter]:
        """Get path parameters."""
        return [p for p in self.parameters if p.location == ParameterLocation.PATH]

    @property
    def query_parameters(self) -> list[MCPToolParameter]:
        """Get query parameters."""
        return [p for p in self.parameters if p.location == ParameterLocation.QUERY]

    @property
    def header_parameters(self) -> list[MCPToolParameter]:
        """Get header parameters."""
        return [p for p in self.parameters if p.location == ParameterLocation.HEADER]

    @property
    def body_parameters(self) -> list[MCPToolParameter]:
        """Get body parameters (includes formData for OpenAPI 2.0)."""
        return [p for p in self.parameters if p.location in (ParameterLocation.BODY, ParameterLocation.FORM_DATA)]

    def to_input_schema(self) -> dict[str, Any]:
        """Generate JSON Schema for tool inputs."""
        properties: dict[str, Any] = {}
        required: list[str] = []

        for param in self.parameters:
            properties[param.name] = param.to_json_schema()
            if param.required:
                required.append(param.name)

        schema: dict[str, Any] = {
            "type": "object",
            "properties": properties,
        }

        if required:
            schema["required"] = required

        return schema


class MCPConverter:
    """Convert OpenAPI endpoints to MCP tools."""

    # Keywords that suggest write operations
    WRITE_KEYWORDS = {'create', 'add', 'post', 'new', 'insert', 'upload', 'send'}
    UPDATE_KEYWORDS = {'update', 'edit', 'modify', 'patch', 'change', 'set'}
    DELETE_KEYWORDS = {'delete', 'remove', 'destroy', 'archive', 'revoke'}
    ADMIN_KEYWORDS = {'admin', 'config', 'setting', 'permission', 'role', 'manage'}

    def __init__(self, deduplicate_names: bool = True):
        """
        Initialize converter.

        Args:
            deduplicate_names: If True, append suffixes to duplicate tool names
        """
        self.deduplicate_names = deduplicate_names
        self._used_names: set[str] = set()

    def convert(self, parsed_spec: ParsedSpec) -> list[MCPTool]:
        """
        Convert all endpoints to MCP tool definitions.

        Args:
            parsed_spec: Parsed OpenAPI specification

        Returns:
            List of MCP tool definitions
        """
        self._used_names.clear()
        tools = []

        for endpoint in parsed_spec.endpoints:
            tool = self.endpoint_to_tool(endpoint, parsed_spec.base_url)
            tools.append(tool)

        return tools

    def endpoint_to_tool(self, endpoint: Endpoint, base_url: str = "") -> MCPTool:
        """Convert a single endpoint to an MCP tool."""
        name = self._generate_tool_name(endpoint)
        description = self._generate_description(endpoint)
        category = self._infer_category(endpoint)

        tool = MCPTool(
            name=name,
            description=description,
            category=category,
            method=endpoint.method,
            path=endpoint.path,
            base_url=base_url,
            operation_id=endpoint.operation_id,
            tags=endpoint.tags,
            deprecated=endpoint.deprecated,
        )

        # Convert parameters (skip auth params)
        for param in endpoint.parameters:
            converted = self._convert_parameter(param)
            if converted is not None:
                tool.parameters.append(converted)

        # Convert request body
        if endpoint.request_body:
            self._convert_request_body(endpoint.request_body, tool)

        return tool

    def _generate_tool_name(self, endpoint: Endpoint) -> str:
        """Generate a unique, clean tool name."""
        # Start with operation_id if available
        if endpoint.operation_id:
            name = endpoint.operation_id
        else:
            # Generate from method + path
            path_parts = endpoint.path.strip('/').split('/')
            path_parts = [p.strip('{}') for p in path_parts]
            name = f"{endpoint.method.value}_{'_'.join(path_parts)}"

        # Clean the name
        name = self._sanitize_name(name)

        # Ensure uniqueness
        if self.deduplicate_names:
            name = self._make_unique(name)

        self._used_names.add(name)
        return name

    def _sanitize_name(self, name: str) -> str:
        """Sanitize a name to be a valid Python identifier."""
        # Convert camelCase to snake_case
        name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
        name = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', name)

        # Replace non-alphanumeric with underscore
        name = re.sub(r'[^a-zA-Z0-9]', '_', name)

        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)

        # Remove leading/trailing underscores
        name = name.strip('_')

        # Lowercase
        name = name.lower()

        # Ensure it doesn't start with a number
        if name and name[0].isdigit():
            name = f"op_{name}"

        # Handle empty name
        if not name:
            name = "unnamed_operation"

        return name

    def _make_unique(self, name: str) -> str:
        """Make a name unique by appending a suffix."""
        if name not in self._used_names:
            return name

        counter = 2
        while f"{name}_{counter}" in self._used_names:
            counter += 1

        return f"{name}_{counter}"

    def _generate_description(self, endpoint: Endpoint) -> str:
        """Generate a comprehensive description."""
        parts = []

        if endpoint.summary:
            parts.append(endpoint.summary)

        if endpoint.description and endpoint.description != endpoint.summary:
            parts.append(endpoint.description)

        if endpoint.deprecated:
            parts.append("⚠️ DEPRECATED")

        if not parts:
            # Generate from path and method
            path_desc = endpoint.path.replace('/', ' ').replace('{', '').replace('}', '')
            parts.append(f"{endpoint.method.value.upper()} {path_desc}")

        return '\n\n'.join(parts)

    def _infer_category(self, endpoint: Endpoint) -> ToolCategory:
        """Infer the tool category from endpoint details."""
        # Check method first
        if endpoint.method == HTTPMethod.DELETE:
            return ToolCategory.DELETE
        if endpoint.method == HTTPMethod.POST:
            name_lower = endpoint.operation_id.lower()
            if any(kw in name_lower for kw in self.DELETE_KEYWORDS):
                return ToolCategory.DELETE
            return ToolCategory.CREATE
        if endpoint.method in (HTTPMethod.PUT, HTTPMethod.PATCH):
            return ToolCategory.UPDATE

        # For GET, check keywords
        name_lower = endpoint.operation_id.lower()
        path_lower = endpoint.path.lower()
        combined = f"{name_lower} {path_lower}"

        if any(kw in combined for kw in self.ADMIN_KEYWORDS):
            return ToolCategory.ADMIN

        return ToolCategory.READ

    # Parameters to skip (auth handled by client)
    SKIP_PARAMETERS = {'token', 'access_token', 'api_key', 'apikey', 'authorization'}

    def _convert_parameter(self, param: Parameter) -> MCPToolParameter | None:
        """Convert an endpoint parameter to MCP tool parameter."""
        # Skip auth-related parameters (handled by client.py)
        if param.name.lower() in self.SKIP_PARAMETERS:
            return None

        # Map JSON Schema type to Python type hint string
        schema_type = param.schema.get('type', 'string')

        return MCPToolParameter(
            name=self._sanitize_name(param.name),
            original_name=param.name if param.name != self._sanitize_name(param.name) else None,
            description=param.description or f"The {param.name} parameter",
            type=schema_type,
            required=param.required,
            default=param.schema.get('default'),
            enum=param.schema.get('enum'),
            format=param.schema.get('format'),
            location=param.location,
        )

    def _convert_request_body(self, body: RequestBody, tool: MCPTool) -> None:
        """Convert request body to tool parameters or body schema."""
        tool.content_type = body.content_type
        tool.body_required = body.required

        schema = body.schema
        if not schema:
            return

        # If the body is an object, flatten its properties into parameters
        if schema.get('type') == 'object' and 'properties' in schema:
            required_props = set(schema.get('required', []))

            for prop_name, prop_schema in schema['properties'].items():
                param = MCPToolParameter(
                    name=self._sanitize_name(prop_name),
                    original_name=prop_name if prop_name != self._sanitize_name(prop_name) else None,
                    description=prop_schema.get('description', f"The {prop_name} field"),
                    type=prop_schema.get('type', 'string'),
                    required=prop_name in required_props,
                    default=prop_schema.get('default'),
                    enum=prop_schema.get('enum'),
                    format=prop_schema.get('format'),
                    location=ParameterLocation.BODY,
                )
                tool.parameters.append(param)
        else:
            # Keep as raw body schema
            tool.body_schema = schema

    def filter_by_category(
        self,
        tools: list[MCPTool],
        categories: list[ToolCategory]
    ) -> list[MCPTool]:
        """Filter tools by category."""
        return [t for t in tools if t.category in categories]

    def filter_by_tags(
        self,
        tools: list[MCPTool],
        tags: list[str],
        include: bool = True
    ) -> list[MCPTool]:
        """
        Filter tools by tags.

        Args:
            tools: List of tools
            tags: Tags to filter by
            include: If True, include matching tools; if False, exclude them
        """
        tags_set = set(t.lower() for t in tags)

        def matches(tool: MCPTool) -> bool:
            tool_tags = set(t.lower() for t in tool.tags)
            return bool(tool_tags & tags_set)

        if include:
            return [t for t in tools if matches(t)]
        else:
            return [t for t in tools if not matches(t)]

    def filter_deprecated(
        self,
        tools: list[MCPTool],
        include_deprecated: bool = False
    ) -> list[MCPTool]:
        """Filter out deprecated tools unless explicitly included."""
        if include_deprecated:
            return tools
        return [t for t in tools if not t.deprecated]
