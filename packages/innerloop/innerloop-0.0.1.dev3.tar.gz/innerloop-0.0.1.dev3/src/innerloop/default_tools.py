"""
Default Tools

Common file system, shell, and web tools with CWD jailing.

These global tool functions are jailed to the current working directory
at import time. For production use with explicit directory control,
prefer the Zone-based tools: Loop(workdir="./sandbox", zone=Zone.FILE_ONLY).

Security notes:
- File tools (read, write, edit, ls, glob) are jailed to Path.cwd()
- Path traversal attacks (../../etc/passwd) are blocked
- bash tool executes in CWD but has no filesystem restrictions
- webfetch only allows http/https URLs (no file://)
"""

from __future__ import annotations

from pathlib import Path

from .filesystem import FileSystem, create_bash_tool, create_web_tool

# Create a CWD-jailed filesystem at import time
# This provides default security while supporting `from innerloop import read`
_default_fs = FileSystem(Path.cwd())
_default_tools = _default_fs.get_tools()

# Extract individual tools by name
read = next(t for t in _default_tools if t.name == "read")
write = next(t for t in _default_tools if t.name == "write")
edit = next(t for t in _default_tools if t.name == "edit")
ls = next(t for t in _default_tools if t.name == "ls")
glob = next(t for t in _default_tools if t.name == "glob")

# Create bash and web tools (these use the secure implementations)
bash = create_bash_tool(Path.cwd())
webfetch = create_web_tool()

# Default tool set for backward compatibility
DEFAULT_TOOLS = [read, write, edit, glob, ls, bash]


__all__ = [
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "bash",
    "webfetch",
    "DEFAULT_TOOLS",
]
