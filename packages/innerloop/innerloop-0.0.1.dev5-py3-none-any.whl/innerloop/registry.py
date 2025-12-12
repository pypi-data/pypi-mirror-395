"""
Model Registry

Hybrid registry combining genai-prices data with curated model overrides.
Provides model lookup, alias resolution, and lazy local discovery.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any
from urllib.request import urlopen

if TYPE_CHECKING:
    from genai_prices.types import ModelInfo

# =============================================================================
# Data Types
# =============================================================================


@dataclass
class Model:
    """Resolved model with metadata."""

    id: str  # Canonical ID (e.g., "claude-sonnet-4-5")
    provider: str  # Provider ID (e.g., "anthropic")
    name: str  # Human-friendly name
    context_window: int | None = None
    input_price_mtok: float | None = None  # Per million tokens
    output_price_mtok: float | None = None
    description: str | None = None
    is_local: bool = False

    @property
    def full_id(self) -> str:
        """Full model ID with provider prefix."""
        return f"{self.provider}/{self.id}"


@dataclass
class Registry:
    """Hybrid model registry."""

    _models: dict[str, Model] = field(default_factory=dict)
    _providers: set[str] = field(default_factory=set)
    _local_checked: set[str] = field(default_factory=set)

    def get(self, model_id: str) -> Model | None:
        """Get model by full ID (provider/model)."""
        return self._models.get(model_id)

    def find(self, query: str) -> Model | None:
        """
        Find model by query string.

        Supports:
        - Full ID: "anthropic/claude-sonnet-4-5"
        - Model ID only: "claude-sonnet-4-5" (matches first provider)
        - Prefix match: "claude-sonnet" matches "claude-sonnet-4-5"

        Note: Does NOT perform network I/O. Call discover_local() explicitly
        to detect local models (LM Studio, Ollama) before using find().
        """
        # Exact match
        if query in self._models:
            return self._models[query]

        # Model ID without provider prefix
        for model in self._models.values():
            if model.id == query:
                return model

        # Prefix match
        for model in self._models.values():
            if model.id.startswith(query):
                return model

        return None

    def discover_local(self, provider: str | None = None) -> list[Model]:
        """
        Discover local models (LM Studio, Ollama).

        This performs network I/O to localhost ports. Call explicitly when
        you want to detect local models.

        Args:
            provider: Specific provider to discover ("lmstudio" or "ollama").
                     If None, discovers all local providers.

        Returns:
            List of newly discovered models.
        """
        before = set(self._models.keys())

        if provider is None:
            self._discover_local("lmstudio")
            self._discover_local("ollama")
        elif provider in ("lmstudio", "ollama"):
            self._discover_local(provider)

        after = set(self._models.keys())
        new_ids = after - before
        return [self._models[mid] for mid in new_ids]

    def list_models(self, provider: str | None = None) -> list[Model]:
        """List all models, optionally filtered by provider."""
        models = list(self._models.values())
        if provider:
            models = [m for m in models if m.provider == provider]
        return sorted(models, key=lambda m: (m.provider, m.id))

    def list_providers(self) -> list[str]:
        """List all known providers."""
        return sorted(self._providers)

    def add(self, model: Model) -> None:
        """Add or override a model."""
        self._models[model.full_id] = model
        self._providers.add(model.provider)

    def _discover_local(self, provider: str) -> None:
        """Lazy discovery of local models (LM Studio/Ollama)."""
        self._local_checked.add(provider)

        if provider == "lmstudio":
            self._discover_lmstudio()
        elif provider == "ollama":
            self._discover_ollama()

    def _discover_lmstudio(self) -> None:
        """Discover LM Studio models on localhost:1234."""
        if not _check_port(1234):
            return

        try:
            import json

            with urlopen("http://localhost:1234/v1/models", timeout=0.5) as resp:
                data = json.loads(resp.read())
                for item in data.get("data", []):
                    model_id = item.get("id", "unknown")
                    self.add(
                        Model(
                            id=model_id,
                            provider="lmstudio",
                            name=model_id,
                            is_local=True,
                        )
                    )
        except Exception:
            pass

    def _discover_ollama(self) -> None:
        """Discover Ollama models on localhost:11434."""
        if not _check_port(11434):
            return

        try:
            import json

            with urlopen("http://localhost:11434/api/tags", timeout=0.5) as resp:
                data = json.loads(resp.read())
                for item in data.get("models", []):
                    model_name = item.get("name", "unknown")
                    self.add(
                        Model(
                            id=model_name,
                            provider="ollama",
                            name=model_name,
                            is_local=True,
                        )
                    )
        except Exception:
            pass


def _check_port(port: int, host: str = "localhost", timeout: float = 0.05) -> bool:
    """Quick check if a port is open."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, TimeoutError):
        return False


# =============================================================================
# Modern Model Manifest (Overrides)
# =============================================================================

# These models are injected on top of genai-prices to ensure bleeding-edge
# models are always available, even if the genai-prices snapshot is stale.

MODERN_MODELS: list[dict[str, Any]] = [
    # Anthropic - Claude 4.5 family
    {
        "id": "claude-opus-4-5",
        "provider": "anthropic",
        "name": "Claude Opus 4.5",
        "context_window": 200000,
        "description": "Most intelligent Claude model",
    },
    {
        "id": "claude-sonnet-4-5",
        "provider": "anthropic",
        "name": "Claude Sonnet 4.5",
        "context_window": 1000000,
        "description": "Balanced intelligence and speed",
    },
    {
        "id": "claude-haiku-4-5",
        "provider": "anthropic",
        "name": "Claude Haiku 4.5",
        "context_window": 200000,
        "description": "Fastest Claude model",
    },
    # OpenAI - GPT-5 family
    {
        "id": "gpt-5.1",
        "provider": "openai",
        "name": "GPT-5.1",
        "context_window": 400000,
        "description": "Latest GPT-5 iteration",
    },
    {
        "id": "gpt-5",
        "provider": "openai",
        "name": "GPT-5",
        "context_window": 400000,
        "description": "Standard GPT-5",
    },
    {
        "id": "gpt-5-mini",
        "provider": "openai",
        "name": "GPT-5 Mini",
        "context_window": 400000,
        "description": "Cost-effective GPT-5",
    },
    {
        "id": "gpt-5-nano",
        "provider": "openai",
        "name": "GPT-5 Nano",
        "context_window": 400000,
        "description": "Ultra-lightweight GPT-5",
    },
    {
        "id": "o3",
        "provider": "openai",
        "name": "o3",
        "context_window": 200000,
        "description": "Advanced reasoning model",
    },
    {
        "id": "o4-mini",
        "provider": "openai",
        "name": "o4-mini",
        "context_window": 200000,
        "description": "Fast reasoning model",
    },
    # Google - Gemini 2.5+ family
    {
        "id": "gemini-2.5-pro",
        "provider": "google",
        "name": "Gemini 2.5 Pro",
        "context_window": 1000000,
        "description": "Latest Gemini Pro",
    },
    {
        "id": "gemini-2.5-flash",
        "provider": "google",
        "name": "Gemini 2.5 Flash",
        "context_window": 1000000,
        "description": "Fast Gemini model",
    },
    # Cerebras - Fast inference
    {
        "id": "gpt-oss-120b",
        "provider": "cerebras",
        "name": "GPT-OSS 120B",
        "context_window": 131072,
        "description": "Open-source GPT on Cerebras",
    },
    {
        "id": "llama-3.3-70b",
        "provider": "cerebras",
        "name": "Llama 3.3 70B",
        "context_window": 128000,
        "description": "Llama on Cerebras inference",
    },
    # Groq - Fast inference
    {
        "id": "llama-3.3-70b-versatile",
        "provider": "groq",
        "name": "Llama 3.3 70B Versatile",
        "context_window": 131072,
        "description": "Llama on Groq inference",
    },
    {
        "id": "qwen3-32b",
        "provider": "groq",
        "name": "Qwen3 32B",
        "context_window": 131072,
        "description": "Qwen3 on Groq inference",
    },
    # OpenRouter - Free tier
    {
        "id": "z-ai/glm-4.5-air:free",
        "provider": "openrouter",
        "name": "GLM-4.5 Air (Free)",
        "context_window": 64000,
        "description": "Free model via OpenRouter",
    },
    {
        "id": "deepseek/deepseek-r1:free",
        "provider": "openrouter",
        "name": "DeepSeek R1 (Free)",
        "context_window": 64000,
        "description": "Free reasoning model via OpenRouter",
    },
]

# =============================================================================
# Curated Aliases
# =============================================================================

# ~10 alias-worthy shortcuts that always point to the latest version
# These are resolved at lookup time, not hardcoded to specific versions

ALIASES: dict[str, str] = {
    # Anthropic - always latest Claude
    "opus": "anthropic/claude-opus-4-5",
    "sonnet": "anthropic/claude-sonnet-4-5",
    "haiku": "anthropic/claude-haiku-4-5",
    # OpenAI - always latest GPT
    "gpt5": "openai/gpt-5.1",
    "gpt": "openai/gpt-5.1",
    # Google - Gemini shortcuts
    "gemini-pro": "google/gemini-2.5-pro",
    "gemini-flash": "google/gemini-2.5-flash",
    "flash": "google/gemini-2.5-flash",
    # Fast inference
    "cerebras": "cerebras/gpt-oss-120b",
    "groq": "groq/llama-3.3-70b-versatile",
    # Free option
    "free": "openrouter/z-ai/glm-4.5-air:free",
}


# =============================================================================
# Registry Builder
# =============================================================================


def _model_from_genai(provider_id: str, model: ModelInfo) -> Model:
    """Convert genai-prices ModelInfo to our Model type."""
    # Extract prices if available - prices can be Decimal, TieredPrices, or other
    input_price: float | None = None
    output_price: float | None = None
    if hasattr(model, "prices") and model.prices:
        prices: Any = model.prices
        if hasattr(prices, "input_mtok") and prices.input_mtok is not None:
            try:
                input_price = float(str(prices.input_mtok))
            except (TypeError, ValueError):
                pass
        if hasattr(prices, "output_mtok") and prices.output_mtok is not None:
            try:
                output_price = float(str(prices.output_mtok))
            except (TypeError, ValueError):
                pass

    return Model(
        id=model.id,
        provider=provider_id,
        name=getattr(model, "name", model.id),
        context_window=getattr(model, "context_window", None),
        input_price_mtok=input_price,
        output_price_mtok=output_price,
        description=getattr(model, "description", None),
    )


def build_registry(include_all_genai: bool = False) -> Registry:
    """
    Build the hybrid model registry.

    Args:
        include_all_genai: If True, include all models from genai-prices.
                          If False (default), only include curated models.

    Returns:
        Populated Registry instance.
    """
    registry = Registry()

    # Step 1: Optionally load from genai-prices
    if include_all_genai:
        try:
            from genai_prices.data_snapshot import get_snapshot

            snapshot = get_snapshot()
            for provider in snapshot.providers:
                for model in provider.models:
                    registry.add(_model_from_genai(provider.id, model))
        except ImportError:
            pass  # genai-prices not installed

    # Step 2: Inject modern models (overrides stale genai-prices entries)
    for spec in MODERN_MODELS:
        registry.add(
            Model(
                id=spec["id"],
                provider=spec["provider"],
                name=spec["name"],
                context_window=spec.get("context_window"),
                description=spec.get("description"),
            )
        )

    return registry


def resolve_alias(model: str) -> str:
    """
    Resolve a model alias to its full model ID.

    Args:
        model: Model string or alias

    Returns:
        Resolved full model ID (provider/model)
    """
    return ALIASES.get(model, model)


# =============================================================================
# Module-level singleton
# =============================================================================

_registry: Registry | None = None


def get_registry() -> Registry:
    """Get the global registry instance (lazy initialization)."""
    global _registry
    if _registry is None:
        _registry = build_registry()
    return _registry


def reset_registry() -> None:
    """Reset the global registry (useful for testing)."""
    global _registry
    _registry = None


__all__ = [
    "Model",
    "Registry",
    "ALIASES",
    "MODERN_MODELS",
    "build_registry",
    "get_registry",
    "reset_registry",
    "resolve_alias",
]
