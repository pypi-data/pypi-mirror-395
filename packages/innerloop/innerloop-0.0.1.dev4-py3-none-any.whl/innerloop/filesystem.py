"""
Filesystem Security

Jailed filesystem tools bound to a root directory.
Prevents path traversal attacks (../../etc/passwd, etc.)
"""

from __future__ import annotations

import subprocess
import urllib.request
from enum import Enum
from pathlib import Path

from .tools import LocalTool, tool


class SecurityError(ValueError):
    """Raised when a path escapes the allowed directory."""

    pass


class Zone(Enum):
    """
    Tool isolation zones.

    Zones define mutually exclusive capability sets to prevent
    dangerous tool combinations (e.g., file access + web access).
    """

    FILE_ONLY = "file_only"  # read, write, edit, ls, glob
    WEB_ONLY = "web_only"  # webfetch
    CODE_EXEC = "code_exec"  # bash (dangerous - explicit opt-in)
    STRUCTURED = "structured"  # No tools, structured output only
    UNRESTRICTED = "unrestricted"  # All tools (requires explicit opt-in)


class FileSystem:
    """
    Jailed filesystem tools bound to a root directory.

    All file operations are restricted to paths within the root.
    Path traversal attempts (../, symlinks outside root) are blocked.

    Example:
        fs = FileSystem(Path("./project"))
        tools = fs.get_tools()

        # These work:
        read("src/main.py")
        write("output/result.txt", "...")

        # These raise SecurityError:
        read("../../../etc/passwd")
        read("/etc/passwd")
    """

    def __init__(self, root: Path):
        """
        Initialize with a root directory.

        Args:
            root: Root directory for all file operations.
                  All paths will be resolved relative to this.
        """
        self.root = root.resolve()
        if not self.root.exists():
            self.root.mkdir(parents=True, exist_ok=True)

    def _secure_path(self, user_path: str) -> Path:
        """
        Resolve a path and verify it's inside the jail.

        Args:
            user_path: User-provided path (relative or absolute)

        Returns:
            Resolved Path object guaranteed to be inside root

        Raises:
            SecurityError: If path escapes the root directory
        """
        # Handle absolute paths by making them relative
        if user_path.startswith("/"):
            user_path = user_path.lstrip("/")

        # Resolve relative to root
        target = (self.root / user_path).resolve()

        # Check for jailbreak (handles ../, symlinks, etc.)
        try:
            target.relative_to(self.root)
        except ValueError as e:
            raise SecurityError(
                f"Security error: path '{user_path}' escapes working directory"
            ) from e

        return target

    def get_tools(self) -> list[LocalTool]:
        """
        Get file tools bound to this filesystem.

        Returns:
            List of LocalTool instances for read, write, edit, ls, glob
        """
        fs = self  # Capture for closures

        @tool
        def read(file_path: str) -> str:
            """Read contents of a file.

            Args:
                file_path: Path to the file to read (relative to working directory)
            """
            target = fs._secure_path(file_path)
            if not target.exists():
                raise FileNotFoundError(f"file not found: {file_path}")
            if target.is_dir():
                raise IsADirectoryError(
                    f"{file_path} is a directory, not a file"
                )
            return target.read_text()

        @tool
        def write(file_path: str, content: str) -> str:
            """Write content to a file.

            Args:
                file_path: Path to the file to write (relative to working directory)
                content: Content to write to the file
            """
            target = fs._secure_path(file_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            return f"Wrote {len(content)} bytes to {file_path}"

        @tool
        def edit(file_path: str, old_text: str, new_text: str) -> str:
            """Edit a file by replacing text.

            Args:
                file_path: Path to the file to edit (relative to working directory)
                old_text: Text to find and replace
                new_text: Text to replace with
            """
            target = fs._secure_path(file_path)
            if not target.exists():
                raise FileNotFoundError(f"file not found: {file_path}")

            content = target.read_text()
            if old_text not in content:
                raise ValueError(f"text not found in {file_path}")

            # Check for multiple matches
            count = content.count(old_text)
            if count > 1:
                raise ValueError(
                    f"found {count} matches. Provide more context for unique match."
                )

            new_content = content.replace(old_text, new_text, 1)
            target.write_text(new_content)
            return f"Replaced text in {file_path}"

        @tool
        def ls(directory: str = ".") -> str:
            """List files and directories.

            Args:
                directory: Directory to list (relative to working directory)
            """
            target = fs._secure_path(directory)
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
        def glob(pattern: str, directory: str = ".") -> str:
            """Find files matching a glob pattern.

            Args:
                pattern: Glob pattern (e.g., "*.py", "src/**/*.js")
                directory: Directory to search in (relative to working directory)
            """
            target = fs._secure_path(directory)
            if not target.exists():
                raise FileNotFoundError(f"directory not found: {directory}")

            matches = list(target.glob(pattern))

            # Filter out any matches that somehow escaped (shouldn't happen)
            safe_matches = []
            for m in matches:
                try:
                    m.resolve().relative_to(fs.root)
                    safe_matches.append(m)
                except ValueError:
                    continue

            if not safe_matches:
                return f"No files found matching {pattern}"

            # Return paths relative to root
            return "\n".join(
                str(p.relative_to(fs.root)) for p in sorted(safe_matches)
            )

        return [read, write, edit, ls, glob]


def create_bash_tool(workdir: Path) -> LocalTool:
    """
    Create a bash tool that runs commands in the specified directory.

    The bash tool is NOT included by default - it must be explicitly
    requested via Zone.CODE_EXEC or Zone.UNRESTRICTED.

    Args:
        workdir: Working directory for command execution

    Returns:
        LocalTool for bash command execution
    """
    workdir = workdir.resolve()

    @tool
    def bash(command: str) -> str:
        """Execute a bash command.

        Args:
            command: Shell command to execute
        """
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=workdir,
        )
        output = result.stdout or result.stderr
        return (
            output.strip()
            if output
            else f"Command exited with code {result.returncode}"
        )

    return bash


def create_web_tool() -> LocalTool:
    """
    Create a web fetch tool.

    Returns:
        LocalTool for fetching URLs
    """
    from urllib.parse import urlparse

    @tool
    def webfetch(url: str) -> str:
        """Fetch content from a URL.

        Args:
            url: URL to fetch (http or https only)
        """
        # Security: Only allow http/https to prevent file:// access
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                f"Invalid URL scheme '{parsed.scheme}'. Only http and https are allowed."
            )

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "InnerLoop/2.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            status = response.status
            content = response.read().decode("utf-8", errors="replace")
            # Truncate large responses
            if len(content) > 10000:
                content = content[:10000] + "\n... (truncated)"
            return f"Status: {status}\n\n{content}"

    return webfetch


def get_zone_tools(
    zone: Zone,
    workdir: Path,
) -> list[LocalTool]:
    """
    Get tools for a specific zone.

    Args:
        zone: The capability zone
        workdir: Working directory for file tools

    Returns:
        List of tools allowed in that zone
    """
    fs = FileSystem(workdir)
    file_tools = fs.get_tools()

    if zone == Zone.FILE_ONLY:
        return file_tools
    elif zone == Zone.WEB_ONLY:
        return [create_web_tool()]
    elif zone == Zone.CODE_EXEC:
        return [create_bash_tool(workdir)]
    elif zone == Zone.STRUCTURED:
        return []
    else:  # Zone.UNRESTRICTED
        return [*file_tools, create_bash_tool(workdir), create_web_tool()]


__all__ = [
    "FileSystem",
    "SecurityError",
    "Zone",
    "create_bash_tool",
    "create_web_tool",
    "get_zone_tools",
]
