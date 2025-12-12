"""
Execution Context

Thread-local context for passing workdir to built-in tools.
"""

from __future__ import annotations

import contextlib
import contextvars
from collections.abc import Iterator
from pathlib import Path

# Context variable for workdir
_workdir: contextvars.ContextVar[Path | None] = contextvars.ContextVar(
    "workdir", default=None
)


def get_workdir() -> Path:
    """Get the current workdir from context."""
    wd = _workdir.get()
    return wd if wd is not None else Path.cwd()


def set_workdir(path: Path) -> contextvars.Token[Path | None]:
    """Set the workdir in context. Returns token for reset."""
    return _workdir.set(path)


def reset_workdir(token: contextvars.Token[Path | None]) -> None:
    """Reset workdir to previous value using token."""
    _workdir.reset(token)


@contextlib.contextmanager
def workdir_context(path: Path) -> Iterator[None]:
    """Context manager for temporarily setting workdir.

    Useful for testing or using built-in tools outside Loop.

    Example:
        with workdir_context(Path("/tmp/sandbox")):
            content = read("file.txt")  # Reads from /tmp/sandbox/file.txt
    """
    token = set_workdir(path)
    try:
        yield
    finally:
        reset_workdir(token)


__all__ = ["get_workdir", "set_workdir", "reset_workdir", "workdir_context"]
