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
from .structured import ResponseTool
from .tooling import (
    # Base
    LocalTool,
    ToolContext,
    tool,
    # Bash (curryable)
    bash,
    BashTool,
    BashConfig,
    # Filesystem tools
    read,
    write,
    edit,
    glob,
    ls,
    grep,
    FS_TOOLS,
    SAFE_FS_TOOLS,
    SecurityError,
    # Todo tools
    TodoState,
    Todo,
    Status,
    make_todo_tools,
    rehydrate_from_session,
    add_todo,
    list_todos,
    mark_done,
    mark_skip,
    TODO_TOOLS,
    # Web tools
    fetch,
    download,
    search,
    WEB_TOOLS,
    # Bundles
    ALL_TOOLS,
)
from .types import (
    Config,
    DoneEvent,
    ErrorEvent,
    MessageEvent,
    Response,
    StructuredOutputEvent,
    TextEvent,
    ThinkingConfig,
    ThinkingEvent,
    ThinkingLevel,
    ToolCallEvent,
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
    # Bash (curryable)
    "bash",
    "BashTool",
    "BashConfig",
    # Filesystem tools
    "read",
    "write",
    "edit",
    "glob",
    "ls",
    "grep",
    "FS_TOOLS",
    "SAFE_FS_TOOLS",
    "SecurityError",
    # Todo tools
    "TodoState",
    "Todo",
    "Status",
    "make_todo_tools",
    "rehydrate_from_session",
    "add_todo",
    "list_todos",
    "mark_done",
    "mark_skip",
    "TODO_TOOLS",
    # Web tools
    "fetch",
    "download",
    "search",
    "WEB_TOOLS",
    # Bundles
    "ALL_TOOLS",
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
    "MessageEvent",
    # Config & Response
    "Config",
    "ThinkingLevel",
    "ThinkingConfig",
    "Response",
    "Usage",
]
