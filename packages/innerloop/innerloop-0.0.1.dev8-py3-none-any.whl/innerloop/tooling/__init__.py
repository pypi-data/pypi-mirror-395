"""
InnerLoop Tooling Subpackage

Provides curryable and stateful tools for the agent loop.

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
"""

# Base infrastructure (re-exported)
from .base import LocalTool, ToolContext, tool

# Curryable bash
from .bash import BashConfig, BashTool, bash

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

__all__ = [
    # Base
    "tool",
    "LocalTool",
    "ToolContext",
    # Bash
    "bash",
    "BashTool",
    "BashConfig",
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
]
