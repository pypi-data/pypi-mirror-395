"""Run command implementation."""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime
from pathlib import Path

from ..api import Loop
from ..config import get_default_model, load_config, resolve_model_alias
from ..session import SessionStore
from ..types import TextEvent


async def _run_async(
    prompt: str,
    model: str,
    stream: bool,
    session_id: str | None,
) -> None:
    """Async implementation of run command."""
    loop = Loop(model=model, session=session_id)

    if stream:
        async for event in loop.astream(prompt):
            if isinstance(event, TextEvent):
                print(event.text, end="", flush=True)
        print()
    else:
        response = await loop.arun(prompt)
        print(response.text)


def _select_session_interactive(
    store: SessionStore,
    workdir: Path,
) -> str | None:
    """
    Show interactive session picker.

    Returns:
        Selected session ID, or None to create new session.
    """
    sessions = store.list_sessions(workdir=workdir, limit=10)

    if not sessions:
        print("No previous sessions in this directory", file=sys.stderr)
        sys.exit(1)

    print(f"\nRecent sessions in {workdir}:\n")
    for i, sess in enumerate(sessions, 1):
        created = sess.get("created")
        if created:
            dt = datetime.fromtimestamp(created)
            date_str = dt.strftime("%Y-%m-%d %H:%M")
        else:
            date_str = "unknown"

        title = (sess.get("title") or "")[:40]

        print(f'  [{i}] {sess["session_id"]}  {date_str}  "{title}"')

    print()
    choice = input(
        f"Select session [1-{len(sessions)}] or press Enter for new: "
    ).strip()

    if not choice:
        return None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(sessions):
            return sessions[idx]["session_id"]
        print("Invalid selection", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Invalid selection", file=sys.stderr)
        sys.exit(1)


def run_command(
    prompt: str,
    model: str | None,
    stream: bool,
    continue_session: bool = False,
    continue_id: str | None = None,
    non_interactive: bool = False,
) -> None:
    """
    Execute prompt using InnerLoop.

    Args:
        prompt: Prompt to execute
        model: Model string or alias (uses default if None)
        stream: Stream output to stdout
        continue_session: Continue a session (interactive picker if no ID)
        continue_id: Specific session ID or list number to continue
        non_interactive: Auto-select most recent session
    """
    try:
        # Resolve model
        config = load_config()
        if model is None:
            resolved_model = get_default_model(config)
        else:
            resolved_model = resolve_model_alias(model, config)

        # Handle session continuation
        resolved_session: str | None = None
        if continue_session or continue_id:
            store = SessionStore()
            workdir = Path.cwd()

            if continue_id:
                # User specified session by ID or list number
                if continue_id.isdigit():
                    # List number (1-based)
                    sessions = store.list_sessions(workdir=workdir, limit=10)
                    idx = int(continue_id) - 1
                    if 0 <= idx < len(sessions):
                        resolved_session = sessions[idx]["session_id"]
                    else:
                        print(
                            f"Invalid session number: {continue_id}",
                            file=sys.stderr,
                        )
                        sys.exit(1)
                else:
                    # Direct session ID
                    if store.exists(continue_id):
                        resolved_session = continue_id
                    else:
                        print(
                            f"Session not found: {continue_id}",
                            file=sys.stderr,
                        )
                        sys.exit(1)
            elif non_interactive:
                # Auto-select most recent
                sessions = store.list_sessions(workdir=workdir, limit=1)
                if sessions:
                    resolved_session = sessions[0]["session_id"]
                else:
                    print(
                        "No previous sessions in this directory",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            else:
                # Interactive selection
                resolved_session = _select_session_interactive(store, workdir)

        asyncio.run(_run_async(prompt, resolved_model, stream, resolved_session))
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


__all__ = ["run_command"]
