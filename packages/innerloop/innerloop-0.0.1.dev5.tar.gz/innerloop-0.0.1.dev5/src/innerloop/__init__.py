"""
InnerLoop SDK

Lightweight Python SDK for building LLM agent loops.

Features:
- Tool calling via @tool decorator
- Structured output with Pydantic
- Session management (JSONL)
- Streaming (sync/async)
- Direct provider APIs (Anthropic, OpenAI, OpenRouter, local models)
- Built-in tools with workdir jailing
"""

from .api import Loop, arun, astream, run, stream
from .builtin_tools import (
    ALL_TOOLS,
    DEFAULT_TOOLS,
    SecurityError,
    bash,
    edit,
    glob,
    grep,
    ls,
    read,
    webfetch,
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
    ThinkingEvent,
    ThinkingLevel,
    ToolCallEvent,
    ToolResultEvent,
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
    # Tools
    "tool",
    "LocalTool",
    "ResponseTool",
    # Built-in tools
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "grep",
    "bash",
    "webfetch",
    "DEFAULT_TOOLS",
    "ALL_TOOLS",
    "SecurityError",
    # Events
    "TextEvent",
    "ThinkingEvent",
    "ToolCallEvent",
    "ToolResultEvent",
    "UsageEvent",
    "ErrorEvent",
    "DoneEvent",
    "StructuredOutputEvent",
    # Config & Response
    "Config",
    "ThinkingLevel",
    "Response",
    "Usage",
]
