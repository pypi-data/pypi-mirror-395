"""
Session Storage

JSONL-based session persistence for conversation history.
Required for structured output retries.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import Message

from .types import dict_to_message, message_to_dict


class SessionStore:
    """
    Session persistence for conversation history.

    Required for:
    - Structured output validation retries
    - Multi-turn conversations
    - Debugging/audit trails

    Sessions are stored as JSONL files in ~/.innerloop/sessions/

    CONCURRENCY WARNING:
    This implementation is NOT process-safe or thread-safe for concurrent
    writes to the same session. If running parallel agents or multiple
    processes accessing the same session_id, JSONL corruption may occur.

    For single-threaded or isolated session usage (typical case), this is safe.
    """

    def __init__(self, base_dir: Path | None = None):
        """
        Initialize session store.

        Args:
            base_dir: Directory for session files. Defaults to ~/.innerloop/sessions/
        """
        self.base_dir = base_dir or Path.home() / ".innerloop" / "sessions"

    def _path(self, session_id: str) -> Path:
        """Get path for a session file."""
        # Sanitize session ID for filename safety
        safe_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
        return self.base_dir / f"{safe_id}.jsonl"

    def append(self, session_id: str, message: Message) -> None:
        """
        Append a message to a session.

        Creates the session file if it doesn't exist.

        Args:
            session_id: Session identifier
            message: Message to append
        """
        path = self._path(session_id)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("a") as f:
            data = message_to_dict(message)
            f.write(json.dumps(data) + "\n")

    def load(self, session_id: str) -> list[Message]:
        """
        Load all messages from a session.

        Args:
            session_id: Session identifier

        Returns:
            List of messages in chronological order
        """
        path = self._path(session_id)
        if not path.exists():
            return []

        messages: list[Message] = []
        with path.open("r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    messages.append(dict_to_message(data))
                except (json.JSONDecodeError, ValueError):
                    # Skip malformed lines
                    continue

        return messages

    def clear(self, session_id: str) -> None:
        """
        Clear a session (delete the file).

        Args:
            session_id: Session identifier
        """
        path = self._path(session_id)
        if path.exists():
            path.unlink()

    def new_session_id(self) -> str:
        """
        Generate a new unique session ID.

        Returns:
            Session ID in format: ses_{uuid_hex}
        """
        return f"ses_{uuid.uuid4().hex[:16]}"

    def exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: Session identifier

        Returns:
            True if session file exists
        """
        return self._path(session_id).exists()


__all__ = ["SessionStore"]
