"""
Filesystem Tools

Standard tools for file operations with jailed paths.
All file tools are jailed to workdir to prevent path traversal.

Usage:
    from innerloop.tooling import read, write, edit, glob, ls, grep

    loop = Loop(model="...", tools=[read, write, edit, glob, ls, grep])

    # Or use the collections
    from innerloop.tooling import FS_TOOLS, SAFE_FS_TOOLS
    loop = Loop(model="...", tools=SAFE_FS_TOOLS)  # read-only tools
"""

from __future__ import annotations

import re
from pathlib import Path

from ..types import ToolContext
from .base import LocalTool, tool


class SecurityError(ValueError):
    """Raised when a path escapes the allowed directory."""

    pass


def _secure_path(user_path: str, workdir: Path) -> Path:
    """
    Resolve a path and verify it's inside the workdir.

    Args:
        user_path: User-provided path (relative or absolute)
        workdir: The working directory to jail paths to

    Returns:
        Resolved Path object guaranteed to be inside workdir

    Raises:
        SecurityError: If path escapes the workdir
    """
    # Handle absolute paths by making them relative
    if user_path.startswith("/"):
        user_path = user_path.lstrip("/")

    # Resolve relative to workdir
    target = (workdir / user_path).resolve()

    # Check for jailbreak (handles ../, symlinks, etc.)
    try:
        target.relative_to(workdir)
    except ValueError as e:
        raise SecurityError(
            f"Security error: path '{user_path}' escapes working directory"
        ) from e

    return target


@tool
def read(ctx: ToolContext, file_path: str) -> str:
    """Read contents of a file.

    Args:
        file_path: Path to the file to read (relative to working directory)
    """
    target = _secure_path(file_path, ctx.workdir)
    if not target.exists():
        raise FileNotFoundError(f"file not found: {file_path}")
    if target.is_dir():
        raise IsADirectoryError(f"{file_path} is a directory, not a file")
    return target.read_text()


@tool
def write(ctx: ToolContext, file_path: str, content: str) -> str:
    """Create or overwrite a file.

    Args:
        file_path: Path to the file to write (relative to working directory)
        content: Content to write to the file
    """
    target = _secure_path(file_path, ctx.workdir)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return f"Wrote {len(content)} bytes to {file_path}"


@tool
def edit(ctx: ToolContext, file_path: str, old_text: str, new_text: str) -> str:
    """Edit a file by replacing exact text.

    Args:
        file_path: Path to the file to edit (relative to working directory)
        old_text: Text to find and replace (must be unique in file)
        new_text: Text to replace with
    """
    target = _secure_path(file_path, ctx.workdir)
    if not target.exists():
        raise FileNotFoundError(f"file not found: {file_path}")

    content = target.read_text()
    if old_text not in content:
        raise ValueError(f"text not found in {file_path}")

    count = content.count(old_text)
    if count > 1:
        raise ValueError(
            f"found {count} matches. Provide more context for unique match."
        )

    new_content = content.replace(old_text, new_text, 1)
    target.write_text(new_content)
    return f"Replaced text in {file_path}"


@tool
def glob(ctx: ToolContext, pattern: str, directory: str = ".") -> str:
    """Find files matching a glob pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "src/**/*.js")
        directory: Directory to search in (relative to working directory)
    """
    workdir = ctx.workdir
    target = _secure_path(directory, workdir)
    if not target.exists():
        raise FileNotFoundError(f"directory not found: {directory}")

    matches = list(target.glob(pattern))

    # Filter out any matches that escaped (shouldn't happen)
    safe_matches = []
    for m in matches:
        try:
            m.resolve().relative_to(workdir)
            safe_matches.append(m)
        except ValueError:
            continue

    if not safe_matches:
        return f"No files found matching {pattern}"

    return "\n".join(str(p.relative_to(workdir)) for p in sorted(safe_matches))


@tool
def ls(ctx: ToolContext, directory: str = ".") -> str:
    """List files and directories.

    Args:
        directory: Directory to list (relative to working directory)
    """
    target = _secure_path(directory, ctx.workdir)
    if not target.exists():
        raise FileNotFoundError(f"directory not found: {directory}")
    if not target.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory")

    items = sorted(target.iterdir(), key=lambda p: p.name)
    lines = []
    for item in items:
        prefix = "[DIR] " if item.is_dir() else "      "
        lines.append(f"{prefix}{item.name}")
    return "\n".join(lines) if lines else "(empty directory)"


_GREP_MAX_RESULTS = 100


@tool
def grep(
    ctx: ToolContext,
    pattern: str,
    path: str = ".",
    file_pattern: str | None = None,
) -> str:
    """Search file contents for a regex pattern.

    Args:
        pattern: Regex to match in file contents (e.g., "def.*foo")
        path: File or directory to search
        file_pattern: Glob to filter which files to search (e.g., "*.py")
    """
    workdir = ctx.workdir
    target = _secure_path(path, workdir)
    if not target.exists():
        raise FileNotFoundError(f"path not found: {path}")

    # Compile regex
    try:
        regex = re.compile(pattern)
    except re.error as e:
        raise ValueError(f"invalid regex: {e}") from e

    results: list[str] = []

    # Get files to search - use generator for lazy evaluation
    if target.is_file():
        files = iter([target])
    else:
        glob_pat = file_pattern or "**/*"
        # Use generator expression to avoid materializing all files at once
        files = (
            f
            for f in target.glob(glob_pat)
            if f.is_file() and f.resolve().is_relative_to(workdir)
        )

    for file in files:
        # Early termination: stop once we have enough results
        if len(results) >= _GREP_MAX_RESULTS:
            break

        try:
            # Read line-by-line to avoid loading entire file into memory
            with file.open(encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    line = line.rstrip("\n\r")
                    if regex.search(line):
                        rel_path = file.relative_to(workdir)
                        results.append(f"{rel_path}:{i}: {line}")
                        # Early termination within file
                        if len(results) >= _GREP_MAX_RESULTS:
                            break
        except (PermissionError, OSError):
            continue

    if not results:
        return f"No matches found for pattern: {pattern}"

    # Truncation message if we hit the limit
    if len(results) >= _GREP_MAX_RESULTS:
        return "\n".join(results) + "\n... (truncated at 100 results)"

    return "\n".join(results)


# Full filesystem tools (read and write operations)
FS_TOOLS: list[LocalTool] = [read, write, edit, glob, ls, grep]

# Safe filesystem tools (read-only operations)
SAFE_FS_TOOLS: list[LocalTool] = [read, glob, ls, grep]

__all__ = [
    # Individual tools
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "grep",
    # Tool collections
    "FS_TOOLS",
    "SAFE_FS_TOOLS",
    # Security
    "SecurityError",
]
