"""
Loop API

Public interface for InnerLoop v2.
Provides sync and async methods for running agent loops.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
from collections.abc import AsyncIterator, Generator, Iterator
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import Any, TypeVar

from pydantic import BaseModel

from .filesystem import Zone, get_zone_tools
from .loop import execute as loop_execute
from .loop import stream as loop_stream
from .providers import get_provider
from .session import SessionStore
from .structured import ResponseTool
from .types import (
    Config,
    Event,
    Message,
    Response,
    StructuredOutputEvent,
    ThinkingConfig,
    ThinkingLevel,
    Tool,
    ToolResultEvent,
    UserMessage,
)

T = TypeVar("T", bound=BaseModel)


class Loop:
    """
    Agent loop with session management.

    Examples:
        # Simple usage
        loop = Loop(model="anthropic/claude-sonnet-4")
        response = loop.run("Hello!")

        # With tools
        @tool
        def get_weather(city: str) -> str:
            return f"Weather in {city}: 72°F"

        loop = Loop(
            model="anthropic/claude-sonnet-4",
            tools=[get_weather],
        )
        response = loop.run("What's the weather in NYC?")

        # Streaming
        for event in loop.stream("Tell me a story"):
            if isinstance(event, TextEvent):
                print(event.text, end="", flush=True)
    """

    def __init__(
        self,
        model: str,
        tools: list[Tool] | None = None,
        thinking: ThinkingLevel | ThinkingConfig | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        session: str | None = None,
        system: str | None = None,
        include_default_tools: bool = True,
        workdir: Path | str | None = None,
        zone: Zone = Zone.FILE_ONLY,
    ):
        """
        Initialize a Loop.

        Args:
            model: Model string (e.g., "anthropic/claude-haiku-4-5")
            tools: Additional custom tools (optional)
            thinking: Thinking level or config (optional)
            api_key: Explicit API key (optional, uses env var otherwise)
            base_url: Custom base URL (optional, for local models)
            session: Session ID to continue (optional, creates new if None)
            system: System prompt (optional)
            include_default_tools: Include default file/shell tools (default: True)
            workdir: Working directory for file tools (default: current directory).
                     All file operations are jailed to this directory.
            zone: Tool capability zone (default: FILE_ONLY).
                  - FILE_ONLY: read, write, edit, ls, glob
                  - WEB_ONLY: webfetch
                  - CODE_EXEC: bash (dangerous)
                  - STRUCTURED: no tools
                  - UNRESTRICTED: all tools (requires INNERLOOP_ALLOW_UNRESTRICTED=1)
        """
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

        # Set up working directory
        self.workdir = Path(workdir).resolve() if workdir else Path.cwd()
        self.zone = zone

        # Check for unrestricted zone safety
        if zone == Zone.UNRESTRICTED:
            if not os.environ.get("INNERLOOP_ALLOW_UNRESTRICTED"):
                raise ValueError(
                    "Zone.UNRESTRICTED requires INNERLOOP_ALLOW_UNRESTRICTED=1 "
                    "environment variable for safety"
                )

        # Build tool list
        if include_default_tools:
            # Use zone-based tools (jailed to workdir)
            zone_tools = get_zone_tools(zone, self.workdir)
            self.tools = [*zone_tools, *(tools or [])]
        else:
            self.tools = tools or []

        # Configure thinking
        if isinstance(thinking, ThinkingLevel):
            self.thinking: ThinkingConfig | None = ThinkingConfig(
                level=thinking
            )
        else:
            self.thinking = thinking

        # System prompt
        self.system = system

        # Session management
        self._store = SessionStore()
        if session:
            self.session_id = session
            self.messages = self._store.load(session)
        else:
            self.session_id = self._store.new_session_id()
            self.messages = []

        # Get provider
        self._provider = get_provider(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def _build_config(self, **overrides: Any) -> Config:
        """Build config with thinking and system prompt."""
        config = Config(
            system=self.system,
            thinking=self.thinking,
            **overrides,
        )
        return config

    def _save_message(self, message: Message) -> None:
        """Save a message to the session."""
        self._store.append(self.session_id, message)

    async def arun(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        max_retries: int = 3,
    ) -> Response:
        """
        Run a prompt asynchronously.

        Args:
            prompt: User prompt
            response_format: Pydantic model class for structured output (optional).
                            When provided, forces the model to call a 'respond' tool
                            and validates the output against this schema.
            max_tokens: Max tokens override (optional)
            temperature: Temperature override (optional)
            max_retries: Max validation retry attempts for structured output

        Returns:
            Response object. If response_format is provided, response.output
            contains the validated Pydantic model instance.
        """
        # Handle structured output via response_format
        if response_format is not None:
            return await self._arun_structured(
                prompt=prompt,
                output_type=response_format,
                max_tokens=max_tokens,
                temperature=temperature,
                max_retries=max_retries,
            )

        # Add user message
        user_msg = UserMessage(content=prompt)
        self.messages.append(user_msg)
        self._save_message(user_msg)

        # Build config
        config_kwargs: dict[str, Any] = {}
        if max_tokens is not None:
            config_kwargs["max_tokens"] = max_tokens
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        config = self._build_config(**config_kwargs)

        # Execute agent loop
        updated_messages, response = await loop_execute(
            provider=self._provider,
            messages=self.messages,
            tools=self.tools,
            config=config,
        )

        # Update messages and save new ones
        new_messages = updated_messages[len(self.messages) :]
        for msg in new_messages:
            self._save_message(msg)
        self.messages = updated_messages

        # Set session ID on response
        response.session_id = self.session_id

        return response

    async def _arun_structured(
        self,
        prompt: str,
        output_type: type[T],
        max_tokens: int | None = None,
        temperature: float | None = None,
        max_retries: int = 3,
    ) -> Response:
        """
        Internal method for structured output execution.

        Creates a ResponseTool, injects it, forces tool_choice, and validates output.
        """
        # Create respond tool
        respond_tool = ResponseTool(output_type)

        # Add respond to tools temporarily
        original_tools = self.tools
        self.tools = [*original_tools, respond_tool]

        try:
            last_response: Response | None = None

            for attempt in range(max_retries):
                # Use empty prompt on retries (session has context)
                current_prompt = prompt if attempt == 0 else ""

                # Add user message if prompt provided
                if current_prompt:
                    user_msg = UserMessage(content=current_prompt)
                    self.messages.append(user_msg)
                    self._save_message(user_msg)

                # Build config
                config_kwargs: dict[str, Any] = {}
                if max_tokens is not None:
                    config_kwargs["max_tokens"] = max_tokens
                if temperature is not None:
                    config_kwargs["temperature"] = temperature
                config = self._build_config(**config_kwargs)

                # Execute with tool_choice forcing respond
                updated_messages, response = await loop_execute(
                    provider=self._provider,
                    messages=self.messages,
                    tools=self.tools,
                    config=config,
                    tool_choice={"type": "tool", "name": "respond"},
                )

                # Update messages and save new ones
                new_messages = updated_messages[len(self.messages) :]
                for msg in new_messages:
                    self._save_message(msg)
                self.messages = updated_messages

                # Set session ID
                response.session_id = self.session_id
                last_response = response

                # Find the respond tool call
                for tr in response.tool_results:
                    if tr.tool_name == "respond":
                        # If validation passed, set output and return
                        if not tr.is_error:
                            validated = output_type.model_validate(tr.input)
                            response.output = validated
                            return response
                        # Validation failed - error is in session, retry
                        break

            # All retries exhausted
            if last_response is not None:
                # Return response with output=None on failure
                last_response.output = None
                return last_response

            raise ValueError(
                f"Structured output failed after {max_retries} attempts"
            )

        finally:
            # Restore original tools
            self.tools = original_tools

    def run(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        max_retries: int = 3,
    ) -> Response:
        """
        Run a prompt synchronously.

        Args:
            prompt: User prompt
            response_format: Pydantic model class for structured output (optional).
                            When provided, forces the model to call a 'respond' tool
                            and validates the output against this schema.
            max_tokens: Max tokens override (optional)
            temperature: Temperature override (optional)
            max_retries: Max validation retry attempts for structured output

        Returns:
            Response object. If response_format is provided, response.output
            contains the validated Pydantic model instance.
        """
        return asyncio.run(
            self.arun(
                prompt, response_format, max_tokens, temperature, max_retries
            )
        )

    async def astream(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> AsyncIterator[Event]:
        """
        Stream events asynchronously.

        Args:
            prompt: User prompt
            response_format: Pydantic model class for structured output (optional).
                            When provided, yields a StructuredOutputEvent with
                            the validated model after the respond tool is called.
            max_tokens: Max tokens override (optional)
            temperature: Temperature override (optional)

        Yields:
            Event objects. If response_format is provided, includes a
            StructuredOutputEvent with the validated model.
        """
        # Handle structured output via response_format
        if response_format is not None:
            async for event in self._astream_structured(
                prompt=prompt,
                output_type=response_format,
                max_tokens=max_tokens,
                temperature=temperature,
            ):
                yield event
            return

        # Add user message
        user_msg = UserMessage(content=prompt)
        self.messages.append(user_msg)
        self._save_message(user_msg)

        # Build config
        config_kwargs: dict[str, Any] = {}
        if max_tokens is not None:
            config_kwargs["max_tokens"] = max_tokens
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        config = self._build_config(**config_kwargs)

        # Stream events
        async for event in loop_stream(
            provider=self._provider,
            messages=self.messages,
            tools=self.tools,
            config=config,
        ):
            yield event

        # Note: We can't easily track new messages in stream mode
        # The loop.stream function doesn't return messages
        # For now, caller should use arun() if they need message history

    async def _astream_structured(
        self,
        prompt: str,
        output_type: type[T],
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> AsyncIterator[Event]:
        """
        Internal method for streaming structured output.

        Streams events normally and yields a StructuredOutputEvent when
        the respond tool validation succeeds.
        """
        import json

        from .types import ToolCallEvent

        # Create respond tool
        respond_tool = ResponseTool(output_type)

        # Add respond to tools temporarily
        original_tools = self.tools
        self.tools = [*original_tools, respond_tool]

        # Track tool calls to get the input for validation
        pending_respond_calls: dict[str, str] = {}  # id -> input JSON

        try:
            # Add user message
            user_msg = UserMessage(content=prompt)
            self.messages.append(user_msg)
            self._save_message(user_msg)

            # Build config
            config_kwargs: dict[str, Any] = {}
            if max_tokens is not None:
                config_kwargs["max_tokens"] = max_tokens
            if temperature is not None:
                config_kwargs["temperature"] = temperature
            config = self._build_config(**config_kwargs)

            # Stream events with tool_choice forcing respond
            async for event in loop_stream(
                provider=self._provider,
                messages=self.messages,
                tools=self.tools,
                config=config,
                tool_choice={"type": "tool", "name": "respond"},
            ):
                yield event

                # Track respond tool calls
                if (
                    isinstance(event, ToolCallEvent)
                    and event.name == "respond"
                ):
                    pending_respond_calls[event.id] = event.input

                # Check if this is a ToolResultEvent for the respond tool
                if (
                    isinstance(event, ToolResultEvent)
                    and event.tool_name == "respond"
                ):
                    if not event.is_error:
                        # Get the input from the tracked tool call
                        input_json = pending_respond_calls.get(
                            event.tool_use_id, "{}"
                        )
                        try:
                            input_data = json.loads(input_json)
                            validated = output_type.model_validate(input_data)
                            yield StructuredOutputEvent(
                                output=validated,
                                success=True,
                            )
                            # Terminate stream on successful structured output
                            return
                        except (json.JSONDecodeError, Exception):
                            # If parsing fails, still yield but with success=False
                            yield StructuredOutputEvent(
                                output=None,
                                success=False,
                            )
                    else:
                        # Validation failed
                        yield StructuredOutputEvent(
                            output=None,
                            success=False,
                        )

        finally:
            # Restore original tools
            self.tools = original_tools

    def stream(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> Iterator[Event]:
        """
        Stream events synchronously.

        Args:
            prompt: User prompt
            response_format: Pydantic model class for structured output (optional).
                            When provided, yields a StructuredOutputEvent with
                            the validated model after the respond tool is called.
            max_tokens: Max tokens override (optional)
            temperature: Temperature override (optional)

        Yields:
            Event objects. If response_format is provided, includes a
            StructuredOutputEvent with the validated model.
        """
        # Use thread + queue for true sync streaming
        queue: Queue[Event | None] = Queue()
        exception_holder: list[Exception | None] = [None]

        def producer() -> None:
            try:
                event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(event_loop)
                try:

                    async def stream_events() -> None:
                        async for event in self.astream(
                            prompt, response_format, max_tokens, temperature
                        ):
                            queue.put(event)
                        queue.put(None)  # Sentinel

                    event_loop.run_until_complete(stream_events())
                finally:
                    event_loop.close()
            except Exception as e:
                exception_holder[0] = e
                queue.put(None)

        thread = Thread(target=producer, daemon=True)
        thread.start()

        while True:
            item = queue.get()
            if item is None:
                break
            if exception_holder[0]:
                raise exception_holder[0]
            yield item

    @contextlib.contextmanager
    def session(
        self,
    ) -> Generator[Any, None, None]:
        """
        Context manager for multi-turn conversations.

        Yields a callable that runs prompts within the same session.

        Example:
            with loop.session() as ask:
                ask("Remember this word: avocado")
                response = ask("What word did I ask you to remember?")
        """

        def ask(prompt: str, **kwargs: Any) -> Response:
            return self.run(prompt, **kwargs)

        yield ask

    @contextlib.asynccontextmanager
    async def asession(
        self,
    ) -> AsyncIterator[Any]:
        """
        Async context manager for multi-turn conversations.

        Yields a callable that runs prompts within the same session.

        Example:
            async with loop.asession() as ask:
                await ask("Remember this word: avocado")
                response = await ask("What word did I ask you to remember?")
        """

        async def ask(prompt: str, **kwargs: Any) -> Response:
            return await self.arun(prompt, **kwargs)

        yield ask


def run(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    **kwargs: Any,
) -> Response:
    """
    One-shot helper for running a prompt.

    Args:
        prompt: User prompt
        model: Model string (e.g., "openrouter/z-ai/glm-4.5-air")
        response_format: Pydantic model class for structured output (optional)
        **kwargs: Additional Loop arguments (tools, system, etc.)

    Returns:
        Response object. If response_format is provided, response.output
        contains the validated Pydantic model instance.
    """
    return Loop(model=model, **kwargs).run(
        prompt, response_format=response_format
    )


async def arun(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    **kwargs: Any,
) -> Response:
    """
    One-shot async helper for running a prompt.

    Args:
        prompt: User prompt
        model: Model string (e.g., "openrouter/z-ai/glm-4.5-air")
        response_format: Pydantic model class for structured output (optional)
        **kwargs: Additional Loop arguments (tools, system, etc.)

    Returns:
        Response object. If response_format is provided, response.output
        contains the validated Pydantic model instance.
    """
    return await Loop(model=model, **kwargs).arun(
        prompt, response_format=response_format
    )


def stream(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    **kwargs: Any,
) -> Iterator[Event]:
    """
    One-shot helper for streaming events.

    Args:
        prompt: User prompt
        model: Model string (e.g., "openrouter/z-ai/glm-4.5-air")
        response_format: Pydantic model class for structured output (optional)
        **kwargs: Additional Loop arguments (tools, system, etc.)

    Yields:
        Event objects. If response_format is provided, includes a
        StructuredOutputEvent with the validated model.
    """
    yield from Loop(model=model, **kwargs).stream(
        prompt, response_format=response_format
    )


async def astream(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    **kwargs: Any,
) -> AsyncIterator[Event]:
    """
    One-shot async helper for streaming events.

    Args:
        prompt: User prompt
        model: Model string (e.g., "openrouter/z-ai/glm-4.5-air")
        response_format: Pydantic model class for structured output (optional)
        **kwargs: Additional Loop arguments (tools, system, etc.)

    Yields:
        Event objects. If response_format is provided, includes a
        StructuredOutputEvent with the validated model.
    """
    async for event in Loop(model=model, **kwargs).astream(
        prompt, response_format=response_format
    ):
        yield event


__all__ = ["Loop", "run", "arun", "stream", "astream"]
