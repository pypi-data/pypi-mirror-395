"""
Auth Handlers - Inject authentication into HTTP requests.

Provides handlers for different auth types (OAuth2, API Key, Bearer, Basic).
"""

from __future__ import annotations

import base64
import os
from abc import ABC, abstractmethod
from typing import Any

import httpx

from auramcp.auth.registry import AuthConfig, AuthType


class AuthHandler(ABC):
    """Base class for authentication handlers."""

    def __init__(self, config: AuthConfig):
        self.config = config

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        """Get authentication headers."""
        pass

    @abstractmethod
    def get_query_params(self) -> dict[str, str]:
        """Get authentication query parameters."""
        pass

    def inject_auth(self, request: httpx.Request) -> httpx.Request:
        """Inject authentication into a request."""
        # Add headers
        for key, value in self.get_headers().items():
            request.headers[key] = value

        # Add query params (requires rebuilding URL)
        query_params = self.get_query_params()
        if query_params:
            # Parse existing URL and add params
            url = request.url
            new_params = dict(url.params)
            new_params.update(query_params)
            request.url = url.copy_with(params=new_params)

        return request

    def _get_env(self, var_name: str | None, default: str = "") -> str:
        """Get environment variable value."""
        if var_name:
            return os.environ.get(var_name, default)
        return default


class OAuth2Handler(AuthHandler):
    """Handle OAuth2 authentication."""

    def get_headers(self) -> dict[str, str]:
        """Get OAuth2 authentication headers."""
        if not self.config.oauth2:
            return {}

        oauth = self.config.oauth2
        if oauth.token_placement != "header":
            return {}

        token = self._get_env(self.config.env_vars.access_token)
        if not token:
            raise ValueError(
                f"Environment variable {self.config.env_vars.access_token} required for OAuth2"
            )

        prefix = oauth.token_prefix
        if prefix:
            return {oauth.token_param_name: f"{prefix} {token}"}
        return {oauth.token_param_name: token}

    def get_query_params(self) -> dict[str, str]:
        """Get OAuth2 query parameters."""
        if not self.config.oauth2:
            return {}

        oauth = self.config.oauth2
        if oauth.token_placement != "query":
            return {}

        token = self._get_env(self.config.env_vars.access_token)
        if not token:
            raise ValueError(
                f"Environment variable {self.config.env_vars.access_token} required for OAuth2"
            )

        return {oauth.token_param_name: token}

    def get_authorization_url(
        self,
        redirect_uri: str,
        state: str,
        scopes: list[str] | None = None,
    ) -> str:
        """Generate authorization URL for OAuth2 flow."""
        if not self.config.oauth2:
            raise ValueError("OAuth2 not configured")

        oauth = self.config.oauth2
        scopes = scopes or oauth.scopes

        params = {
            "client_id": self._get_env(self.config.env_vars.client_id),
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
        }

        if scopes:
            params["scope"] = " ".join(scopes)

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{oauth.authorization_url}?{query}"

    async def exchange_code(
        self,
        code: str,
        redirect_uri: str,
    ) -> dict[str, Any]:
        """Exchange authorization code for tokens."""
        if not self.config.oauth2:
            raise ValueError("OAuth2 not configured")

        oauth = self.config.oauth2

        async with httpx.AsyncClient() as client:
            response = await client.post(
                oauth.token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": self._get_env(self.config.env_vars.client_id),
                    "client_secret": self._get_env(self.config.env_vars.client_secret),
                },
            )
            response.raise_for_status()
            return response.json()

    async def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        """Refresh the access token."""
        if not self.config.oauth2:
            raise ValueError("OAuth2 not configured")

        oauth = self.config.oauth2
        refresh_url = oauth.refresh_url or oauth.token_url

        async with httpx.AsyncClient() as client:
            response = await client.post(
                refresh_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self._get_env(self.config.env_vars.client_id),
                    "client_secret": self._get_env(self.config.env_vars.client_secret),
                },
            )
            response.raise_for_status()
            return response.json()


class APIKeyHandler(AuthHandler):
    """Handle API Key authentication."""

    def get_headers(self) -> dict[str, str]:
        """Get API Key authentication headers."""
        if not self.config.api_key:
            return {}

        key_config = self.config.api_key
        if key_config.placement != "header":
            return {}

        api_key = self._get_env(self.config.env_vars.api_key)
        if not api_key:
            raise ValueError(
                f"Environment variable {self.config.env_vars.api_key} required for API Key auth"
            )

        if key_config.prefix:
            return {key_config.param_name: f"{key_config.prefix} {api_key}"}
        return {key_config.param_name: api_key}

    def get_query_params(self) -> dict[str, str]:
        """Get API Key query parameters."""
        if not self.config.api_key:
            return {}

        key_config = self.config.api_key
        if key_config.placement != "query":
            return {}

        api_key = self._get_env(self.config.env_vars.api_key)
        if not api_key:
            raise ValueError(
                f"Environment variable {self.config.env_vars.api_key} required for API Key auth"
            )

        return {key_config.param_name: api_key}


class BearerHandler(AuthHandler):
    """Handle Bearer token authentication."""

    def get_headers(self) -> dict[str, str]:
        """Get Bearer token authentication headers."""
        if not self.config.bearer:
            # Fall back to default bearer config
            token = self._get_env(self.config.env_vars.access_token)
            if token:
                return {"Authorization": f"Bearer {token}"}
            return {}

        bearer = self.config.bearer
        token = self._get_env(self.config.env_vars.access_token)
        if not token:
            raise ValueError(
                f"Environment variable {self.config.env_vars.access_token} required for Bearer auth"
            )

        prefix = bearer.prefix
        if prefix:
            return {bearer.header_name: f"{prefix} {token}"}
        return {bearer.header_name: token}

    def get_query_params(self) -> dict[str, str]:
        """Bearer tokens don't use query params."""
        return {}


class BasicHandler(AuthHandler):
    """Handle Basic authentication."""

    def get_headers(self) -> dict[str, str]:
        """Get Basic authentication headers."""
        username = self._get_env(self.config.env_vars.username)
        password = self._get_env(self.config.env_vars.password)

        if not username:
            raise ValueError(
                f"Environment variable {self.config.env_vars.username} required for Basic auth"
            )

        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    def get_query_params(self) -> dict[str, str]:
        """Basic auth doesn't use query params."""
        return {}


class NoAuthHandler(AuthHandler):
    """Handler for APIs that don't require authentication."""

    def get_headers(self) -> dict[str, str]:
        return {}

    def get_query_params(self) -> dict[str, str]:
        return {}


def get_auth_handler(config: AuthConfig) -> AuthHandler:
    """
    Get the appropriate auth handler for a config.

    Args:
        config: AuthConfig for the provider

    Returns:
        Appropriate AuthHandler instance
    """
    handlers = {
        AuthType.OAUTH2: OAuth2Handler,
        AuthType.API_KEY: APIKeyHandler,
        AuthType.BEARER: BearerHandler,
        AuthType.BASIC: BasicHandler,
    }

    handler_class = handlers.get(config.auth_type, NoAuthHandler)
    return handler_class(config)
