"""Auth management commands."""

from __future__ import annotations

import getpass
import sys

from ..auth import list_configured_providers, remove_api_key, set_api_key


def auth_set(provider: str, api_key: str | None = None, local: bool = False) -> None:
    """Set API key for a provider."""
    if api_key is None:
        # Prompt for key
        api_key = getpass.getpass(f"Enter API key for {provider}: ")
        if not api_key:
            print("No API key provided", file=sys.stderr)
            sys.exit(1)

    path = set_api_key(provider, api_key, local=local)
    scope = "project" if local else "global"
    print(f"Saved {provider} API key to {scope} config ({path})")


def auth_show() -> None:
    """Show configured providers."""
    providers = list_configured_providers()

    if not providers:
        print("No API keys configured")
        print("\nSet keys with: innerloop auth set <provider>")
        return

    print("Configured providers:")
    for p in providers:
        provider = p["provider"]
        source = p["source"]
        preview = p["key_preview"]
        print(f"  {provider:<15} {preview:<20} ({source})")


def auth_remove(provider: str, local: bool = False) -> None:
    """Remove API key for a provider."""
    if remove_api_key(provider, local=local):
        scope = "project" if local else "global"
        print(f"Removed {provider} API key from {scope} config")
    else:
        print(f"No API key found for {provider}", file=sys.stderr)
        sys.exit(1)


__all__ = ["auth_set", "auth_show", "auth_remove"]
