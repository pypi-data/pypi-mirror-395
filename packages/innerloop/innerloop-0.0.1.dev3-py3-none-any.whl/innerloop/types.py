"""
InnerLoop v2 Types

Provider-agnostic types for messages, events, tools, and configuration.
All types are Pydantic models for validation and serialization.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# =============================================================================
# Content Parts (building blocks for messages)
# =============================================================================


class TextPart(BaseModel):
    """Text content in a message."""

    type: Literal["text"] = "text"
    text: str


class ToolUsePart(BaseModel):
    """Tool call in an assistant message."""

    type: Literal["tool_use"] = "tool_use"
    id: str
    name: str
    input: dict[str, Any]


class ThinkingPart(BaseModel):
    """Extended thinking content (Anthropic, OpenAI reasoning)."""

    type: Literal["thinking"] = "thinking"
    text: str
    signature: str | None = None  # Anthropic cache signature


ContentPart = TextPart | ToolUsePart | ThinkingPart


# =============================================================================
# Messages
# =============================================================================


class UserMessage(BaseModel):
    """Message from the user."""

    role: Literal["user"] = "user"
    content: str
    timestamp: int | None = None


class AssistantMessage(BaseModel):
    """Message from the assistant (model)."""

    role: Literal["assistant"] = "assistant"
    content: list[ContentPart]
    model: str | None = None
    timestamp: int | None = None


class ToolResultMessage(BaseModel):
    """Result of a tool execution."""

    role: Literal["tool_result"] = "tool_result"
    tool_use_id: str
    tool_name: str
    content: str
    is_error: bool = False
    timestamp: int | None = None


Message = UserMessage | AssistantMessage | ToolResultMessage


# =============================================================================
# Events (streaming)
# =============================================================================


class TextEvent(BaseModel):
    """Text chunk from streaming response."""

    type: Literal["text"] = "text"
    text: str


class ThinkingEvent(BaseModel):
    """Thinking chunk from streaming response."""

    type: Literal["thinking"] = "thinking"
    text: str


class ToolCallEvent(BaseModel):
    """Tool call detected during streaming.

    Note: input accumulates as partial JSON during streaming.
    Final input is complete JSON when tool_call_end would be emitted.
    """

    type: Literal["tool_call"] = "tool_call"
    id: str
    name: str
    input: str  # JSON string (may be partial during streaming)


class ToolResultEvent(BaseModel):
    """Tool execution result."""

    type: Literal["tool_result"] = "tool_result"
    tool_use_id: str
    tool_name: str
    content: str
    is_error: bool = False


class UsageEvent(BaseModel):
    """Token usage information."""

    type: Literal["usage"] = "usage"
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0


class ErrorEvent(BaseModel):
    """Error during execution."""

    type: Literal["error"] = "error"
    error: str
    code: str | None = None
    recoverable: bool = False


class DoneEvent(BaseModel):
    """Stream completion."""

    type: Literal["done"] = "done"
    stop_reason: str  # "end_turn", "tool_use", "max_tokens", "error"


class StructuredOutputEvent(BaseModel):
    """Structured output validation result (when using response_format with streaming)."""

    type: Literal["structured_output"] = "structured_output"
    output: Any  # The validated Pydantic model instance
    success: bool = True


Event = (
    TextEvent
    | ThinkingEvent
    | ToolCallEvent
    | ToolResultEvent
    | UsageEvent
    | ErrorEvent
    | DoneEvent
    | StructuredOutputEvent
)


# =============================================================================
# Tool Definition
# =============================================================================


class Tool(BaseModel):
    """Base tool interface.

    Subclasses (LocalTool, MCPTool) implement execute().
    """

    name: str
    description: str
    input_schema: dict[str, Any]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def execute(self, input: dict[str, Any]) -> tuple[str, bool]:
        """Execute the tool.

        Returns:
            tuple of (result_string, is_error)

        Note: Returns tuple instead of raising exceptions (functional style).
        """
        raise NotImplementedError("Subclasses must implement execute()")


# =============================================================================
# Configuration
# =============================================================================


class ThinkingLevel(str, Enum):
    """Provider-agnostic thinking levels."""

    OFF = "off"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ThinkingConfig(BaseModel):
    """Extended thinking configuration."""

    level: ThinkingLevel = ThinkingLevel.OFF
    budget_tokens: int | None = None  # Anthropic override
    summary: str | None = (
        None  # OpenAI override ("auto", "detailed", "concise")
    )


class Config(BaseModel):
    """Loop execution configuration."""

    max_tokens: int = 8192
    temperature: float | None = None
    timeout: float = 120.0
    max_tool_rounds: int = 50
    system: str | None = None
    thinking: ThinkingConfig | None = None


# =============================================================================
# Usage Tracking
# =============================================================================


class Usage(BaseModel):
    """Aggregated token usage across rounds."""

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0

    def add(self, other: Usage | UsageEvent) -> Usage:
        """Add usage from another source. Returns new Usage (immutable)."""
        return Usage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cache_read_tokens=self.cache_read_tokens + other.cache_read_tokens,
            cache_write_tokens=self.cache_write_tokens
            + other.cache_write_tokens,
        )


# =============================================================================
# Tool Result (for Response)
# =============================================================================


class ToolResult(BaseModel):
    """Record of a tool execution."""

    tool_use_id: str
    tool_name: str
    input: dict[str, Any]
    output: str
    is_error: bool = False


# =============================================================================
# Response
# =============================================================================


class Response(BaseModel):
    """Result of a Loop.run() or Loop.arun() call.

    When `response_format` is used, `output` contains the validated Pydantic model.
    Otherwise, `output` is the same as `text`.
    """

    text: str
    output: Any = None  # Structured output (BaseModel) or text
    thinking: str | None = None
    model: str
    session_id: str
    usage: Usage = Field(default_factory=Usage)
    tool_results: list[ToolResult] = Field(default_factory=list)
    stop_reason: str = "end_turn"

    def model_post_init(self, __context: Any) -> None:
        """Set output to text if not explicitly set."""
        if self.output is None:
            object.__setattr__(self, "output", self.text)


# =============================================================================
# Serialization
# =============================================================================


def message_to_dict(msg: Message) -> dict[str, Any]:
    """Convert a Message to a JSON-serializable dict."""
    if isinstance(msg, UserMessage):
        return {
            "role": "user",
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
    elif isinstance(msg, AssistantMessage):
        return {
            "role": "assistant",
            "content": [_part_to_dict(p) for p in msg.content],
            "model": msg.model,
            "timestamp": msg.timestamp,
        }
    elif isinstance(msg, ToolResultMessage):
        return {
            "role": "tool_result",
            "tool_use_id": msg.tool_use_id,
            "tool_name": msg.tool_name,
            "content": msg.content,
            "is_error": msg.is_error,
            "timestamp": msg.timestamp,
        }
    else:
        raise ValueError(f"Unknown message type: {type(msg)}")


def _part_to_dict(part: ContentPart) -> dict[str, Any]:
    """Convert a ContentPart to a dict."""
    if isinstance(part, TextPart):
        return {"type": "text", "text": part.text}
    elif isinstance(part, ToolUsePart):
        return {
            "type": "tool_use",
            "id": part.id,
            "name": part.name,
            "input": part.input,
        }
    elif isinstance(part, ThinkingPart):
        d = {"type": "thinking", "text": part.text}
        if part.signature:
            d["signature"] = part.signature
        return d
    else:
        raise ValueError(f"Unknown part type: {type(part)}")


def dict_to_message(data: dict[str, Any]) -> Message:
    """Convert a dict back to a Message."""
    role = data.get("role")

    if role == "user":
        return UserMessage(
            content=data["content"],
            timestamp=data.get("timestamp"),
        )
    elif role == "assistant":
        content = [_dict_to_part(p) for p in data.get("content", [])]
        return AssistantMessage(
            content=content,
            model=data.get("model"),
            timestamp=data.get("timestamp"),
        )
    elif role == "tool_result":
        return ToolResultMessage(
            tool_use_id=data["tool_use_id"],
            tool_name=data["tool_name"],
            content=data["content"],
            is_error=data.get("is_error", False),
            timestamp=data.get("timestamp"),
        )
    else:
        raise ValueError(f"Unknown role: {role}")


def _dict_to_part(data: dict[str, Any]) -> ContentPart:
    """Convert a dict back to a ContentPart."""
    part_type = data.get("type")

    if part_type == "text":
        return TextPart(text=data["text"])
    elif part_type == "tool_use":
        return ToolUsePart(
            id=data["id"],
            name=data["name"],
            input=data["input"],
        )
    elif part_type == "thinking":
        return ThinkingPart(
            text=data["text"],
            signature=data.get("signature"),
        )
    else:
        raise ValueError(f"Unknown part type: {part_type}")


__all__ = [
    # Content parts
    "TextPart",
    "ToolUsePart",
    "ThinkingPart",
    "ContentPart",
    # Messages
    "UserMessage",
    "AssistantMessage",
    "ToolResultMessage",
    "Message",
    # Events
    "TextEvent",
    "ThinkingEvent",
    "ToolCallEvent",
    "ToolResultEvent",
    "UsageEvent",
    "ErrorEvent",
    "DoneEvent",
    "StructuredOutputEvent",
    "Event",
    # Tool
    "Tool",
    "ToolResult",
    # Config
    "ThinkingLevel",
    "ThinkingConfig",
    "Config",
    # Usage & Response
    "Usage",
    "Response",
    # Serialization
    "message_to_dict",
    "dict_to_message",
]
