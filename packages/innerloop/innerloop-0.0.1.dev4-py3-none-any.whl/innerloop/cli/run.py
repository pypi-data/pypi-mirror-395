"""Run command implementation."""

from __future__ import annotations

import asyncio
import sys

from ..api import Loop
from ..types import TextEvent


async def _run_async(prompt: str, model: str, stream: bool) -> None:
    """Async implementation of run command."""
    loop = Loop(model=model)

    if stream:
        async for event in loop.astream(prompt):
            if isinstance(event, TextEvent):
                print(event.text, end="", flush=True)
        print()
    else:
        response = await loop.arun(prompt)
        print(response.text)


def run_command(prompt: str, model: str, stream: bool) -> None:
    """
    Execute prompt using InnerLoop.

    Args:
        prompt: Prompt to execute
        model: Model string (e.g., "openai/gpt-5-nano")
        stream: Stream output to stdout
    """
    try:
        asyncio.run(_run_async(prompt, model, stream))
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


__all__ = ["run_command"]
