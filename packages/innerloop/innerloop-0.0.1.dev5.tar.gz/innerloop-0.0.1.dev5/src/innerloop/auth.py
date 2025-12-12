"""
API Key Resolution

Layered authentication: explicit > env var > project auth > global auth > SDK default.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

from .config import get_config_dir, get_project_config_dir

# Provider name -> environment variable
ENV_VARS: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "google": "GOOGLE_API_KEY",
    "cerebras": "CEREBRAS_API_KEY",
    "groq": "GROQ_API_KEY",
}


def _load_auth_file(path: Path) -> dict[str, str]:
    """Load auth.json file, returning empty dict if not found or invalid."""
    if not path.exists():
        return {}
    try:
        with path.open() as f:
            data = json.load(f)
            return {k: v for k, v in data.items() if isinstance(v, str)}
    except (json.JSONDecodeError, OSError):
        return {}


def _check_permissions(path: Path) -> bool:
    """
    Check if auth file has secure permissions.

    Returns True if permissions are OK, False if too permissive.
    """
    if not path.exists():
        return True

    # On Unix, check that group/world can't read
    try:
        mode = path.stat().st_mode
        if mode & (stat.S_IRGRP | stat.S_IROTH):
            return False
    except OSError:
        pass

    return True


def get_global_auth_path() -> Path:
    """Get path to global auth.json."""
    return get_config_dir() / "auth.json"


def get_project_auth_path() -> Path | None:
    """Get path to project auth.json if project config exists."""
    if project_dir := get_project_config_dir():
        return project_dir / "auth.json"
    return None


def load_auth(check_permissions: bool = True) -> dict[str, str]:
    """
    Load all authentication from files.

    Args:
        check_permissions: If True, warn about insecure file permissions

    Returns:
        Dict mapping provider names to API keys
    """
    auth: dict[str, str] = {}

    # Load global auth
    global_path = get_global_auth_path()
    if check_permissions and not _check_permissions(global_path):
        import warnings

        warnings.warn(
            f"Auth file {global_path} has insecure permissions. "
            "Run: chmod 600 " + str(global_path),
            stacklevel=2,
        )
    auth.update(_load_auth_file(global_path))

    # Load project auth (overrides global)
    if project_path := get_project_auth_path():
        if check_permissions and not _check_permissions(project_path):
            import warnings

            warnings.warn(
                f"Auth file {project_path} has insecure permissions. "
                "Run: chmod 600 " + str(project_path),
                stacklevel=2,
            )
        auth.update(_load_auth_file(project_path))

    return auth


def resolve_api_key(
    provider: str,
    explicit_key: str | None = None,
) -> str | None:
    """
    Resolve API key for a provider.

    Priority:
    1. Explicit key passed as argument
    2. Environment variable for provider
    3. Project auth.json
    4. Global auth.json
    5. None (let SDK use its default lookup)

    Args:
        provider: Provider name (e.g., "anthropic", "openai", "google")
        explicit_key: Optional explicit API key

    Returns:
        API key string or None
    """
    if explicit_key:
        return explicit_key

    # Check environment variable
    env_var = ENV_VARS.get(provider)
    if env_var:
        key = os.environ.get(env_var)
        if key:
            return key

    # Check auth files (project overrides global)
    auth = load_auth(check_permissions=False)
    if provider in auth:
        return auth[provider]

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


# =============================================================================
# Auth Management (for CLI)
# =============================================================================


def set_api_key(provider: str, api_key: str, local: bool = False) -> Path:
    """
    Set API key for a provider.

    Args:
        provider: Provider name
        api_key: API key value
        local: If True, save to project auth; otherwise global

    Returns:
        Path to auth file
    """
    if local:
        project_dir = get_project_config_dir()
        if project_dir is None:
            project_dir = Path.cwd() / ".innerloop"
            project_dir.mkdir(exist_ok=True)
        auth_path = project_dir / "auth.json"
    else:
        auth_path = get_global_auth_path()

    auth_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing auth
    auth = _load_auth_file(auth_path)
    auth[provider] = api_key

    # Write back
    with auth_path.open("w") as f:
        json.dump(auth, f, indent=2)
        f.write("\n")

    # Set secure permissions on Unix
    try:
        auth_path.chmod(0o600)
    except OSError:
        pass

    return auth_path


def remove_api_key(provider: str, local: bool = False) -> bool:
    """
    Remove API key for a provider.

    Args:
        provider: Provider name
        local: If True, remove from project auth; otherwise global

    Returns:
        True if key was removed, False if not found
    """
    if local:
        if project_dir := get_project_config_dir():
            auth_path = project_dir / "auth.json"
        else:
            return False
    else:
        auth_path = get_global_auth_path()

    if not auth_path.exists():
        return False

    auth = _load_auth_file(auth_path)
    if provider not in auth:
        return False

    del auth[provider]

    with auth_path.open("w") as f:
        json.dump(auth, f, indent=2)
        f.write("\n")

    return True


def list_configured_providers() -> list[dict[str, Any]]:
    """
    List all configured providers with their source.

    Returns:
        List of dicts with 'provider', 'source', and 'key_preview' keys
    """
    result: list[dict[str, Any]] = []
    seen: set[str] = set()

    # Check environment variables first
    for provider, env_var in ENV_VARS.items():
        if key := os.environ.get(env_var):
            result.append(
                {
                    "provider": provider,
                    "source": "env",
                    "key_preview": _redact_key(key),
                }
            )
            seen.add(provider)

    # Check project auth
    if project_path := get_project_auth_path():
        project_auth = _load_auth_file(project_path)
        for provider, key in project_auth.items():
            if provider not in seen:
                result.append(
                    {
                        "provider": provider,
                        "source": "project",
                        "key_preview": _redact_key(key),
                    }
                )
                seen.add(provider)

    # Check global auth
    global_auth = _load_auth_file(get_global_auth_path())
    for provider, key in global_auth.items():
        if provider not in seen:
            result.append(
                {
                    "provider": provider,
                    "source": "global",
                    "key_preview": _redact_key(key),
                }
            )
            seen.add(provider)

    return result


def _redact_key(key: str) -> str:
    """Redact API key for display, showing only first few chars."""
    if len(key) <= 8:
        return "***"
    return key[:8] + "..."


__all__ = [
    # Resolution
    "resolve_api_key",
    "get_provider_from_model",
    "load_auth",
    # Paths
    "get_global_auth_path",
    "get_project_auth_path",
    # Management
    "set_api_key",
    "remove_api_key",
    "list_configured_providers",
    # Constants
    "ENV_VARS",
]
