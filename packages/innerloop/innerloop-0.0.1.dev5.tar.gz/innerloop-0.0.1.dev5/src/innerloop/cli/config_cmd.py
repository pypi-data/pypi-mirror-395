"""Config management commands."""

from __future__ import annotations

import json
from typing import Any

from ..config import (
    get_config_dir,
    get_project_config_dir,
    init_project,
    load_config,
    save_config,
)


def show_config() -> None:
    """Show effective configuration."""
    config = load_config()

    print("Effective configuration:")
    print()

    # Show as formatted JSON
    config_dict = config.model_dump()
    print(json.dumps(config_dict, indent=2))

    print()
    print("Config locations:")
    print(f"  Global: {get_config_dir() / 'config.json'}")
    if project_dir := get_project_config_dir():
        print(f"  Project: {project_dir / 'config.json'}")


def set_config(key: str, value: str, local: bool = False) -> None:
    """Set a configuration value."""
    # Parse the key path (e.g., "defaults.temperature" or "default_model")
    parts = key.split(".")

    # Try to parse value as JSON for complex types
    try:
        parsed_value = json.loads(value)
    except json.JSONDecodeError:
        # Treat as string
        parsed_value = value

    # Build nested dict
    config_data: dict[str, Any] = {}
    current: dict[str, Any] = config_data
    for part in parts[:-1]:
        current[part] = {}
        current = current[part]
    current[parts[-1]] = parsed_value

    path = save_config(config_data, local=local)
    scope = "project" if local else "global"
    print(f"Set {key}={value} in {scope} config ({path})")


def init_command() -> None:
    """Initialize project-local configuration."""
    project_dir = init_project()
    print(f"Initialized InnerLoop config in {project_dir}/")
    print()
    print("Created:")
    print("  config.json  - Project configuration")
    print("  auth.json    - API keys (git-ignored)")
    print("  .gitignore   - Prevents auth.json from being committed")


__all__ = ["show_config", "set_config", "init_command"]
