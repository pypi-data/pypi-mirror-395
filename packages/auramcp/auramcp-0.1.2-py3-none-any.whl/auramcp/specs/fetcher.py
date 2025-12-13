"""
Spec Fetcher - Fetch OpenAPI specs from various sources.

Supports APIs.guru directory and first-party provider specs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
import yaml


@dataclass
class ProviderInfo:
    """Information about an API provider."""
    name: str
    title: str = ""
    description: str = ""
    version: str = ""
    logo_url: str = ""
    docs_url: str = ""
    spec_url: str = ""
    categories: list[str] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        """Get display name."""
        return self.title or self.name.replace(".", " ").title()


class SpecFetcher:
    """Fetch OpenAPI specs from various sources."""

    # APIs.guru REST API
    APIS_GURU_LIST_URL = "https://api.apis.guru/v2/list.json"
    APIS_GURU_API_URL = "https://api.apis.guru/v2/{provider}.json"

    # First-party spec URLs (preferred over APIs.guru)
    FIRST_PARTY_SPECS = {
        "slack": "https://raw.githubusercontent.com/slackapi/slack-api-specs/master/web-api/slack_web_openapi_v2.json",
        "stripe": "https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json",
        "github": "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json",
        "twilio": "https://raw.githubusercontent.com/twilio/twilio-oai/main/spec/json/twilio_api_v2010.json",
        "sendgrid": "https://raw.githubusercontent.com/sendgrid/sendgrid-oai/main/oai.json",
        "shopify": "https://raw.githubusercontent.com/Shopify/shopify-api-specs/main/admin/admin_2024-01.json",
    }

    # Aliases for common provider names
    PROVIDER_ALIASES = {
        "sheets": "googleapis.com:sheets",
        "gmail": "googleapis.com:gmail",
        "drive": "googleapis.com:drive",
        "calendar": "googleapis.com:calendar",
        "youtube": "googleapis.com:youtube",
        "google-sheets": "googleapis.com:sheets",
        "google-gmail": "googleapis.com:gmail",
        "google-drive": "googleapis.com:drive",
        "google-calendar": "googleapis.com:calendar",
    }

    def __init__(self, cache_dir: Path | None = None):
        """
        Initialize the spec fetcher.

        Args:
            cache_dir: Directory for caching specs (optional)
        """
        self.cache_dir = cache_dir
        self._apis_guru_index: dict[str, Any] | None = None

    async def fetch_spec(self, provider: str) -> dict:
        """
        Fetch spec with fallback strategy.

        1. Try first-party if available
        2. Fall back to APIs.guru
        3. Raise if not found

        Args:
            provider: Provider name (e.g., "slack", "github")

        Returns:
            OpenAPI spec as dictionary

        Raises:
            ValueError: If provider not found
        """
        # Resolve aliases
        provider = self.PROVIDER_ALIASES.get(provider.lower(), provider.lower())

        # Check cache first
        cached = self._get_cached(provider)
        if cached:
            return cached

        # Try first-party
        if provider in self.FIRST_PARTY_SPECS:
            spec = await self._fetch_url(self.FIRST_PARTY_SPECS[provider])
            self._cache_spec(provider, spec)
            return spec

        # Try APIs.guru
        spec = await self.fetch_from_apis_guru(provider)
        if spec:
            self._cache_spec(provider, spec)
            return spec

        raise ValueError(f"No OpenAPI spec found for provider: {provider}")

    async def fetch_from_apis_guru(self, provider: str) -> dict | None:
        """
        Fetch spec from APIs.guru directory.

        Args:
            provider: Provider name

        Returns:
            OpenAPI spec or None if not found
        """
        # Load index if needed
        if self._apis_guru_index is None:
            self._apis_guru_index = await self._fetch_apis_guru_index()

        # Find provider in index
        provider_data = self._apis_guru_index.get(provider)
        if not provider_data:
            # Try partial match
            for key in self._apis_guru_index:
                if provider in key.lower() or key.lower() in provider:
                    provider_data = self._apis_guru_index[key]
                    break

        if not provider_data:
            return None

        # Get preferred version
        versions = provider_data.get("versions", {})
        if not versions:
            return None

        preferred = provider_data.get("preferred", "")
        version_data = versions.get(preferred) or next(iter(versions.values()))

        spec_url = version_data.get("swaggerUrl") or version_data.get("openapiVer")
        if not spec_url:
            return None

        return await self._fetch_url(spec_url)

    async def fetch_first_party(self, provider: str) -> dict | None:
        """
        Fetch from provider's official spec.

        Args:
            provider: Provider name

        Returns:
            OpenAPI spec or None if no first-party spec available
        """
        provider = provider.lower()
        if provider not in self.FIRST_PARTY_SPECS:
            return None

        return await self._fetch_url(self.FIRST_PARTY_SPECS[provider])

    async def list_available(self) -> list[ProviderInfo]:
        """
        List all available providers from APIs.guru.

        Returns:
            List of provider information
        """
        if self._apis_guru_index is None:
            self._apis_guru_index = await self._fetch_apis_guru_index()

        providers = []
        for name, data in self._apis_guru_index.items():
            preferred = data.get("preferred", "")
            version_data = data.get("versions", {}).get(preferred, {})

            info = version_data.get("info", {})
            providers.append(ProviderInfo(
                name=name,
                title=info.get("title", ""),
                description=info.get("description", "")[:200] if info.get("description") else "",
                version=preferred,
                logo_url=info.get("x-logo", {}).get("url", ""),
                docs_url=info.get("x-origin", [{}])[0].get("url", "") if info.get("x-origin") else "",
                categories=info.get("x-categories", []),
            ))

        return sorted(providers, key=lambda p: p.name)

    async def search(self, query: str) -> list[ProviderInfo]:
        """
        Search for providers by name or description.

        Args:
            query: Search query

        Returns:
            Matching providers
        """
        all_providers = await self.list_available()
        query = query.lower()

        matches = []
        for provider in all_providers:
            if (
                query in provider.name.lower()
                or query in provider.title.lower()
                or query in provider.description.lower()
            ):
                matches.append(provider)

        return matches

    async def get_provider_info(self, provider: str) -> ProviderInfo | None:
        """
        Get detailed info about a provider.

        Args:
            provider: Provider name

        Returns:
            ProviderInfo or None if not found
        """
        provider = self.PROVIDER_ALIASES.get(provider.lower(), provider.lower())

        # Check first-party
        if provider in self.FIRST_PARTY_SPECS:
            return ProviderInfo(
                name=provider,
                title=provider.title(),
                spec_url=self.FIRST_PARTY_SPECS[provider],
            )

        # Check APIs.guru
        if self._apis_guru_index is None:
            self._apis_guru_index = await self._fetch_apis_guru_index()

        data = self._apis_guru_index.get(provider)
        if not data:
            return None

        preferred = data.get("preferred", "")
        version_data = data.get("versions", {}).get(preferred, {})
        info = version_data.get("info", {})

        return ProviderInfo(
            name=provider,
            title=info.get("title", ""),
            description=info.get("description", ""),
            version=preferred,
            logo_url=info.get("x-logo", {}).get("url", ""),
            spec_url=version_data.get("swaggerUrl", ""),
            categories=info.get("x-categories", []),
        )

    async def _fetch_apis_guru_index(self) -> dict[str, Any]:
        """Fetch the APIs.guru provider index."""
        async with httpx.AsyncClient() as client:
            response = await client.get(self.APIS_GURU_LIST_URL, timeout=30.0)
            response.raise_for_status()
            return response.json()

    async def _fetch_url(self, url: str) -> dict:
        """Fetch spec from URL."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0, follow_redirects=True)
            response.raise_for_status()

            content = response.text
            # Try JSON first, then YAML
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return yaml.safe_load(content)

    def _get_cached(self, provider: str) -> dict | None:
        """Get cached spec if available."""
        if not self.cache_dir:
            return None

        cache_file = self.cache_dir / f"{provider}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def _cache_spec(self, provider: str, spec: dict) -> None:
        """Cache a spec to disk."""
        if not self.cache_dir:
            return

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = self.cache_dir / f"{provider}.json"
        cache_file.write_text(json.dumps(spec, indent=2))
