"""
Stateful Todo Tools

A todo system that lets the LLM track its own work with persistent state.

Usage:
    from innerloop.tooling import TodoState, make_todo_tools

    # Create state container
    todos = TodoState()

    # Create tools bound to state
    add_todo, list_todos, mark_done, mark_skip = make_todo_tools(todos)

    # Use in loop
    loop = Loop(model="...", tools=[add_todo, list_todos, mark_done, mark_skip])
    response = loop.run("Plan the task with todos")

    # After execution, inspect state
    print(todos.counts_str())  # "3 todo, 2 done, 1 skip"
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

from ..types import Message, ToolResultMessage
from .base import LocalTool, tool


class Status(Enum):
    """Todo status values."""

    TODO = "todo"
    DONE = "done"
    SKIP = "skip"


@dataclass
class Todo:
    """A single todo item."""

    id: int
    title: str
    note: str | None = None
    status: Status = Status.TODO


@dataclass
class TodoState:
    """Mutable container for todo state."""

    items: list[Todo] = field(default_factory=list)

    def active(self) -> list[Todo]:
        """Get todos with status=TODO."""
        return [t for t in self.items if t.status == Status.TODO]

    def counts(self) -> tuple[int, int, int]:
        """Return (todo_count, done_count, skip_count)."""
        todo = sum(1 for t in self.items if t.status == Status.TODO)
        done = sum(1 for t in self.items if t.status == Status.DONE)
        skip = sum(1 for t in self.items if t.status == Status.SKIP)
        return (todo, done, skip)

    def counts_str(self) -> str:
        """Format counts as string: '5 todo, 3 done, 1 skip'."""
        todo, done, skip = self.counts()
        parts = []
        if todo:
            parts.append(f"{todo} todo")
        if done:
            parts.append(f"{done} done")
        if skip:
            parts.append(f"{skip} skip")
        return ", ".join(parts) if parts else "empty"

    def summary(self) -> str:
        """Generate summary of active todos."""
        active = self.active()
        if not active:
            return "No active todos."

        lines = [f"Active todos ({len(active)}):"]
        for t in active:
            note_part = f" - {t.note}" if t.note else ""
            lines.append(f"  [{t.id}] {t.title}{note_part}")
        return "\n".join(lines)

    def next_id(self) -> int:
        """Generate next todo ID (length + 1)."""
        return len(self.items) + 1

    def clear(self) -> None:
        """Clear all todos."""
        self.items.clear()


def make_todo_tools(
    state: TodoState,
) -> tuple[LocalTool, LocalTool, LocalTool, LocalTool]:
    """
    Create todo tools bound to a shared state container.

    Returns: (add_todo, list_todos, mark_done, mark_skip)
    """

    def _feedback(action: str, item: Todo) -> str:
        """Format response with action confirmation and counts."""
        return f"{action} [{item.id}]: {item.title}\n({state.counts_str()})"

    @tool
    def add_todo(title: str, note: str | None = None) -> str:
        """
        Add a new todo item.

        Returns confirmation with current counts. Call list_todos to see all items.

        Args:
            title: Brief description of the task
            note: Optional additional details
        """
        todo = Todo(
            id=state.next_id(),
            title=title,
            note=note,
        )
        state.items.append(todo)
        return _feedback("Added", todo)

    @tool
    def list_todos(include_completed: bool = False) -> str:
        """
        List todos. By default shows only active (todo) items.

        Set include_completed=True to see done and skipped items too.

        Args:
            include_completed: Whether to include completed/skipped items
        """
        if include_completed:
            items = state.items
        else:
            items = state.active()

        if not items:
            msg = "No todos." if include_completed else "No active todos."
            return f"{msg}\n({state.counts_str()})"

        lines = []
        for t in items:
            status_str = f"[{t.status.value}] " if include_completed else ""
            note_str = f" - {t.note}" if t.note else ""
            lines.append(f"[{t.id}] {status_str}{t.title}{note_str}")

        lines.append(f"\n({state.counts_str()})")
        return "\n".join(lines)

    @tool
    def mark_done(todo_id: int) -> str:
        """
        Mark a todo as done by its ID.

        Returns confirmation with current counts.

        Args:
            todo_id: ID of the todo to mark as done
        """
        for t in state.items:
            if t.id == todo_id:
                t.status = Status.DONE
                return _feedback("Done", t)
        return f"Todo [{todo_id}] not found. Call list_todos to see valid IDs."

    @tool
    def mark_skip(todo_id: int, reason: str | None = None) -> str:
        """
        Mark a todo as skipped (won't do) by its ID.

        Optionally provide a reason. Returns confirmation with current counts.

        Args:
            todo_id: ID of the todo to skip
            reason: Optional explanation for why this was skipped
        """
        for t in state.items:
            if t.id == todo_id:
                t.status = Status.SKIP
                if reason:
                    t.note = f"Skipped: {reason}"
                return _feedback("Skipped", t)
        return f"Todo [{todo_id}] not found. Call list_todos to see valid IDs."

    return add_todo, list_todos, mark_done, mark_skip


def rehydrate_from_session(messages: list[Message]) -> TodoState:
    """
    Rebuild todo state by replaying session history.

    Parses tool results from add_todo, mark_done, mark_skip calls.
    """
    state = TodoState()

    for msg in messages:
        if not isinstance(msg, ToolResultMessage):
            continue

        if msg.tool_name == "add_todo":
            # Parse: "Added [3]: Write tests\n(3 todo, 1 done)"
            match = re.match(r"Added \[(\d+)\]: (.+?)\n", msg.content)
            if match:
                state.items.append(
                    Todo(
                        id=int(match.group(1)),
                        title=match.group(2),
                        status=Status.TODO,
                    )
                )

        elif msg.tool_name == "mark_done":
            # Parse: "Done [3]: Write tests\n(2 todo, 2 done)"
            match = re.match(r"Done \[(\d+)\]:", msg.content)
            if match:
                todo_id = int(match.group(1))
                for t in state.items:
                    if t.id == todo_id:
                        t.status = Status.DONE
                        break

        elif msg.tool_name == "mark_skip":
            # Parse: "Skipped [3]: Write tests\n(2 todo, 1 done, 1 skip)"
            match = re.match(r"Skipped \[(\d+)\]:", msg.content)
            if match:
                todo_id = int(match.group(1))
                for t in state.items:
                    if t.id == todo_id:
                        t.status = Status.SKIP
                        break

    return state


# Convenience: default state + tools for simple single-loop usage
_default_state = TodoState()
add_todo, list_todos, mark_done, mark_skip = make_todo_tools(_default_state)

# Export as a bundle
TODO_TOOLS = [add_todo, list_todos, mark_done, mark_skip]

__all__ = [
    # State management
    "TodoState",
    "Todo",
    "Status",
    # Factory
    "make_todo_tools",
    "rehydrate_from_session",
    # Default tools
    "add_todo",
    "list_todos",
    "mark_done",
    "mark_skip",
    "TODO_TOOLS",
]
