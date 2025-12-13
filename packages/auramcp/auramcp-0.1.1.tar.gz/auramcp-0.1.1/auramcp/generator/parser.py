"""
OpenAPI Parser - Parse OpenAPI 2.0 (Swagger) and 3.x specifications.

Converts specs into a normalized internal format for MCP tool generation.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import httpx
import yaml


class ParameterLocation(str, Enum):
    """Where a parameter is located in the request."""
    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    COOKIE = "cookie"
    BODY = "body"
    FORM_DATA = "formData"  # OpenAPI 2.0 form data


class HTTPMethod(str, Enum):
    """HTTP methods."""
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"
    HEAD = "head"
    OPTIONS = "options"


@dataclass
class Parameter:
    """Represents an API parameter."""
    name: str
    location: ParameterLocation
    description: str = ""
    required: bool = False
    schema: dict[str, Any] = field(default_factory=dict)
    example: Any = None
    deprecated: bool = False

    @property
    def python_type(self) -> str:
        """Infer Python type from JSON schema."""
        schema_type = self.schema.get("type", "any")
        type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict",
        }
        return type_map.get(schema_type, "Any")


@dataclass
class RequestBody:
    """Represents a request body."""
    description: str = ""
    required: bool = False
    content_type: str = "application/json"
    schema: dict[str, Any] = field(default_factory=dict)
    example: Any = None


@dataclass
class Response:
    """Represents an API response."""
    status_code: str
    description: str = ""
    content_type: str = "application/json"
    schema: dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityRequirement:
    """Security requirement for an endpoint."""
    scheme_name: str
    scopes: list[str] = field(default_factory=list)


@dataclass
class Endpoint:
    """Represents a single API endpoint."""
    path: str
    method: HTTPMethod
    operation_id: str
    summary: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)
    parameters: list[Parameter] = field(default_factory=list)
    request_body: RequestBody | None = None
    responses: list[Response] = field(default_factory=list)
    security: list[SecurityRequirement] = field(default_factory=list)
    deprecated: bool = False

    @property
    def tool_name(self) -> str:
        """Generate a clean tool name from operation_id or path."""
        if self.operation_id:
            # Convert camelCase or snake_case to snake_case
            name = re.sub(r'([A-Z])', r'_\1', self.operation_id).lower()
            name = re.sub(r'[-.]', '_', name)
            name = re.sub(r'_+', '_', name).strip('_')
            return name

        # Generate from path and method
        path_parts = self.path.strip('/').split('/')
        # Remove path parameters
        path_parts = [p for p in path_parts if not p.startswith('{')]
        name = '_'.join(path_parts)
        return f"{self.method.value}_{name}"


@dataclass
class Schema:
    """Represents a reusable schema/model."""
    name: str
    schema: dict[str, Any]
    description: str = ""


@dataclass
class SecurityScheme:
    """Represents an authentication scheme."""
    name: str
    type: str  # apiKey, http, oauth2, openIdConnect
    description: str = ""
    # For apiKey
    param_name: str | None = None
    location: str | None = None  # query, header, cookie
    # For http
    scheme: str | None = None  # bearer, basic
    bearer_format: str | None = None
    # For oauth2
    flows: dict[str, Any] = field(default_factory=dict)


@dataclass
class ServerInfo:
    """API server information."""
    url: str
    description: str = ""
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedSpec:
    """Normalized representation of an OpenAPI spec."""
    title: str
    version: str
    description: str = ""
    servers: list[ServerInfo] = field(default_factory=list)
    endpoints: list[Endpoint] = field(default_factory=list)
    schemas: dict[str, Schema] = field(default_factory=dict)
    security_schemes: dict[str, SecurityScheme] = field(default_factory=dict)
    global_security: list[SecurityRequirement] = field(default_factory=list)

    @property
    def base_url(self) -> str:
        """Get the primary base URL."""
        if self.servers:
            return self.servers[0].url.rstrip('/')
        return ""


class OpenAPIParser:
    """Parse OpenAPI specs into normalized internal format."""

    def __init__(self):
        self._ref_cache: dict[str, Any] = {}

    def parse(self, spec_source: str | dict | Path) -> ParsedSpec:
        """
        Parse OpenAPI spec from file path, URL, or dict.
        Handles both OpenAPI 2.0 and 3.x.

        Args:
            spec_source: File path, URL, or spec dict

        Returns:
            Normalized ParsedSpec object
        """
        spec = self._load_spec(spec_source)

        # Determine version and normalize
        if self._is_openapi_2(spec):
            spec = self._convert_2_to_3(spec)

        return self._parse_openapi_3(spec)

    def _load_spec(self, source: str | dict | Path) -> dict:
        """Load spec from various sources."""
        if isinstance(source, dict):
            return source

        if isinstance(source, Path):
            source = str(source)

        # Check if URL
        if source.startswith(('http://', 'https://')):
            response = httpx.get(source, follow_redirects=True)
            response.raise_for_status()
            content = response.text
            # Try JSON first, then YAML
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return yaml.safe_load(content)

        # File path
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Spec file not found: {source}")

        content = path.read_text()
        if path.suffix in ('.yaml', '.yml'):
            return yaml.safe_load(content)
        return json.loads(content)

    def _is_openapi_2(self, spec: dict) -> bool:
        """Check if spec is OpenAPI 2.0 (Swagger)."""
        return 'swagger' in spec and spec.get('swagger', '').startswith('2')

    def _convert_2_to_3(self, spec: dict) -> dict:
        """Convert OpenAPI 2.0 to 3.x format."""
        converted = {
            'openapi': '3.0.0',
            'info': spec.get('info', {}),
            'paths': {},
            'components': {
                'schemas': spec.get('definitions', {}),
                'securitySchemes': {},
            }
        }

        # Convert servers from host/basePath
        host = spec.get('host', 'localhost')
        base_path = spec.get('basePath', '')
        schemes = spec.get('schemes', ['https'])
        scheme = schemes[0] if schemes else 'https'
        converted['servers'] = [{'url': f"{scheme}://{host}{base_path}"}]

        # Convert security definitions
        if 'securityDefinitions' in spec:
            for name, sec_def in spec['securityDefinitions'].items():
                converted['components']['securitySchemes'][name] = self._convert_security_def(sec_def)

        # Convert paths
        for path, path_item in spec.get('paths', {}).items():
            converted['paths'][path] = self._convert_path_item_2_to_3(path_item)

        # Global security
        if 'security' in spec:
            converted['security'] = spec['security']

        return converted

    def _convert_security_def(self, sec_def: dict) -> dict:
        """Convert OpenAPI 2.0 security definition to 3.0."""
        sec_type = sec_def.get('type', '')

        if sec_type == 'apiKey':
            return {
                'type': 'apiKey',
                'name': sec_def.get('name', ''),
                'in': sec_def.get('in', 'header'),
            }
        elif sec_type == 'basic':
            return {
                'type': 'http',
                'scheme': 'basic',
            }
        elif sec_type == 'oauth2':
            flow = sec_def.get('flow', 'implicit')
            flows = {}

            flow_config = {
                'scopes': sec_def.get('scopes', {}),
            }

            if flow in ('implicit', 'accessCode'):
                flow_config['authorizationUrl'] = sec_def.get('authorizationUrl', '')
            if flow in ('password', 'application', 'accessCode'):
                flow_config['tokenUrl'] = sec_def.get('tokenUrl', '')

            flow_map = {
                'implicit': 'implicit',
                'password': 'password',
                'application': 'clientCredentials',
                'accessCode': 'authorizationCode',
            }
            flows[flow_map.get(flow, flow)] = flow_config

            return {
                'type': 'oauth2',
                'flows': flows,
            }

        return sec_def

    def _convert_path_item_2_to_3(self, path_item: dict) -> dict:
        """Convert path item from 2.0 to 3.0."""
        converted = {}

        for method in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
            if method not in path_item:
                continue

            op = path_item[method]
            converted_op = {
                'operationId': op.get('operationId'),
                'summary': op.get('summary', ''),
                'description': op.get('description', ''),
                'tags': op.get('tags', []),
                'deprecated': op.get('deprecated', False),
                'parameters': [],
                'responses': {},
            }

            # Convert parameters
            for param in op.get('parameters', []):
                if param.get('in') == 'body':
                    # Convert body parameter to requestBody
                    converted_op['requestBody'] = {
                        'description': param.get('description', ''),
                        'required': param.get('required', False),
                        'content': {
                            'application/json': {
                                'schema': param.get('schema', {})
                            }
                        }
                    }
                else:
                    converted_param = {
                        'name': param.get('name'),
                        'in': param.get('in'),
                        'description': param.get('description', ''),
                        'required': param.get('required', False),
                        'deprecated': param.get('deprecated', False),
                        'schema': {
                            'type': param.get('type', 'string'),
                        }
                    }
                    if 'enum' in param:
                        converted_param['schema']['enum'] = param['enum']
                    if 'default' in param:
                        converted_param['schema']['default'] = param['default']
                    if 'format' in param:
                        converted_param['schema']['format'] = param['format']
                    converted_op['parameters'].append(converted_param)

            # Convert responses
            for status, response in op.get('responses', {}).items():
                converted_response = {
                    'description': response.get('description', ''),
                }
                if 'schema' in response:
                    converted_response['content'] = {
                        'application/json': {
                            'schema': response['schema']
                        }
                    }
                converted_op['responses'][status] = converted_response

            # Security
            if 'security' in op:
                converted_op['security'] = op['security']

            converted[method] = converted_op

        return converted

    def _parse_openapi_3(self, spec: dict) -> ParsedSpec:
        """Parse OpenAPI 3.x spec."""
        self._ref_cache = {}
        self._spec = spec

        info = spec.get('info', {})

        parsed = ParsedSpec(
            title=info.get('title', 'Unknown API'),
            version=info.get('version', '1.0.0'),
            description=info.get('description', ''),
        )

        # Parse servers
        for server in spec.get('servers', []):
            parsed.servers.append(ServerInfo(
                url=server.get('url', ''),
                description=server.get('description', ''),
                variables=server.get('variables', {}),
            ))

        # Parse security schemes
        components = spec.get('components', {})
        for name, scheme in components.get('securitySchemes', {}).items():
            parsed.security_schemes[name] = self._parse_security_scheme(name, scheme)

        # Parse schemas
        for name, schema in components.get('schemas', {}).items():
            parsed.schemas[name] = Schema(
                name=name,
                schema=schema,
                description=schema.get('description', ''),
            )

        # Parse global security
        for sec_req in spec.get('security', []):
            for scheme_name, scopes in sec_req.items():
                parsed.global_security.append(SecurityRequirement(
                    scheme_name=scheme_name,
                    scopes=scopes,
                ))

        # Parse endpoints
        for path, path_item in spec.get('paths', {}).items():
            parsed.endpoints.extend(self._parse_path_item(path, path_item, parsed.global_security))

        return parsed

    def _parse_security_scheme(self, name: str, scheme: dict) -> SecurityScheme:
        """Parse a security scheme."""
        return SecurityScheme(
            name=name,
            type=scheme.get('type', ''),
            description=scheme.get('description', ''),
            param_name=scheme.get('name'),
            location=scheme.get('in'),
            scheme=scheme.get('scheme'),
            bearer_format=scheme.get('bearerFormat'),
            flows=scheme.get('flows', {}),
        )

    def _parse_path_item(
        self,
        path: str,
        path_item: dict,
        global_security: list[SecurityRequirement]
    ) -> list[Endpoint]:
        """Parse all endpoints from a path item."""
        endpoints = []

        # Path-level parameters
        path_params = path_item.get('parameters', [])

        for method in HTTPMethod:
            if method.value not in path_item:
                continue

            op = path_item[method.value]
            endpoint = self._parse_operation(path, method, op, path_params, global_security)
            endpoints.append(endpoint)

        return endpoints

    def _parse_operation(
        self,
        path: str,
        method: HTTPMethod,
        op: dict,
        path_params: list,
        global_security: list[SecurityRequirement]
    ) -> Endpoint:
        """Parse a single operation/endpoint."""
        # Generate operation_id if not present
        operation_id = op.get('operationId', '')
        if not operation_id:
            path_parts = path.strip('/').replace('/', '_').replace('{', '').replace('}', '')
            operation_id = f"{method.value}_{path_parts}"

        endpoint = Endpoint(
            path=path,
            method=method,
            operation_id=operation_id,
            summary=op.get('summary', ''),
            description=op.get('description', ''),
            tags=op.get('tags', []),
            deprecated=op.get('deprecated', False),
        )

        # Combine path-level and operation-level parameters
        all_params = path_params + op.get('parameters', [])
        for param in all_params:
            param = self._resolve_ref(param)
            endpoint.parameters.append(self._parse_parameter(param))

        # Parse request body
        if 'requestBody' in op:
            endpoint.request_body = self._parse_request_body(op['requestBody'])

        # Parse responses
        for status, response in op.get('responses', {}).items():
            response = self._resolve_ref(response)
            endpoint.responses.append(self._parse_response(status, response))

        # Parse security (operation-level overrides global)
        if 'security' in op:
            for sec_req in op['security']:
                for scheme_name, scopes in sec_req.items():
                    endpoint.security.append(SecurityRequirement(
                        scheme_name=scheme_name,
                        scopes=scopes,
                    ))
        else:
            endpoint.security = global_security.copy()

        return endpoint

    def _parse_parameter(self, param: dict) -> Parameter:
        """Parse a parameter."""
        return Parameter(
            name=param.get('name', ''),
            location=ParameterLocation(param.get('in', 'query')),
            description=param.get('description', ''),
            required=param.get('required', False),
            schema=self._resolve_ref(param.get('schema', {})),
            example=param.get('example'),
            deprecated=param.get('deprecated', False),
        )

    def _parse_request_body(self, body: dict) -> RequestBody:
        """Parse a request body."""
        body = self._resolve_ref(body)

        content = body.get('content', {})
        # Prefer JSON, fall back to first available
        if 'application/json' in content:
            content_type = 'application/json'
            media_type = content['application/json']
        elif content:
            content_type = next(iter(content))
            media_type = content[content_type]
        else:
            content_type = 'application/json'
            media_type = {}

        return RequestBody(
            description=body.get('description', ''),
            required=body.get('required', False),
            content_type=content_type,
            schema=self._resolve_ref(media_type.get('schema', {})),
            example=media_type.get('example'),
        )

    def _parse_response(self, status: str, response: dict) -> Response:
        """Parse a response."""
        content = response.get('content', {})

        if 'application/json' in content:
            content_type = 'application/json'
            media_type = content['application/json']
        elif content:
            content_type = next(iter(content))
            media_type = content[content_type]
        else:
            content_type = 'application/json'
            media_type = {}

        return Response(
            status_code=status,
            description=response.get('description', ''),
            content_type=content_type,
            schema=self._resolve_ref(media_type.get('schema', {})),
        )

    def _resolve_ref(self, obj: dict) -> dict:
        """Resolve $ref references in the spec."""
        if not isinstance(obj, dict):
            return obj

        if '$ref' not in obj:
            return obj

        ref = obj['$ref']

        # Check cache
        if ref in self._ref_cache:
            return self._ref_cache[ref]

        # Parse reference path
        if not ref.startswith('#/'):
            # External ref - not supported yet
            return obj

        parts = ref[2:].split('/')
        resolved = self._spec
        for part in parts:
            # Handle JSON pointer escaping
            part = part.replace('~1', '/').replace('~0', '~')
            resolved = resolved.get(part, {})

        self._ref_cache[ref] = resolved
        return resolved
