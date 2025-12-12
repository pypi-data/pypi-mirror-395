"""
Agent Loop

Core tool execution loop: send messages -> process tool calls -> execute -> repeat.
Stateless function design - state passed in/out explicitly.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Callable
from typing import TYPE_CHECKING, Any

from .types import (
    AssistantMessage,
    Config,
    DoneEvent,
    ErrorEvent,
    Event,
    Message,
    Response,
    TextEvent,
    TextPart,
    ThinkingEvent,
    ThinkingPart,
    Tool,
    ToolCallEvent,
    ToolResult,
    ToolResultEvent,
    ToolResultMessage,
    ToolUsePart,
    Usage,
    UsageEvent,
)

if TYPE_CHECKING:
    from .providers.base import Provider


async def execute(
    provider: Provider,
    messages: list[Message],
    tools: list[Tool] | None = None,
    config: Config | None = None,
    tool_choice: dict[str, str] | None = None,
    on_event: Callable[[Event], None] | None = None,
) -> tuple[list[Message], Response]:
    """
    Execute the agent loop.

    Streams from provider, executes tools, repeats until done.

    Args:
        provider: LLM provider to use
        messages: Conversation history (modified in place)
        tools: Available tools (optional)
        config: Execution configuration (optional)
        on_event: Callback for streaming events (optional)

    Returns:
        Tuple of (updated messages, Response object)

    Note: This is a pure function - messages list is copied internally.
    """
    config = config or Config()
    tool_map = {t.name: t for t in (tools or [])}
    all_messages = list(messages)  # Copy to avoid mutating input
    all_tool_results: list[ToolResult] = []
    total_usage = Usage()
    rounds = 0
    final_text_parts: list[str] = []
    final_thinking_parts: list[str] = []
    stop_reason = "end_turn"

    while rounds < config.max_tool_rounds:
        rounds += 1

        # Stream one round from provider
        round_result = await _stream_round(
            provider=provider,
            messages=all_messages,
            tools=tools,
            config=config,
            tool_choice=tool_choice,
            on_event=on_event,
        )

        # Unpack round result
        text_parts = round_result["text_parts"]
        thinking_parts = round_result["thinking_parts"]
        tool_calls = round_result["tool_calls"]
        usage = round_result["usage"]
        stop_reason = round_result["stop_reason"]
        error = round_result["error"]

        # Aggregate
        final_text_parts.extend(text_parts)
        final_thinking_parts.extend(thinking_parts)
        total_usage = total_usage.add(usage)

        # Build assistant message content
        content: list[Any] = []
        if thinking_parts:
            content.append(ThinkingPart(text="".join(thinking_parts)))
        if text_parts:
            content.append(TextPart(text="".join(text_parts)))
        for tc in tool_calls:
            try:
                tool_input = json.loads(tc["input"])
            except json.JSONDecodeError:
                tool_input = {}
            content.append(
                ToolUsePart(id=tc["id"], name=tc["name"], input=tool_input)
            )

        # Add assistant message
        assistant_msg = AssistantMessage(
            content=content,
            model=f"{provider.name}/{provider.model_id}",
        )
        all_messages.append(assistant_msg)

        # Handle error
        if error:
            return all_messages, Response(
                text="".join(final_text_parts),
                thinking=(
                    "".join(final_thinking_parts)
                    if final_thinking_parts
                    else None
                ),
                model=f"{provider.name}/{provider.model_id}",
                session_id="",  # Caller sets this
                usage=total_usage,
                tool_results=all_tool_results,
                stop_reason="error",
            )

        # No tool calls = done
        if not tool_calls:
            break

        # Execute tools in parallel
        tool_results = await _execute_tools(
            tool_calls=tool_calls,
            tool_map=tool_map,
            on_event=on_event,
        )

        # Add tool result messages and track results
        for tc, (result_content, is_error) in zip(
            tool_calls, tool_results, strict=True
        ):
            tool_msg = ToolResultMessage(
                tool_use_id=tc["id"],
                tool_name=tc["name"],
                content=result_content,
                is_error=is_error,
            )
            all_messages.append(tool_msg)

            # Track for response
            try:
                tool_input = json.loads(tc["input"])
            except json.JSONDecodeError:
                tool_input = {}

            all_tool_results.append(
                ToolResult(
                    tool_use_id=tc["id"],
                    tool_name=tc["name"],
                    input=tool_input,
                    output=result_content,
                    is_error=is_error,
                )
            )

    else:
        # Max rounds exceeded
        stop_reason = "max_rounds"

    return all_messages, Response(
        text="".join(final_text_parts),
        thinking=(
            "".join(final_thinking_parts) if final_thinking_parts else None
        ),
        model=f"{provider.name}/{provider.model_id}",
        session_id="",  # Caller sets this
        usage=total_usage,
        tool_results=all_tool_results,
        stop_reason=stop_reason,
    )


async def stream(
    provider: Provider,
    messages: list[Message],
    tools: list[Tool] | None = None,
    config: Config | None = None,
    tool_choice: dict[str, str] | None = None,
) -> AsyncIterator[Event]:
    """
    Stream events from the agent loop.

    Yields events as they arrive, including tool results.

    Args:
        provider: LLM provider to use
        messages: Conversation history
        tools: Available tools (optional)
        config: Execution configuration (optional)

    Yields:
        Event objects
    """
    config = config or Config()
    tool_map = {t.name: t for t in (tools or [])}
    all_messages = list(messages)
    rounds = 0

    while rounds < config.max_tool_rounds:
        rounds += 1
        tool_calls: list[dict[str, str]] = []

        # Stream from provider
        async for event in provider.stream(
            all_messages, tools, config, tool_choice
        ):
            yield event

            if isinstance(event, ToolCallEvent):
                tool_calls.append(
                    {
                        "id": event.id,
                        "name": event.name,
                        "input": event.input,
                    }
                )
            elif isinstance(event, DoneEvent):
                # Check stop reason
                if event.stop_reason != "tool_use":
                    return  # Done

        # No tool calls = done
        if not tool_calls:
            return

        # Build assistant message for context
        content: list[Any] = []
        for tc in tool_calls:
            try:
                tool_input = json.loads(tc["input"])
            except json.JSONDecodeError:
                tool_input = {}
            content.append(
                ToolUsePart(id=tc["id"], name=tc["name"], input=tool_input)
            )

        assistant_msg = AssistantMessage(
            content=content,
            model=f"{provider.name}/{provider.model_id}",
        )
        all_messages.append(assistant_msg)

        # Execute tools in parallel
        results = await _execute_tools(tool_calls, tool_map)

        # Add results and yield events
        for tc, (result_content, is_error) in zip(
            tool_calls, results, strict=True
        ):
            # Yield result event
            yield ToolResultEvent(
                tool_use_id=tc["id"],
                tool_name=tc["name"],
                content=result_content,
                is_error=is_error,
            )

            # Add to messages
            tool_msg = ToolResultMessage(
                tool_use_id=tc["id"],
                tool_name=tc["name"],
                content=result_content,
                is_error=is_error,
            )
            all_messages.append(tool_msg)

    # Max rounds exceeded
    yield ErrorEvent(
        error=f"Max tool rounds ({config.max_tool_rounds}) exceeded"
    )
    yield DoneEvent(stop_reason="max_rounds")


async def _stream_round(
    provider: Provider,
    messages: list[Message],
    tools: list[Tool] | None,
    config: Config,
    tool_choice: dict[str, str] | None,
    on_event: Callable[[Event], None] | None,
) -> dict[str, Any]:
    """Stream one round from the provider and collect results."""
    text_parts: list[str] = []
    thinking_parts: list[str] = []
    tool_calls: list[dict[str, str]] = []
    usage = Usage()
    stop_reason = "end_turn"
    error: str | None = None

    async for event in provider.stream(
        messages, tools, config, tool_choice=tool_choice
    ):
        if on_event:
            on_event(event)

        if isinstance(event, TextEvent):
            text_parts.append(event.text)
        elif isinstance(event, ThinkingEvent):
            thinking_parts.append(event.text)
        elif isinstance(event, ToolCallEvent):
            tool_calls.append(
                {
                    "id": event.id,
                    "name": event.name,
                    "input": event.input,
                }
            )
        elif isinstance(event, UsageEvent):
            usage = usage.add(event)
        elif isinstance(event, ErrorEvent):
            error = event.error
        elif isinstance(event, DoneEvent):
            stop_reason = event.stop_reason

    return {
        "text_parts": text_parts,
        "thinking_parts": thinking_parts,
        "tool_calls": tool_calls,
        "usage": usage,
        "stop_reason": stop_reason,
        "error": error,
    }


async def _execute_tools(
    tool_calls: list[dict[str, str]],
    tool_map: dict[str, Tool],
    on_event: Callable[[Event], None] | None = None,
) -> list[tuple[str, bool]]:
    """Execute tools in parallel.

    Returns:
        List of (result_content, is_error) tuples
    """

    async def run_one(tc: dict[str, str]) -> tuple[str, bool]:
        tool = tool_map.get(tc["name"])
        if tool is None:
            return f"Unknown tool: {tc['name']}", True

        try:
            tool_input = json.loads(tc["input"])
        except json.JSONDecodeError as e:
            return f"Invalid JSON input: {e}", True

        result, is_error = await tool.execute(tool_input)

        # Emit result event if callback provided
        if on_event:
            on_event(
                ToolResultEvent(
                    tool_use_id=tc["id"],
                    tool_name=tc["name"],
                    content=result,
                    is_error=is_error,
                )
            )

        return result, is_error

    # Execute all tools in parallel
    results = await asyncio.gather(*[run_one(tc) for tc in tool_calls])
    return list(results)


__all__ = ["execute", "stream"]
