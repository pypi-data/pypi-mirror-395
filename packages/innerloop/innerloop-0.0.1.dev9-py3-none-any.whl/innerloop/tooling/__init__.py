"""
InnerLoop Tooling Subpackage

Provides curryable, stateful, and specialized tools for the agent loop.

Bash (curryable):
    from innerloop.tooling import bash

    # Full reign
    loop = Loop(model="...", tools=[bash])

    # Constrained
    safe_bash = bash(
        allow={"make": "Run make targets"},
        deny=["rm -rf", "sudo"],
        usage="Use make for builds"
    )
    loop = Loop(model="...", tools=[safe_bash])

Todo (stateful):
    from innerloop.tooling import TodoState, make_todo_tools

    todos = TodoState()
    add_todo, list_todos, mark_done, mark_skip = make_todo_tools(todos)
    loop = Loop(model="...", tools=[add_todo, list_todos, mark_done, mark_skip])

Filesystem:
    from innerloop.tooling import read, write, edit, glob, ls, grep
    from innerloop.tooling import FS_TOOLS, SAFE_FS_TOOLS

    loop = Loop(model="...", tools=SAFE_FS_TOOLS)  # read-only tools

Web:
    from innerloop.tooling import fetch, download, search, WEB_TOOLS

    loop = Loop(model="...", tools=WEB_TOOLS)
"""

# Base infrastructure (re-exported)
from .base import LocalTool, ToolContext, tool

# Curryable bash
from .bash import BashConfig, BashTool, bash

# Filesystem tools
from .filesystem import (
    FS_TOOLS,
    SAFE_FS_TOOLS,
    SecurityError,
    edit,
    glob,
    grep,
    ls,
    read,
    write,
)

# Stateful todos
from .todo import (
    TODO_TOOLS,
    Status,
    Todo,
    TodoState,
    add_todo,
    list_todos,
    make_todo_tools,
    mark_done,
    mark_skip,
    rehydrate_from_session,
)

# Web tools
from .web import WEB_TOOLS, download, fetch, search

# Combined bundles
ALL_TOOLS = [*FS_TOOLS, bash, *WEB_TOOLS]

__all__ = [
    # Base
    "tool",
    "LocalTool",
    "ToolContext",
    # Bash
    "bash",
    "BashTool",
    "BashConfig",
    # Filesystem
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "grep",
    "FS_TOOLS",
    "SAFE_FS_TOOLS",
    "SecurityError",
    # Todo
    "TodoState",
    "Todo",
    "Status",
    "make_todo_tools",
    "rehydrate_from_session",
    "add_todo",
    "list_todos",
    "mark_done",
    "mark_skip",
    "TODO_TOOLS",
    # Web
    "fetch",
    "download",
    "search",
    "WEB_TOOLS",
    # Bundles
    "ALL_TOOLS",
]
