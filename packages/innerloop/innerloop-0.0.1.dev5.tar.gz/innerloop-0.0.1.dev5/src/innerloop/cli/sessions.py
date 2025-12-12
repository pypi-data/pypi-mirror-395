"""Session management commands."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from ..session import SessionStore


def list_sessions(show_all: bool = False, current_dir_only: bool = False) -> None:
    """List recent sessions."""
    store = SessionStore()
    limit = None if show_all else 10
    workdir = Path.cwd() if current_dir_only else None
    sessions = store.list_sessions(limit=limit, workdir=workdir)

    if not sessions:
        if current_dir_only:
            print("No sessions found in current directory")
        else:
            print("No sessions found")
        return

    print("Sessions:")
    for s in sessions:
        session_id = s["session_id"]
        title = s.get("title") or ""

        # Format timestamp
        created = s.get("created")
        if created:
            dt = datetime.fromtimestamp(created)
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        else:
            time_str = "unknown"

        # Truncate title
        if len(title) > 40:
            title = title[:37] + "..."

        print(f'  {session_id}  {time_str}  "{title}"')


def show_session(session_id: str) -> None:
    """Show contents of a session."""
    store = SessionStore()

    if not store.exists(session_id):
        print(f"Session not found: {session_id}", file=sys.stderr)
        sys.exit(1)

    meta = store.get_metadata(session_id)
    messages = store.load(session_id)

    # Header
    print(f"Session: {session_id}")
    if meta:
        if meta.model:
            print(f"Model: {meta.model}")
        if meta.created:
            dt = datetime.fromtimestamp(meta.created)
            print(f"Created: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Messages
    for msg in messages:
        role = msg.role
        if role == "user":
            content = msg.content if hasattr(msg, "content") else ""
            print(f"[user] {content}")
        elif role == "assistant":
            # Extract text from content parts
            text_parts = []
            if hasattr(msg, "content"):
                for part in msg.content:
                    if hasattr(part, "text"):
                        text_parts.append(part.text)
            content = "".join(text_parts)
            # Truncate long responses for display
            if len(content) > 500:
                content = content[:500] + "..."
            print(f"[assistant] {content}")
        elif role == "tool_result":
            tool_name = getattr(msg, "tool_name", "unknown")
            is_error = getattr(msg, "is_error", False)
            status = "error" if is_error else "ok"
            print(f"[tool:{tool_name}] ({status})")
        print()


def delete_session(session_id: str) -> None:
    """Delete a session."""
    store = SessionStore()

    if not store.exists(session_id):
        print(f"Session not found: {session_id}", file=sys.stderr)
        sys.exit(1)

    store.clear(session_id)
    print(f"Deleted session: {session_id}")


def clear_sessions() -> None:
    """Delete all sessions."""
    store = SessionStore()
    count = store.clear_all()
    print(f"Deleted {count} session(s)")


__all__ = ["list_sessions", "show_session", "delete_session", "clear_sessions"]
