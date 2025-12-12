"""
InnerLoop SDK

Lightweight Python SDK for building LLM agent loops.

Features:
- Tool calling via @tool decorator
- Core tools (read, write, edit, bash, etc.)
- Structured output with Pydantic
- Session management (JSONL)
- Streaming (sync/async)
- Direct provider APIs (Anthropic, OpenAI, OpenRouter, local models)
"""

from .api import Loop, arun, astream, run, stream
from .core_tools import (
    ALL_TOOLS,
    CORE_TOOLS,
    SecurityError,
    bash,
    edit,
    fetch,
    glob,
    grep,
    ls,
    read,
    write,
)
from .structured import ResponseTool
from .tools import LocalTool, tool
from .types import (
    Config,
    DoneEvent,
    ErrorEvent,
    Response,
    StructuredOutputEvent,
    TextEvent,
    ThinkingConfig,
    ThinkingEvent,
    ThinkingLevel,
    ToolCallEvent,
    ToolContext,
    ToolResultEvent,
    TurnStartEvent,
    Usage,
    UsageEvent,
)

__all__ = [
    # Core API
    "Loop",
    "run",
    "arun",
    "stream",
    "astream",
    # Tool decorator
    "tool",
    "LocalTool",
    "ResponseTool",
    "ToolContext",
    # Core tools
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "grep",
    "bash",
    "fetch",
    "CORE_TOOLS",
    "ALL_TOOLS",
    "SecurityError",
    # Events
    "TextEvent",
    "ThinkingEvent",
    "ToolCallEvent",
    "ToolResultEvent",
    "UsageEvent",
    "TurnStartEvent",
    "ErrorEvent",
    "DoneEvent",
    "StructuredOutputEvent",
    # Config & Response
    "Config",
    "ThinkingLevel",
    "ThinkingConfig",
    "Response",
    "Usage",
]
