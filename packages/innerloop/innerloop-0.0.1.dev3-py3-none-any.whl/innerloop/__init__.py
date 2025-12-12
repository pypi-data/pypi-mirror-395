"""
InnerLoop SDK

Lightweight Python SDK for building LLM agent loops.

Features:
- Tool calling via @tool decorator
- Structured output with Pydantic
- Session management (JSONL)
- Streaming (sync/async)
- Direct provider APIs (Anthropic, OpenAI, OpenRouter, local models)
- Security: Zone-based tool isolation and CWD jailing
"""

from .api import Loop, arun, astream, run, stream
from .default_tools import (
    DEFAULT_TOOLS,
    bash,
    edit,
    glob,
    ls,
    read,
    webfetch,
    write,
)
from .filesystem import FileSystem, SecurityError, Zone
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
    # Security
    "Zone",
    "FileSystem",
    "SecurityError",
    # Tools
    "tool",
    "LocalTool",
    "ResponseTool",
    # Default tools (legacy - prefer using Zone-based tools)
    "DEFAULT_TOOLS",
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "bash",
    "webfetch",
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
