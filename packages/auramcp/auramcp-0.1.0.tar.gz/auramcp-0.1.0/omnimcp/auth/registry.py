"""
Auth Registry - Load and manage authentication configurations.

Handles per-provider authentication settings stored in YAML configs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml


class AuthType(str, Enum):
    """Supported authentication types."""
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BEARER = "bearer"
    BASIC = "basic"
    CUSTOM = "custom"


@dataclass
class OAuth2Config:
    """OAuth2 configuration."""
    authorization_url: str = ""
    token_url: str = ""
    refresh_url: str = ""
    scopes: list[str] = field(default_factory=list)
    token_placement: str = "header"  # header or query
    token_param_name: str = "Authorization"
    token_prefix: str = "Bearer"


@dataclass
class APIKeyConfig:
    """API Key configuration."""
    param_name: str = "X-API-Key"
    placement: str = "header"  # header or query
    prefix: str = ""


@dataclass
class BearerConfig:
    """Bearer token configuration."""
    header_name: str = "Authorization"
    prefix: str = "Bearer"


@dataclass
class EnvVarConfig:
    """Environment variable names for credentials."""
    client_id: str | None = None
    client_secret: str | None = None
    api_key: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    username: str | None = None
    password: str | None = None


@dataclass
class AuthConfig:
    """Complete authentication configuration for a provider."""
    provider: str
    display_name: str = ""
    docs_url: str = ""
    auth_type: AuthType = AuthType.API_KEY

    oauth2: OAuth2Config | None = None
    api_key: APIKeyConfig | None = None
    bearer: BearerConfig | None = None

    quirks: list[str] = field(default_factory=list)
    env_vars: EnvVarConfig = field(default_factory=EnvVarConfig)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuthConfig:
        """Create AuthConfig from dictionary (loaded from YAML)."""
        auth_type = AuthType(data.get("auth_type", "api_key"))

        config = cls(
            provider=data.get("provider", ""),
            display_name=data.get("display_name", ""),
            docs_url=data.get("docs_url", ""),
            auth_type=auth_type,
            quirks=data.get("quirks", []),
        )

        # Parse OAuth2 config
        if "oauth2" in data:
            oauth_data = data["oauth2"]
            config.oauth2 = OAuth2Config(
                authorization_url=oauth_data.get("authorization_url", ""),
                token_url=oauth_data.get("token_url", ""),
                refresh_url=oauth_data.get("refresh_url", ""),
                scopes=oauth_data.get("scopes", []),
                token_placement=oauth_data.get("token_placement", "header"),
                token_param_name=oauth_data.get("token_param_name", "Authorization"),
                token_prefix=oauth_data.get("token_prefix", "Bearer"),
            )

        # Parse API Key config
        if "api_key" in data:
            key_data = data["api_key"]
            config.api_key = APIKeyConfig(
                param_name=key_data.get("param_name", "X-API-Key"),
                placement=key_data.get("placement", "header"),
                prefix=key_data.get("prefix", ""),
            )

        # Parse Bearer config
        if "bearer" in data:
            bearer_data = data["bearer"]
            config.bearer = BearerConfig(
                header_name=bearer_data.get("header_name", "Authorization"),
                prefix=bearer_data.get("prefix", "Bearer"),
            )

        # Parse env vars
        if "env_vars" in data:
            env_data = data["env_vars"]
            config.env_vars = EnvVarConfig(
                client_id=env_data.get("client_id"),
                client_secret=env_data.get("client_secret"),
                api_key=env_data.get("api_key"),
                access_token=env_data.get("access_token"),
                refresh_token=env_data.get("refresh_token"),
                username=env_data.get("username"),
                password=env_data.get("password"),
            )

        return config

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        data: dict[str, Any] = {
            "provider": self.provider,
            "display_name": self.display_name,
            "docs_url": self.docs_url,
            "auth_type": self.auth_type.value,
            "quirks": self.quirks,
        }

        if self.oauth2:
            data["oauth2"] = {
                "authorization_url": self.oauth2.authorization_url,
                "token_url": self.oauth2.token_url,
                "refresh_url": self.oauth2.refresh_url,
                "scopes": self.oauth2.scopes,
                "token_placement": self.oauth2.token_placement,
                "token_param_name": self.oauth2.token_param_name,
                "token_prefix": self.oauth2.token_prefix,
            }

        if self.api_key:
            data["api_key"] = {
                "param_name": self.api_key.param_name,
                "placement": self.api_key.placement,
                "prefix": self.api_key.prefix,
            }

        if self.bearer:
            data["bearer"] = {
                "header_name": self.bearer.header_name,
                "prefix": self.bearer.prefix,
            }

        env_dict = {}
        if self.env_vars.client_id:
            env_dict["client_id"] = self.env_vars.client_id
        if self.env_vars.client_secret:
            env_dict["client_secret"] = self.env_vars.client_secret
        if self.env_vars.api_key:
            env_dict["api_key"] = self.env_vars.api_key
        if self.env_vars.access_token:
            env_dict["access_token"] = self.env_vars.access_token
        if env_dict:
            data["env_vars"] = env_dict

        return data


class AuthRegistry:
    """Manage authentication configurations for providers."""

    def __init__(self, configs_dir: Path | None = None):
        """
        Initialize the auth registry.

        Args:
            configs_dir: Directory containing YAML config files.
                        Defaults to omnimcp/auth/configs/
        """
        if configs_dir is None:
            configs_dir = Path(__file__).parent / "configs"
        self.configs_dir = configs_dir
        self._configs: dict[str, AuthConfig] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        """Ensure configs are loaded."""
        if not self._loaded:
            self._load_all_configs()
            self._loaded = True

    def _load_all_configs(self) -> None:
        """Load all config files from the configs directory."""
        if not self.configs_dir.exists():
            return

        for config_file in self.configs_dir.glob("*.yaml"):
            if config_file.name.startswith("_"):
                continue  # Skip templates

            try:
                config = self._load_config_file(config_file)
                self._configs[config.provider] = config
            except Exception as e:
                # Log warning but continue loading other configs
                print(f"Warning: Failed to load {config_file}: {e}")

    def _load_config_file(self, path: Path) -> AuthConfig:
        """Load a single config file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return AuthConfig.from_dict(data)

    def load_config(self, provider: str) -> AuthConfig:
        """
        Load auth config for a provider.

        Args:
            provider: Provider name (e.g., "slack")

        Returns:
            AuthConfig for the provider

        Raises:
            KeyError: If provider config not found
        """
        self._ensure_loaded()

        if provider in self._configs:
            return self._configs[provider]

        # Try to load directly
        config_path = self.configs_dir / f"{provider}.yaml"
        if config_path.exists():
            config = self._load_config_file(config_path)
            self._configs[provider] = config
            return config

        raise KeyError(f"No auth config found for provider: {provider}")

    def get_config(self, provider: str) -> AuthConfig | None:
        """
        Get auth config for a provider, returning None if not found.

        Args:
            provider: Provider name

        Returns:
            AuthConfig or None
        """
        try:
            return self.load_config(provider)
        except KeyError:
            return None

    def has_config(self, provider: str) -> bool:
        """Check if provider has auth config."""
        self._ensure_loaded()
        if provider in self._configs:
            return True
        return (self.configs_dir / f"{provider}.yaml").exists()

    def list_providers(self) -> list[str]:
        """List all configured providers."""
        self._ensure_loaded()
        return sorted(self._configs.keys())

    def register_config(self, config: AuthConfig) -> None:
        """Register a config programmatically."""
        self._configs[config.provider] = config

    def save_config(self, config: AuthConfig) -> Path:
        """
        Save a config to a YAML file.

        Args:
            config: AuthConfig to save

        Returns:
            Path to saved file
        """
        self.configs_dir.mkdir(parents=True, exist_ok=True)
        path = self.configs_dir / f"{config.provider}.yaml"

        with open(path, "w") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, sort_keys=False)

        self._configs[config.provider] = config
        return path
