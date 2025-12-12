"""
Provider implementations.

Each provider translates between InnerLoop's unified types and
provider-specific API formats.
"""

from __future__ import annotations

import os

from .base import Provider

# Provider registry - populated as providers are imported
_PROVIDERS: dict[str, type[Provider]] = {}

# Default base URLs for known providers
_DEFAULT_BASE_URLS: dict[str, str] = {
    "openrouter": "https://openrouter.ai/api/v1",
    "ollama": "http://localhost:11434/v1",
    "lmstudio": "http://localhost:1234/v1",
    "cerebras": "https://api.cerebras.ai/v1",
    "groq": "https://api.groq.com/openai/v1",
}

# Environment variable names for each provider's API key
_API_KEY_ENV_VARS: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "groq": "GROQ_API_KEY",
    "cerebras": "CEREBRAS_API_KEY",
    # ollama and lmstudio don't need API keys (local)
}


def register_provider(name: str, provider_class: type[Provider]) -> None:
    """Register a provider class."""
    _PROVIDERS[name] = provider_class


def _resolve_api_key(
    provider_name: str, explicit_key: str | None
) -> str | None:
    """
    Resolve API key for a provider.

    Priority: explicit key > provider-specific env var

    Args:
        provider_name: The provider name (e.g., "openrouter", "groq")
        explicit_key: Explicitly provided API key, if any

    Returns:
        The resolved API key, or None if not found (some providers don't need one)
    """
    if explicit_key is not None:
        return explicit_key

    env_var = _API_KEY_ENV_VARS.get(provider_name)
    if env_var:
        return os.environ.get(env_var)

    return None


def _parse_model_string(model: str) -> tuple[str, str]:
    """
    Parse model string into provider and model_id.

    Examples:
        "anthropic/claude-sonnet-4" -> ("anthropic", "claude-sonnet-4")
        "openrouter/meta-llama/llama-3" -> ("openrouter", "meta-llama/llama-3")
        "ollama/llama3" -> ("ollama", "llama3")
    """
    if "/" not in model:
        raise ValueError(
            f"Invalid model string: {model!r}. "
            f"Expected format: 'provider/model-id' (e.g., 'anthropic/claude-sonnet-4')"
        )

    parts = model.split("/", 1)
    provider_name = parts[0].lower()
    model_id = parts[1]

    return provider_name, model_id


def get_provider(
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
) -> Provider:
    """
    Get a provider instance for a model string.

    Args:
        model: Full model string (e.g., "anthropic/claude-sonnet-4")
        api_key: Optional explicit API key (uses env var if not provided)
        base_url: Optional base URL override (for local models)

    Returns:
        Provider instance configured for the model
    """
    provider_name, model_id = _parse_model_string(model)

    # Lazy import providers to avoid loading all SDKs
    if provider_name not in _PROVIDERS:
        _load_provider(provider_name)

    if provider_name not in _PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_name!r}")

    provider_class = _PROVIDERS[provider_name]

    # Resolve API key: explicit > provider-specific env var
    resolved_key = _resolve_api_key(provider_name, api_key)

    # Resolve base URL: explicit > default
    if base_url is None:
        base_url = _DEFAULT_BASE_URLS.get(provider_name)

    return provider_class(
        model_id=model_id, api_key=resolved_key, base_url=base_url
    )


def _load_provider(name: str) -> None:
    """Lazy-load a provider module."""
    if name == "anthropic":
        from . import anthropic  # noqa: F401
    elif name in (
        "openai",
        "openrouter",
        "ollama",
        "lmstudio",
        "cerebras",
        "groq",
    ):
        # All use OpenAI-compatible provider
        from . import openai  # noqa: F401
    elif name == "google":
        from . import google  # noqa: F401
    # Unknown providers stay unregistered


__all__ = [
    "Provider",
    "get_provider",
    "register_provider",
]
