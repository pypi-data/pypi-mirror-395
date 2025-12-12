"""
API Key Resolution

Simple environment variable based auth. No OAuth, no file storage.
Provider SDKs handle their own defaults if we pass None.
"""

from __future__ import annotations

import os

# Provider name -> environment variable
ENV_VARS: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "google": "GOOGLE_API_KEY",
}


def resolve_api_key(
    provider: str,
    explicit_key: str | None = None,
) -> str | None:
    """
    Resolve API key for a provider.

    Priority:
    1. Explicit key passed as argument
    2. Environment variable for provider
    3. None (let SDK use its default lookup)

    Args:
        provider: Provider name (e.g., "anthropic", "openai", "google")
        explicit_key: Optional explicit API key

    Returns:
        API key string or None
    """
    if explicit_key:
        return explicit_key

    env_var = ENV_VARS.get(provider)
    if env_var:
        key = os.environ.get(env_var)
        if key:
            return key

    # Let SDK handle it (may check its own env vars or config)
    return None


def get_provider_from_model(model: str) -> tuple[str, str]:
    """
    Parse model string into provider and model ID.

    Format: "provider/model-name" or "provider/org/model-name"

    Args:
        model: Full model string (e.g., "anthropic/claude-sonnet-4")

    Returns:
        Tuple of (provider_name, model_id)

    Examples:
        "anthropic/claude-sonnet-4" -> ("anthropic", "claude-sonnet-4")
        "openai/gpt-4" -> ("openai", "gpt-4")
        "openrouter/anthropic/claude-3" -> ("openrouter", "anthropic/claude-3")
    """
    parts = model.split("/", 1)
    if len(parts) != 2:
        raise ValueError(
            f"Invalid model format: {model!r}. Expected 'provider/model-name'"
        )
    return parts[0], parts[1]


__all__ = [
    "resolve_api_key",
    "get_provider_from_model",
    "ENV_VARS",
]
