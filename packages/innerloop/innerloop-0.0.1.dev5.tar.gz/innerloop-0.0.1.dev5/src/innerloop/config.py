"""
Configuration Management

Layered JSON configuration with XDG directory support.
Priority: CLI args > env vars > project config > global config > defaults
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, cast

from pydantic import BaseModel, Field

# =============================================================================
# XDG Directory Helpers
# =============================================================================


def get_config_dir() -> Path:
    """Get configuration directory (XDG_CONFIG_HOME/innerloop)."""
    if env_dir := os.environ.get("INNERLOOP_CONFIG_DIR"):
        return Path(env_dir)
    xdg_config = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    return Path(xdg_config) / "innerloop"


def get_data_dir() -> Path:
    """Get data directory (XDG_DATA_HOME/innerloop)."""
    if env_dir := os.environ.get("INNERLOOP_DATA_DIR"):
        return Path(env_dir)
    xdg_data = os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
    return Path(xdg_data) / "innerloop"


def get_session_dir() -> Path:
    """Get session storage directory."""
    if env_dir := os.environ.get("INNERLOOP_SESSION_DIR"):
        return Path(env_dir)
    return get_data_dir() / "sessions"


def get_project_config_dir() -> Path | None:
    """Get project-local config directory (.innerloop/) if it exists."""
    project_dir = Path.cwd() / ".innerloop"
    if project_dir.is_dir():
        return project_dir
    return None


# =============================================================================
# Configuration Schema
# =============================================================================


class ProviderConfig(BaseModel):
    """Custom provider configuration."""

    type: str = "openai-compatible"
    base_url: str


class DefaultsConfig(BaseModel):
    """Default execution parameters."""

    temperature: float | None = None
    max_tokens: int | None = None  # Let provider APIs use their defaults
    timeout: float = 120.0
    thinking: str = "off"


class ToolsConfig(BaseModel):
    """Tool configuration."""

    zone: str = "file_only"


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = "WARNING"
    events: bool = False


class Config(BaseModel):
    """InnerLoop configuration."""

    default_model: str | None = None
    aliases: dict[str, str] = Field(default_factory=dict)
    providers: dict[str, ProviderConfig] = Field(default_factory=dict)
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)
    tools: ToolsConfig = Field(default_factory=ToolsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


# =============================================================================
# Configuration Loading
# =============================================================================


def _get_default_aliases() -> dict[str, str]:
    """Get default aliases from registry (lazy import to avoid circular deps)."""
    from innerloop.registry import ALIASES

    return dict(ALIASES)


# For backwards compatibility - use _get_default_aliases() for actual values
DEFAULT_ALIASES: dict[str, str] = {}


def _load_json_file(path: Path) -> dict[str, Any]:
    """Load JSON file, returning empty dict if not found or invalid."""
    if not path.exists():
        return {}
    try:
        with path.open() as f:
            data = json.load(f)
            return cast(dict[str, Any], data)
    except (json.JSONDecodeError, OSError):
        return {}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dicts, with override taking precedence."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> Config:
    """
    Load configuration from all sources.

    Priority (highest first):
    1. Environment variables (INNERLOOP_*)
    2. Project config (.innerloop/config.json)
    3. Global config (~/.config/innerloop/config.json)
    4. Defaults
    """
    # Start with empty config
    merged: dict[str, Any] = {}

    # Load global config
    global_path = get_config_dir() / "config.json"
    global_config = _load_json_file(global_path)
    merged = _deep_merge(merged, global_config)

    # Load project config (overrides global)
    if project_dir := get_project_config_dir():
        project_path = project_dir / "config.json"
        project_config = _load_json_file(project_path)
        merged = _deep_merge(merged, project_config)

    # Environment variable overrides
    if env_model := os.environ.get("INNERLOOP_MODEL"):
        merged["default_model"] = env_model
    if env_default_model := os.environ.get("INNERLOOP_DEFAULT_MODEL"):
        merged["default_model"] = env_default_model

    # Merge default aliases with configured aliases
    aliases = _get_default_aliases()
    aliases.update(merged.get("aliases", {}))
    merged["aliases"] = aliases

    return cast(Config, Config.model_validate(merged))


def resolve_model_alias(model: str, config: Config | None = None) -> str:
    """
    Resolve a model alias to full model string.

    Args:
        model: Model string or alias
        config: Config to use (loads if not provided)

    Returns:
        Resolved model string
    """
    if config is None:
        config = load_config()

    # Check aliases
    if model in config.aliases:
        return config.aliases[model]

    return model


def get_default_model(config: Config | None = None) -> str:
    """
    Get the default model from config.

    Args:
        config: Config to use (loads if not provided)

    Returns:
        Default model string

    Raises:
        ValueError: If no default model configured
    """
    if config is None:
        config = load_config()

    if config.default_model:
        return resolve_model_alias(config.default_model, config)

    # Fallback to free model via OpenRouter
    return "openrouter/z-ai/glm-4.5-air:free"


def get_provider_base_url(provider: str, config: Config | None = None) -> str | None:
    """
    Get base URL for a provider from config.

    Args:
        provider: Provider name
        config: Config to use (loads if not provided)

    Returns:
        Base URL or None if not configured
    """
    if config is None:
        config = load_config()

    if provider in config.providers:
        return config.providers[provider].base_url

    return None


# =============================================================================
# Configuration Writing
# =============================================================================


def save_config(config_data: dict[str, Any], local: bool = False) -> Path:
    """
    Save configuration to file.

    Args:
        config_data: Configuration data to save
        local: If True, save to project config; otherwise global

    Returns:
        Path to saved file
    """
    if local:
        config_dir = Path.cwd() / ".innerloop"
    else:
        config_dir = get_config_dir()

    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"

    # Load existing config and merge
    existing = _load_json_file(config_path)
    merged = _deep_merge(existing, config_data)

    with config_path.open("w") as f:
        json.dump(merged, f, indent=2)
        f.write("\n")

    return config_path


def init_project() -> Path:
    """
    Initialize project-local configuration.

    Creates .innerloop/ directory with config.json, auth.json, and .gitignore.

    Returns:
        Path to created directory
    """
    project_dir = Path.cwd() / ".innerloop"
    project_dir.mkdir(exist_ok=True)

    # Create empty config.json
    config_path = project_dir / "config.json"
    if not config_path.exists():
        config_path.write_text("{}\n")

    # Create empty auth.json
    auth_path = project_dir / "auth.json"
    if not auth_path.exists():
        auth_path.write_text("{}\n")

    # Create .gitignore
    gitignore_path = project_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text("auth.json\n")

    return project_dir


__all__ = [
    # Directory helpers
    "get_config_dir",
    "get_data_dir",
    "get_session_dir",
    "get_project_config_dir",
    # Config types
    "Config",
    "ProviderConfig",
    "DefaultsConfig",
    "ToolsConfig",
    "LoggingConfig",
    # Loading/saving
    "load_config",
    "save_config",
    "init_project",
    # Helpers
    "resolve_model_alias",
    "get_default_model",
    "get_provider_base_url",
    "DEFAULT_ALIASES",
]
