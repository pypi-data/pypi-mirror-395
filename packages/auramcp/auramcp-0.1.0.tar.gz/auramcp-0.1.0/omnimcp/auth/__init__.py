"""Authentication layer for OmniMCP."""

from omnimcp.auth.registry import AuthRegistry, AuthConfig, AuthType
from omnimcp.auth.handlers import AuthHandler, get_auth_handler

__all__ = [
    "AuthRegistry",
    "AuthConfig",
    "AuthType",
    "AuthHandler",
    "get_auth_handler",
]
