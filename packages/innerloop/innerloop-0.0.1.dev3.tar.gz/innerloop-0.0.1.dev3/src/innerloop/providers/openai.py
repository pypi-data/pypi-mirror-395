"""
OpenAI Provider

Implements streaming for OpenAI models via the OpenAI Python SDK.
Also supports OpenAI-compatible APIs (OpenRouter, Ollama, LM Studio, etc.).

Handles:
- Message format conversion
- Tool calls with partial JSON accumulation
- Reasoning content (o1/o3 models)
- Custom base URLs for compatible servers
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from ..types import (
    AssistantMessage,
    Config,
    DoneEvent,
    ErrorEvent,
    Event,
    Message,
    TextEvent,
    TextPart,
    ThinkingConfig,
    ThinkingEvent,
    ThinkingLevel,
    ThinkingPart,
    Tool,
    ToolCallEvent,
    ToolResultMessage,
    ToolUsePart,
    UsageEvent,
    UserMessage,
)
from . import register_provider
from .base import Provider

if TYPE_CHECKING:
    import openai


class OpenAIProvider(Provider):
    """OpenAI and OpenAI-compatible provider."""

    def __init__(
        self,
        model_id: str,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        self._model_id = model_id
        self._api_key = api_key
        self._base_url = base_url
        self._client: openai.AsyncOpenAI | None = None

    @property
    def name(self) -> str:
        return "openai"

    @property
    def model_id(self) -> str:
        return self._model_id

    def _get_client(self) -> openai.AsyncOpenAI:
        """Lazy-load the OpenAI client."""
        if self._client is None:
            import openai

            kwargs: dict[str, Any] = {}
            if self._api_key:
                kwargs["api_key"] = self._api_key
            if self._base_url:
                kwargs["base_url"] = self._base_url

            # OpenRouter requires extra headers
            if self._base_url and "openrouter.ai" in self._base_url:
                kwargs["default_headers"] = {
                    "HTTP-Referer": "https://github.com/botassembly/innerloop",
                    "X-Title": "InnerLoop",
                }

            self._client = openai.AsyncOpenAI(**kwargs)
        return self._client

    async def stream(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        config: Config | None = None,
        tool_choice: dict[str, str] | None = None,
    ) -> AsyncIterator[Event]:
        """Stream a response from OpenAI."""
        import openai

        config = config or Config()
        client = self._get_client()

        # Convert messages to OpenAI format
        api_messages = _convert_messages(messages, config.system)

        # Build API kwargs
        kwargs: dict[str, Any] = {
            "model": self._model_id,
            "messages": api_messages,
            "stream": True,
        }

        # Some models (gpt-5+) use max_completion_tokens instead of max_tokens
        # Try max_completion_tokens first for newer models
        if (
            "gpt-5" in self._model_id
            or "o1" in self._model_id
            or "o3" in self._model_id
        ):
            kwargs["max_completion_tokens"] = config.max_tokens
        else:
            kwargs["max_tokens"] = config.max_tokens

        if config.temperature is not None:
            kwargs["temperature"] = config.temperature

        # Tools
        if tools:
            kwargs["tools"] = _convert_tools(tools)

        # Tool choice
        if tool_choice:
            kwargs["tool_choice"] = {
                "type": "function",
                "function": {"name": tool_choice.get("name")},
            }

        # Reasoning (for o1/o3 models with thinking)
        thinking_config = config.thinking
        if thinking_config and thinking_config.level != ThinkingLevel.OFF:
            reasoning_param = _build_reasoning_param(thinking_config)
            if reasoning_param:
                kwargs["reasoning"] = reasoning_param

        # Stream the response
        try:
            stream = await client.chat.completions.create(**kwargs)

            # State for accumulating tool calls
            tool_calls_accumulator: dict[int, dict[str, Any]] = {}
            usage_data = {"input": 0, "output": 0}
            stop_reason = "stop"

            async for chunk in stream:
                if not chunk.choices:
                    continue

                choice = chunk.choices[0]
                delta = choice.delta

                # Text content
                if delta.content:
                    yield TextEvent(text=delta.content)

                # Reasoning content (o1/o3 models)
                if (
                    hasattr(delta, "reasoning_content")
                    and delta.reasoning_content
                ):
                    yield ThinkingEvent(text=delta.reasoning_content)

                # Tool calls (streamed as deltas)
                if delta.tool_calls:
                    for tc in delta.tool_calls:
                        idx = tc.index
                        if idx not in tool_calls_accumulator:
                            tool_calls_accumulator[idx] = {
                                "id": tc.id or f"call_{idx}",
                                "name": "",
                                "arguments": "",
                            }

                        if tc.id:
                            tool_calls_accumulator[idx]["id"] = tc.id
                        if tc.function.name:
                            tool_calls_accumulator[idx][
                                "name"
                            ] = tc.function.name
                        if tc.function.arguments:
                            tool_calls_accumulator[idx][
                                "arguments"
                            ] += tc.function.arguments

                # Finish reason
                if choice.finish_reason:
                    stop_reason = _map_stop_reason(choice.finish_reason)

                # Usage (appears in final chunk)
                if chunk.usage:
                    usage_data["input"] = chunk.usage.prompt_tokens
                    usage_data["output"] = chunk.usage.completion_tokens

            # Emit completed tool calls
            for tc in tool_calls_accumulator.values():
                yield ToolCallEvent(
                    id=tc["id"],
                    name=tc["name"],
                    input=tc["arguments"],  # JSON string
                )

            # Emit usage
            yield UsageEvent(
                input_tokens=usage_data["input"],
                output_tokens=usage_data["output"],
            )

            # Done
            yield DoneEvent(stop_reason=stop_reason)

        except openai.APIError as e:
            code = getattr(e, "code", None)
            yield ErrorEvent(
                error=str(e),
                code=str(code) if code else None,
                recoverable=_is_recoverable(e),
            )
            yield DoneEvent(stop_reason="error")


def _convert_messages(
    messages: list[Message], system: str | None
) -> list[dict[str, Any]]:
    """Convert InnerLoop messages to OpenAI format."""
    result: list[dict[str, Any]] = []

    # System message goes first if present
    if system:
        result.append({"role": "system", "content": system})

    for msg in messages:
        if isinstance(msg, UserMessage):
            result.append(
                {
                    "role": "user",
                    "content": msg.content,
                }
            )

        elif isinstance(msg, AssistantMessage):
            content_parts: list[dict[str, Any]] = []
            tool_calls: list[dict[str, Any]] = []

            for part in msg.content:
                if isinstance(part, TextPart):
                    content_parts.append({"type": "text", "text": part.text})
                elif isinstance(part, ThinkingPart):
                    # Convert thinking to text for OpenAI
                    content_parts.append(
                        {"type": "text", "text": f"[Thinking: {part.text}]"}
                    )
                elif isinstance(part, ToolUsePart):
                    tool_calls.append(
                        {
                            "id": part.id,
                            "type": "function",
                            "function": {
                                "name": part.name,
                                "arguments": json.dumps(part.input),
                            },
                        }
                    )

            # Build message
            msg_dict: dict[str, Any] = {"role": "assistant"}
            if content_parts:
                # Concatenate text parts
                text = " ".join(p["text"] for p in content_parts)
                msg_dict["content"] = text
            if tool_calls:
                msg_dict["tool_calls"] = tool_calls

            result.append(msg_dict)

        elif isinstance(msg, ToolResultMessage):
            result.append(
                {
                    "role": "tool",
                    "tool_call_id": msg.tool_use_id,
                    "content": msg.content,
                }
            )

    return result


def _convert_tools(tools: list[Tool]) -> list[dict[str, Any]]:
    """Convert InnerLoop tools to OpenAI format."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            },
        }
        for tool in tools
    ]


def _build_reasoning_param(config: ThinkingConfig) -> dict[str, Any] | None:
    """Build reasoning parameter for OpenAI o1/o3 models."""
    if config.level == ThinkingLevel.OFF:
        return None

    effort_map = {
        ThinkingLevel.LOW: "low",
        ThinkingLevel.MEDIUM: "medium",
        ThinkingLevel.HIGH: "high",
    }

    return {
        "effort": effort_map.get(config.level, "medium"),
        "summary": config.summary or "auto",
    }


def _map_stop_reason(reason: str | None) -> str:
    """Map OpenAI stop reason to InnerLoop format."""
    if reason == "stop":
        return "end_turn"
    elif reason == "tool_calls":
        return "tool_use"
    elif reason == "length":
        return "max_tokens"
    else:
        return reason or "unknown"


def _is_recoverable(error: Exception) -> bool:
    """Check if an error is recoverable."""
    import openai

    if isinstance(error, openai.RateLimitError):
        return True
    if isinstance(error, openai.APIStatusError):
        return error.status_code >= 500
    return False


# Register this provider
register_provider("openai", OpenAIProvider)

# Also register as openrouter (uses same API)
register_provider("openrouter", OpenAIProvider)

# Local model providers (OpenAI-compatible)
register_provider("ollama", OpenAIProvider)
register_provider("lmstudio", OpenAIProvider)


__all__ = ["OpenAIProvider"]
