"""
Built-in Tools

Standard tools for file operations, search, shell, and web access.
All file tools are jailed to workdir to prevent path traversal.

Usage:
    from innerloop import Loop, read, write, edit, bash

    # Use specific tools
    loop = Loop(model="...", tools=[read, write, edit])

    # Default: safe file tools
    loop = Loop(model="...")  # includes read, write, edit, glob, ls, grep
"""

from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from .tools import LocalTool, tool


class SecurityError(ValueError):
    """Raised when a path escapes the allowed directory."""

    pass


def _get_workdir() -> Path:
    """Get workdir from context or default to cwd."""
    # This will be set by Loop before tool execution
    from .context import get_workdir

    return get_workdir()


def _secure_path(user_path: str) -> Path:
    """
    Resolve a path and verify it's inside the workdir.

    Args:
        user_path: User-provided path (relative or absolute)

    Returns:
        Resolved Path object guaranteed to be inside workdir

    Raises:
        SecurityError: If path escapes the workdir
    """
    workdir = _get_workdir()

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
def read(file_path: str) -> str:
    """Read contents of a file.

    Args:
        file_path: Path to the file to read (relative to working directory)
    """
    target = _secure_path(file_path)
    if not target.exists():
        raise FileNotFoundError(f"file not found: {file_path}")
    if target.is_dir():
        raise IsADirectoryError(f"{file_path} is a directory, not a file")
    return target.read_text()


@tool
def write(file_path: str, content: str) -> str:
    """Create or overwrite a file.

    Args:
        file_path: Path to the file to write (relative to working directory)
        content: Content to write to the file
    """
    target = _secure_path(file_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return f"Wrote {len(content)} bytes to {file_path}"


@tool
def edit(file_path: str, old_text: str, new_text: str) -> str:
    """Edit a file by replacing exact text.

    Args:
        file_path: Path to the file to edit (relative to working directory)
        old_text: Text to find and replace (must be unique in file)
        new_text: Text to replace with
    """
    target = _secure_path(file_path)
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
def glob(pattern: str, directory: str = ".") -> str:
    """Find files matching a glob pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "src/**/*.js")
        directory: Directory to search in (relative to working directory)
    """
    workdir = _get_workdir()
    target = _secure_path(directory)
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
def ls(directory: str = ".") -> str:
    """List files and directories.

    Args:
        directory: Directory to list (relative to working directory)
    """
    target = _secure_path(directory)
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


@tool
def grep(pattern: str, path: str = ".", file_pattern: str | None = None) -> str:
    """Search file contents using regular expressions.

    Args:
        pattern: Regex pattern to search for
        path: File or directory to search (relative to working directory)
        file_pattern: Optional glob pattern to filter files (e.g., "*.py")
    """
    workdir = _get_workdir()
    target = _secure_path(path)
    if not target.exists():
        raise FileNotFoundError(f"path not found: {path}")

    # Compile regex
    try:
        regex = re.compile(pattern)
    except re.error as e:
        raise ValueError(f"invalid regex: {e}") from e

    results: list[str] = []

    # Get files to search
    if target.is_file():
        files = [target]
    else:
        glob_pat = file_pattern or "**/*"
        files = [f for f in target.glob(glob_pat) if f.is_file()]
        # Security filter
        files = [f for f in files if f.resolve().is_relative_to(workdir)]

    for file in files:
        try:
            content = file.read_text()
        except (UnicodeDecodeError, PermissionError):
            continue

        for i, line in enumerate(content.splitlines(), 1):
            if regex.search(line):
                rel_path = file.relative_to(workdir)
                results.append(f"{rel_path}:{i}: {line}")

    if not results:
        return f"No matches found for pattern: {pattern}"

    # Limit results
    if len(results) > 100:
        return "\n".join(results[:100]) + f"\n... ({len(results) - 100} more)"

    return "\n".join(results)


@tool
def bash(command: str) -> str:
    """Execute a shell command.

    Args:
        command: Shell command to execute
    """
    workdir = _get_workdir()
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=workdir,
    )
    output = result.stdout or result.stderr
    return output.strip() if output else f"Command exited with code {result.returncode}"


@tool
def webfetch(url: str) -> str:
    """Fetch content from a URL.

    Args:
        url: URL to fetch (http or https only)
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Invalid URL scheme '{parsed.scheme}'. Only http and https allowed."
        )

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "InnerLoop/2.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        status = response.status
        content = response.read().decode("utf-8", errors="replace")
        if len(content) > 10000:
            content = content[:10000] + "\n... (truncated)"
        return f"Status: {status}\n\n{content}"


# Default safe tools (no bash, no webfetch)
DEFAULT_TOOLS: list[LocalTool] = [read, write, edit, glob, ls, grep]

# All available built-in tools
ALL_TOOLS: list[LocalTool] = [read, write, edit, glob, ls, grep, bash, webfetch]

__all__ = [
    # Individual tools
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "grep",
    "bash",
    "webfetch",
    # Tool collections
    "DEFAULT_TOOLS",
    "ALL_TOOLS",
    # Security
    "SecurityError",
]
