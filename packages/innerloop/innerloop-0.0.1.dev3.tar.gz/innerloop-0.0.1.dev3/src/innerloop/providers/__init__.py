"""
Provider implementations.

Each provider translates between InnerLoop's unified types and
provider-specific API formats.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import Provider

if TYPE_CHECKING:
    pass

# Provider registry - populated as providers are imported
_PROVIDERS: dict[str, type[Provider]] = {}


def register_provider(name: str, provider_class: type[Provider]) -> None:
    """Register a provider class."""
    _PROVIDERS[name] = provider_class


def get_provider(
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
) -> Provider:
    """
    Get a provider instance for a model string.

    Args:
        model: Full model string (e.g., "anthropic/claude-sonnet-4")
        api_key: Optional explicit API key
        base_url: Optional base URL override (for local models)

    Returns:
        Provider instance configured for the model
    """
    from ..auth import get_provider_from_model, resolve_api_key

    provider_name, model_id = get_provider_from_model(model)

    # Lazy import providers to avoid loading all SDKs
    if provider_name not in _PROVIDERS:
        _load_provider(provider_name)

    if provider_name not in _PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_name!r}")

    provider_class = _PROVIDERS[provider_name]
    key = resolve_api_key(provider_name, api_key)

    # Set default base URLs for known providers
    if base_url is None:
        base_url = _get_default_base_url(provider_name)

    return provider_class(model_id=model_id, api_key=key, base_url=base_url)


def _get_default_base_url(provider_name: str) -> str | None:
    """Get default base URL for known providers."""
    base_urls = {
        "openrouter": "https://openrouter.ai/api/v1",
        "ollama": "http://localhost:11434/v1",
        "lmstudio": "http://localhost:1234/v1",
    }
    return base_urls.get(provider_name)


def _load_provider(name: str) -> None:
    """Lazy-load a provider module."""
    if name == "anthropic":
        from . import anthropic  # noqa: F401
    elif name in ("openai", "openrouter", "ollama", "lmstudio"):
        # All use OpenAI-compatible provider
        from . import openai  # noqa: F401
    # Unknown providers stay unregistered


__all__ = [
    "Provider",
    "get_provider",
    "register_provider",
]
