"""
Session Storage

JSONL-based session persistence for conversation history.
Supports resumption via metadata and last session tracking.

Session IDs are datetime-based for chronological sorting:
  Format: YYYYMMDDHHMMSS-RRRRRR (e.g., 20241204143022-A7K2M9)
  - Datetime prefix for sortability
  - 6-char base36 random suffix for uniqueness

Sessions track their working directory for directory-aware filtering.
"""

from __future__ import annotations

import contextlib
import datetime
import json
import secrets
import string
import sys
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .types import Message

from .config import get_session_dir
from .types import dict_to_message, message_to_dict

# Platform-specific file locking
if sys.platform != "win32":
    import fcntl

    @contextlib.contextmanager
    def _file_lock(f: IO[str], exclusive: bool = True) -> Iterator[None]:
        """Acquire file lock (Unix)."""
        op = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        try:
            fcntl.flock(f.fileno(), op)
            yield
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
else:
    import msvcrt

    @contextlib.contextmanager
    def _file_lock(f: IO[str], exclusive: bool = True) -> Iterator[None]:
        """Acquire file lock (Windows) with retry to match Unix blocking behavior."""
        # LK_NBLCK fails immediately if locked; retry with backoff to simulate blocking
        max_attempts = 100  # ~10 seconds total with 0.1s sleep
        for attempt in range(max_attempts):
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if attempt == max_attempts - 1:
                    raise  # Give up after max attempts
                time.sleep(0.1)
        try:
            yield
        finally:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)


# Base36 alphabet for random suffix
_BASE36_ALPHABET = string.digits + string.ascii_uppercase


def _encode_base36(num: int, length: int) -> str:
    """Encode integer to base36 string of fixed length."""
    if num == 0:
        return _BASE36_ALPHABET[0] * length
    chars = []
    base = len(_BASE36_ALPHABET)
    while num > 0:
        num, rem = divmod(num, base)
        chars.append(_BASE36_ALPHABET[rem])
    encoded = "".join(reversed(chars))
    return encoded.rjust(length, _BASE36_ALPHABET[0])[-length:]


@dataclass
class SessionMetadata:
    """Session metadata stored in first line of JSONL."""

    model: str | None = None
    created: int | None = None
    updated: int | None = None
    title: str | None = None
    workdir: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "_meta": {
                "model": self.model,
                "created": self.created,
                "updated": self.updated,
                "title": self.title,
                "workdir": self.workdir,
            }
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionMetadata:
        """Create from dict (expects _meta wrapper)."""
        meta = data.get("_meta", {})
        return cls(
            model=meta.get("model"),
            created=meta.get("created"),
            updated=meta.get("updated"),
            title=meta.get("title"),
            workdir=meta.get("workdir"),
        )


class SessionStore:
    """
    Session persistence for conversation history.

    Required for:
    - Structured output validation retries
    - Multi-turn conversations
    - Session resumption
    - Debugging/audit trails

    Sessions are stored as JSONL files with metadata in first line.
    File locking is used for process-safe writes.
    """

    def __init__(self, base_dir: Path | None = None):
        """
        Initialize session store.

        Args:
            base_dir: Directory for session files. Defaults to XDG data dir.
        """
        self.base_dir = base_dir or get_session_dir()

    def _path(self, session_id: str) -> Path:
        """Get path for a session file."""
        # Sanitize session ID for filename safety
        safe_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
        return self.base_dir / f"{safe_id}.jsonl"

    def append(
        self,
        session_id: str,
        message: Message,
        model: str | None = None,
        workdir: Path | None = None,
    ) -> None:
        """
        Append a message to a session.

        Creates the session file with metadata if it doesn't exist.
        Uses file locking for process-safe writes.

        Args:
            session_id: Session identifier
            message: Message to append
            model: Model name (used for metadata on first message)
            workdir: Working directory (used for metadata on first message)
        """
        path = self._path(session_id)
        path.parent.mkdir(parents=True, exist_ok=True)

        now = int(time.time())
        is_new = not path.exists()

        with path.open("a") as f:
            with _file_lock(f, exclusive=True):
                # Write metadata line for new sessions
                if is_new:
                    # Generate title from first user message
                    title = None
                    if hasattr(message, "content") and isinstance(message.content, str):
                        title = message.content[:50]
                        if len(message.content) > 50:
                            title += "..."

                    meta = SessionMetadata(
                        model=model,
                        created=now,
                        updated=now,
                        title=title,
                        workdir=str(workdir.resolve()) if workdir else None,
                    )
                    f.write(json.dumps(meta.to_dict()) + "\n")

                # Write message
                data = message_to_dict(message)
                f.write(json.dumps(data) + "\n")
                f.flush()

        # Update metadata timestamp
        if not is_new:
            self._update_metadata(session_id, updated=now)

        # Track as last session
        self._set_last_session(session_id)

    def _update_metadata(self, session_id: str, **updates: Any) -> None:
        """Update metadata fields in session file (with file locking)."""
        path = self._path(session_id)
        if not path.exists():
            return

        # Use r+ mode for read-modify-write with exclusive lock
        with path.open("r+") as f:
            with _file_lock(f, exclusive=True):
                content = f.read()
                lines = content.splitlines()
                if not lines:
                    return

                # Check if first line is metadata
                try:
                    first = json.loads(lines[0])
                    if "_meta" in first:
                        meta = SessionMetadata.from_dict(first)
                        for key, value in updates.items():
                            if hasattr(meta, key):
                                setattr(meta, key, value)
                        lines[0] = json.dumps(meta.to_dict())
                        # Rewrite entire file
                        f.seek(0)
                        f.write("\n".join(lines) + "\n")
                        f.truncate()
                        f.flush()
                except (json.JSONDecodeError, ValueError):
                    pass

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
                    # Skip metadata lines
                    if "_meta" in data:
                        continue
                    messages.append(dict_to_message(data))
                except (json.JSONDecodeError, ValueError):
                    # Skip malformed lines
                    continue

        return messages

    def get_metadata(self, session_id: str) -> SessionMetadata | None:
        """
        Get metadata for a session.

        Args:
            session_id: Session identifier

        Returns:
            SessionMetadata or None if not found
        """
        path = self._path(session_id)
        if not path.exists():
            return None

        with path.open("r") as f:
            first_line = f.readline().strip()
            if not first_line:
                return None
            try:
                data = json.loads(first_line)
                if "_meta" in data:
                    return SessionMetadata.from_dict(data)
            except (json.JSONDecodeError, ValueError):
                pass

        return None

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
            Session ID in format: YYYYMMDDHHMMSS-RRRRRR
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        dt_str = now.strftime("%Y%m%d%H%M%S")
        rand = secrets.randbits(31)  # ~2 billion possibilities
        rand_str = _encode_base36(rand, 6)
        return f"{dt_str}-{rand_str}"

    def exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: Session identifier

        Returns:
            True if session file exists
        """
        return self._path(session_id).exists()

    # =========================================================================
    # Session Listing & Management
    # =========================================================================

    def list_sessions(
        self,
        limit: int | None = None,
        workdir: Path | None = None,
    ) -> list[dict[str, Any]]:
        """
        List sessions with metadata, sorted by most recent.

        Args:
            limit: Maximum number of sessions to return
            workdir: Filter by working directory

        Returns:
            List of dicts with session_id, model, created, updated, title, workdir
        """
        sessions: list[dict[str, Any]] = []

        if not self.base_dir.exists():
            return sessions

        # Resolve workdir filter
        workdir_str = str(workdir.resolve()) if workdir else None

        for path in self.base_dir.glob("*.jsonl"):
            session_id = path.stem
            meta = self.get_metadata(session_id)

            # Filter by workdir if specified
            if workdir_str and meta and meta.workdir != workdir_str:
                continue

            sessions.append(
                {
                    "session_id": session_id,
                    "model": meta.model if meta else None,
                    "created": meta.created if meta else None,
                    "updated": meta.updated if meta else None,
                    "title": meta.title if meta else None,
                    "workdir": meta.workdir if meta else None,
                    "path": str(path),
                }
            )

        # Sort by session ID (chronological due to datetime prefix)
        sessions.sort(key=lambda s: s["session_id"], reverse=True)

        if limit:
            sessions = sessions[:limit]

        return sessions

    def clear_all(self) -> int:
        """
        Delete all sessions.

        Returns:
            Number of sessions deleted
        """
        count = 0
        if not self.base_dir.exists():
            return count
        for path in self.base_dir.glob("*.jsonl"):
            path.unlink()
            count += 1
        return count

    # =========================================================================
    # Last Session Tracking
    # =========================================================================

    def _last_session_path(self) -> Path:
        """Get path to last session file."""
        return self.base_dir.parent / "last_session"

    def _set_last_session(self, session_id: str) -> None:
        """Record the last used session ID."""
        path = self._last_session_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(session_id + "\n")

    def get_last_session(self) -> str | None:
        """
        Get the last used session ID.

        Returns:
            Session ID or None if no last session
        """
        path = self._last_session_path()
        if not path.exists():
            return None
        session_id = path.read_text().strip()
        # Verify session still exists
        if session_id and self.exists(session_id):
            return session_id
        return None


__all__ = ["SessionStore", "SessionMetadata"]
