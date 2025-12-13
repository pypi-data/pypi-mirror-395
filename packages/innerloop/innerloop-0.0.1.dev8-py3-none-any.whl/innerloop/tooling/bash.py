"""
Curryable Bash Tool

A bash tool that can be used directly or curried with constraints.

Usage:
    from innerloop.tooling import bash

    # Full reign - use bash directly as a tool
    loop = Loop(model="...", tools=[bash])

    # Curry with constraints
    safe_bash = bash(
        allow={"make": "Run make targets", "uv": "Python package manager"},
        deny=["rm -rf", "sudo", "chmod 777"],
        usage="Use make for builds. Destructive commands are blocked."
    )
    loop = Loop(model="...", tools=[safe_bash])
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from typing import Any

from .base import LocalTool, ToolContext


def _to_regex(pattern: str) -> str:
    """
    Convert human-readable deny pattern to regex.

    "rm -rf"  -> r"\\brm\\s+\\-rf\\b"
    "sudo"    -> r"\\bsudo\\b"
    ">/etc/"  -> r">/etc/"  (no word boundaries for punctuation)

    If pattern already looks like regex (contains \\b or ^), keep as-is.
    """
    # Already regex? Keep as-is
    if r"\b" in pattern or pattern.startswith("^"):
        return pattern

    # Escape regex special chars except spaces
    escaped = re.escape(pattern)

    # Convert escaped spaces (\\ ) back to flexible whitespace
    escaped = escaped.replace(r"\ ", r"\s+")

    # Only add word boundaries around word characters
    # \b doesn't work before/after punctuation like > or /
    prefix = r"\b" if pattern and pattern[0].isalnum() else ""
    suffix = r"\b" if pattern and pattern[-1].isalnum() else ""

    return f"{prefix}{escaped}{suffix}"


@dataclass(frozen=True)
class BashConfig:
    """Configuration for bash tool constraints."""

    allow: dict[str, str]  # {command: description}
    deny: list[str]  # Patterns to block (human-readable or regex)
    deny_regex: tuple[str, ...]  # Compiled regex patterns (internal)
    usage: str | None  # Usage notes for LLM


def _build_docstring(
    base: str,
    config: BashConfig | None,
) -> str:
    """Build docstring with allow/deny/usage sections."""
    sections = [base.strip()]

    if config is None:
        return sections[0]

    if config.allow:
        sections.append("\nRecommended commands:")
        for cmd, desc in config.allow.items():
            sections.append(f"  - {cmd}: {desc}")

    if config.deny:
        sections.append("\nBlocked commands:")
        for pattern in config.deny:
            sections.append(f"  - {pattern}")

    if config.usage:
        sections.append(f"\nUsage: {config.usage}")

    return "\n".join(sections)


class BashTool(LocalTool):
    """Bash tool that can be curried with configuration."""

    _config: BashConfig | None
    _deny_patterns: list[re.Pattern[str]]

    def __init__(
        self,
        config: BashConfig | None = None,
    ):
        # Build docstring based on config
        description = _build_docstring(
            "Execute a shell command and return its output.",
            config,
        )

        # Build JSON schema
        input_schema = {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Optional timeout in seconds (overrides default)",
                },
            },
            "required": ["command"],
        }

        super().__init__(
            name="bash",
            description=description,
            input_schema=input_schema,
            handler=self._execute_handler,
            context_params=["ctx"],
        )

        # Store config using object.__setattr__ since LocalTool is frozen via Pydantic
        object.__setattr__(self, "_config", config)
        deny_patterns = [re.compile(p) for p in config.deny_regex] if config else []
        object.__setattr__(self, "_deny_patterns", deny_patterns)

    def _check_denied(self, command: str) -> None:
        """Check if command matches any deny pattern."""
        for pattern in self._deny_patterns:
            if pattern.search(command):
                raise ValueError(f"Command blocked by policy: {command!r}")

    def _execute_handler(
        self,
        command: str,
        ctx: ToolContext | None = None,
        timeout: int | None = None,
    ) -> str:
        """Execute the shell command."""
        self._check_denied(command)

        # Determine timeout
        if timeout is not None:
            effective_timeout = timeout
        elif ctx is not None:
            effective_timeout = int(ctx.tool_timeout)
        else:
            effective_timeout = 60  # Default fallback

        # Determine working directory
        cwd = ctx.workdir if ctx else None

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=effective_timeout,
            cwd=cwd,
        )

        output = result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"

        return output.strip() or "(no output)"


class BashFactory:
    """
    Dual-purpose bash: use directly as a tool or curry with config.

    # Direct use as tool:
    loop = Loop(model="...", tools=[bash])

    # Curry with config (returns new tool):
    safe_bash = bash(allow={...}, deny=[...], usage="...")
    loop = Loop(model="...", tools=[safe_bash])
    """

    def __init__(self) -> None:
        self._default = BashTool()

    def __call__(
        self,
        *,
        allow: dict[str, str] | None = None,
        deny: list[str] | None = None,
        usage: str | None = None,
    ) -> BashTool:
        """Create a new bash tool with constraints."""
        if allow is None and deny is None and usage is None:
            # No config - return unconstrained tool
            return self._default

        deny_list = deny or []
        config = BashConfig(
            allow=allow or {},
            deny=deny_list,
            deny_regex=tuple(_to_regex(p) for p in deny_list),
            usage=usage,
        )
        return BashTool(config)

    # Forward tool protocol attributes to default tool
    @property
    def name(self) -> str:
        return self._default.name

    @property
    def description(self) -> str:
        return self._default.description

    @property
    def input_schema(self) -> dict[str, Any]:
        return self._default.input_schema

    async def execute(
        self, input: dict[str, Any], context: ToolContext | None = None
    ) -> tuple[str, bool]:
        """Execute the default bash tool."""
        return await self._default.execute(input, context)


# The exported bash object - can be used directly or curried
bash = BashFactory()

__all__ = [
    "bash",
    "BashTool",
    "BashConfig",
    "_to_regex",
]
