"""
Spec Registry - Index of available OpenAPI specs.

Maintains a registry of known providers and their spec sources.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml


class ProviderTier(str, Enum):
    """Provider quality tiers."""
    TIER1 = "tier1"  # Curated, production-ready
    TIER2 = "tier2"  # Auto-generated + reviewed
    TIER3 = "tier3"  # Fully automated


@dataclass
class ProviderEntry:
    """Entry in the provider registry."""
    name: str
    display_name: str = ""
    tier: ProviderTier = ProviderTier.TIER3
    spec_source: str = "apis_guru"  # apis_guru, first_party, custom
    spec_url: str = ""
    auth_type: str = ""
    base_url: str = ""
    notes: list[str] = field(default_factory=list)
    enabled: bool = True


# Default tier 1 providers
DEFAULT_TIER1_PROVIDERS = [
    ProviderEntry(
        name="slack",
        display_name="Slack",
        tier=ProviderTier.TIER1,
        spec_source="first_party",
        auth_type="oauth2",
        base_url="https://slack.com/api",
    ),
    ProviderEntry(
        name="github",
        display_name="GitHub",
        tier=ProviderTier.TIER1,
        spec_source="first_party",
        auth_type="bearer",
        base_url="https://api.github.com",
    ),
    ProviderEntry(
        name="notion",
        display_name="Notion",
        tier=ProviderTier.TIER1,
        spec_source="apis_guru",
        auth_type="bearer",
        base_url="https://api.notion.com",
    ),
    ProviderEntry(
        name="stripe",
        display_name="Stripe",
        tier=ProviderTier.TIER1,
        spec_source="first_party",
        auth_type="api_key",
        base_url="https://api.stripe.com",
    ),
    ProviderEntry(
        name="airtable",
        display_name="Airtable",
        tier=ProviderTier.TIER1,
        spec_source="apis_guru",
        auth_type="bearer",
        base_url="https://api.airtable.com",
    ),
    ProviderEntry(
        name="hubspot",
        display_name="HubSpot",
        tier=ProviderTier.TIER1,
        spec_source="apis_guru",
        auth_type="oauth2",
        base_url="https://api.hubapi.com",
    ),
    ProviderEntry(
        name="trello",
        display_name="Trello",
        tier=ProviderTier.TIER1,
        spec_source="apis_guru",
        auth_type="api_key",
        base_url="https://api.trello.com",
    ),
    ProviderEntry(
        name="discord",
        display_name="Discord",
        tier=ProviderTier.TIER1,
        spec_source="apis_guru",
        auth_type="bearer",
        base_url="https://discord.com/api",
    ),
]

DEFAULT_TIER2_PROVIDERS = [
    ProviderEntry(name="asana", display_name="Asana", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="linear", display_name="Linear", tier=ProviderTier.TIER2, auth_type="api_key"),
    ProviderEntry(name="jira", display_name="Jira", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="zendesk", display_name="Zendesk", tier=ProviderTier.TIER2, auth_type="api_key"),
    ProviderEntry(name="intercom", display_name="Intercom", tier=ProviderTier.TIER2, auth_type="bearer"),
    ProviderEntry(name="mailchimp", display_name="Mailchimp", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="sendgrid", display_name="SendGrid", tier=ProviderTier.TIER2, auth_type="api_key"),
    ProviderEntry(name="twilio", display_name="Twilio", tier=ProviderTier.TIER2, auth_type="basic"),
    ProviderEntry(name="shopify", display_name="Shopify", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="zoom", display_name="Zoom", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="calendly", display_name="Calendly", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="typeform", display_name="Typeform", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="monday", display_name="Monday.com", tier=ProviderTier.TIER2, auth_type="api_key"),
    ProviderEntry(name="clickup", display_name="ClickUp", tier=ProviderTier.TIER2, auth_type="api_key"),
    ProviderEntry(name="figma", display_name="Figma", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="dropbox", display_name="Dropbox", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="box", display_name="Box", tier=ProviderTier.TIER2, auth_type="oauth2"),
    ProviderEntry(name="salesforce", display_name="Salesforce", tier=ProviderTier.TIER2, auth_type="oauth2"),
]


class SpecRegistry:
    """Registry of known providers and their specs."""

    def __init__(self, registry_file: Path | None = None):
        """
        Initialize the spec registry.

        Args:
            registry_file: Optional YAML file with custom registry entries
        """
        self.registry_file = registry_file
        self._providers: dict[str, ProviderEntry] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        """Ensure registry is loaded."""
        if not self._loaded:
            self._load_defaults()
            if self.registry_file and self.registry_file.exists():
                self._load_from_file()
            self._loaded = True

    def _load_defaults(self) -> None:
        """Load default provider entries."""
        for entry in DEFAULT_TIER1_PROVIDERS + DEFAULT_TIER2_PROVIDERS:
            self._providers[entry.name] = entry

    def _load_from_file(self) -> None:
        """Load custom entries from registry file."""
        with open(self.registry_file) as f:
            data = yaml.safe_load(f) or {}

        for name, entry_data in data.get("providers", {}).items():
            entry = ProviderEntry(
                name=name,
                display_name=entry_data.get("display_name", name.title()),
                tier=ProviderTier(entry_data.get("tier", "tier3")),
                spec_source=entry_data.get("spec_source", "apis_guru"),
                spec_url=entry_data.get("spec_url", ""),
                auth_type=entry_data.get("auth_type", ""),
                base_url=entry_data.get("base_url", ""),
                notes=entry_data.get("notes", []),
                enabled=entry_data.get("enabled", True),
            )
            self._providers[name] = entry

    def get(self, provider: str) -> ProviderEntry | None:
        """Get a provider entry."""
        self._ensure_loaded()
        return self._providers.get(provider.lower())

    def list_all(self) -> list[ProviderEntry]:
        """List all registered providers."""
        self._ensure_loaded()
        return sorted(self._providers.values(), key=lambda e: e.name)

    def list_by_tier(self, tier: ProviderTier) -> list[ProviderEntry]:
        """List providers by tier."""
        self._ensure_loaded()
        return [e for e in self._providers.values() if e.tier == tier and e.enabled]

    def list_enabled(self) -> list[ProviderEntry]:
        """List all enabled providers."""
        self._ensure_loaded()
        return [e for e in self._providers.values() if e.enabled]

    def register(self, entry: ProviderEntry) -> None:
        """Register a new provider."""
        self._ensure_loaded()
        self._providers[entry.name] = entry

    def has_provider(self, provider: str) -> bool:
        """Check if provider is registered."""
        self._ensure_loaded()
        return provider.lower() in self._providers

    def save(self) -> None:
        """Save registry to file."""
        if not self.registry_file:
            raise ValueError("No registry file configured")

        data: dict[str, Any] = {"providers": {}}
        for name, entry in self._providers.items():
            data["providers"][name] = {
                "display_name": entry.display_name,
                "tier": entry.tier.value,
                "spec_source": entry.spec_source,
                "spec_url": entry.spec_url,
                "auth_type": entry.auth_type,
                "base_url": entry.base_url,
                "notes": entry.notes,
                "enabled": entry.enabled,
            }

        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
