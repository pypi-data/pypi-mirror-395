"""Models listing commands."""

from __future__ import annotations

from ..config import load_config
from ..registry import Model, get_registry


def list_models(
    show_aliases: bool = False,
    provider_filter: str | None = None,
) -> None:
    """List available models."""
    config = load_config()
    registry = get_registry()

    if show_aliases:
        print("Aliases:")
        for alias, target in sorted(config.aliases.items()):
            print(f"  {alias:<15} -> {target}")
        return

    # Get models from registry
    if provider_filter:
        models = registry.list_models(provider=provider_filter)
        if not models:
            print(f"Unknown provider: {provider_filter}")
            print(f"Known providers: {', '.join(registry.list_providers())}")
            return
    else:
        models = registry.list_models()

    # Group by provider
    by_provider: dict[str, list[Model]] = {}
    for m in models:
        by_provider.setdefault(m.provider, []).append(m)

    print("Available models:")
    for provider in sorted(by_provider.keys()):
        print(f"\n  {provider}:")
        for m in by_provider[provider]:
            ctx = f" ({m.context_window // 1000}k)" if m.context_window else ""
            print(f"    {m.full_id}{ctx}")

    # Show custom providers from config
    if config.providers:
        print("\n  Custom providers:")
        for name, pconfig in config.providers.items():
            print(f"    {name}/ (base: {pconfig.base_url})")

    # Show aliases
    print("\nAliases:")
    for alias, target in sorted(config.aliases.items()):
        print(f"  {alias:<15} -> {target}")


__all__ = ["list_models"]
