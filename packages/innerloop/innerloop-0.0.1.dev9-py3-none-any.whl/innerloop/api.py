"""
Loop API

Public interface for InnerLoop.
Provides sync and async methods for running agent loops.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import AsyncIterator, Generator, Iterator
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import Any, TypeVar

from pydantic import BaseModel

from .loop import execute as loop_execute
from .loop import stream as loop_stream
from .providers import get_provider
from .session import SessionStore
from .structured import ResponseTool
from .tooling.todo import TodoState, rehydrate_from_session
from .types import (
    Config,
    Event,
    Message,
    Response,
    StructuredOutputEvent,
    ThinkingConfig,
    ThinkingLevel,
    Tool,
    ToolCallEvent,
    ToolContext,
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
        system: str | None = None,
        workdir: Path | str | None = None,
        session: str | None = None,
        tool_timeout: float | None = None,
        timeout: float = 300.0,
        todo_state: TodoState | None = None,
    ):
        """
        Initialize a Loop.

        Args:
            model: Model string (e.g., "anthropic/claude-sonnet-4").
            tools: List of tools (functions decorated with @tool).
                   Default: [] (no tools).
            thinking: Thinking level or config (optional).
            api_key: Explicit API key (optional, uses env var otherwise).
            base_url: Custom base URL (optional, for local models).
            system: System prompt (optional).
            workdir: Working directory for tools (default: current directory).
            session: Session ID to resume (from a previous response.session_id).
                     If None, creates a new session with auto-generated ID.
            tool_timeout: Timeout in seconds for tool execution.
                         Default: None (auto-computed as 80% of timeout).
            timeout: Total loop execution timeout in seconds (default: 300.0).
            todo_state: Optional TodoState for exit-with-pending-todos prompting.
                       When provided, the loop will prompt the LLM to complete
                       pending todos before exiting.
        """
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

        # Compute tool_timeout: default to 80% of loop timeout, cap at 80%
        if tool_timeout is None:
            self.tool_timeout = timeout * 0.8
        else:
            # Cap tool_timeout at 80% of loop timeout
            self.tool_timeout = min(tool_timeout, timeout * 0.8)

        # Set up working directory
        self.workdir = Path(workdir).resolve() if workdir else Path.cwd()

        # Tools (default to empty list)
        self.tools: list[Tool] = list(tools) if tools else []

        # Configure thinking
        if isinstance(thinking, ThinkingLevel):
            self.thinking: ThinkingConfig | None = ThinkingConfig(level=thinking)
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

        # Todo state for exit prompting
        # If resuming a session and todo_state provided, rehydrate from session
        if todo_state is not None:
            self.todo_state: TodoState | None = todo_state
            # If resuming and state is empty, try to rehydrate from session history
            if session and not todo_state.items:
                rehydrated = rehydrate_from_session(self.messages)
                todo_state.items = rehydrated.items
        else:
            self.todo_state = None

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
        self._store.append(
            self.session_id, message, model=self.model, workdir=self.workdir
        )

    async def arun(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
        timeout: float | None = None,
        max_turns: int | None = None,
        validation_retries: int = 3,
    ) -> Response:
        """
        Run a prompt asynchronously.

        Args:
            prompt: User prompt.
            response_format: Pydantic model class for structured output (optional).
                            When provided, forces the model to call a 'respond' tool
                            and validates the output against this schema.
            max_output_tokens: Maximum tokens in response (default: 8192).
            temperature: Sampling temperature (optional).
            timeout: Total loop timeout in seconds (default: 300.0).
            max_turns: Maximum agent loop iterations (default: 50).
            validation_retries: Max validation retry attempts for structured output.

        Returns:
            Response object. If response_format is provided, response.output
            contains the validated Pydantic model instance.
        """
        # Handle structured output via response_format
        if response_format is not None:
            return await self._arun_structured(
                prompt=prompt,
                output_type=response_format,
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                timeout=timeout,
                max_turns=max_turns,
                validation_retries=validation_retries,
            )

        # Add user message
        user_msg = UserMessage(content=prompt)
        self.messages.append(user_msg)
        self._save_message(user_msg)

        # Build config
        config_kwargs: dict[str, Any] = {}
        if max_output_tokens is not None:
            config_kwargs["max_output_tokens"] = max_output_tokens
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        if timeout is not None:
            config_kwargs["timeout"] = timeout
        if max_turns is not None:
            config_kwargs["max_turns"] = max_turns
        config = self._build_config(**config_kwargs)

        # Create tool context
        tool_context = ToolContext(
            workdir=self.workdir,
            session_id=self.session_id,
            model=self.model,
            tool_timeout=self.tool_timeout,
        )

        # Execute agent loop
        updated_messages, response = await loop_execute(
            provider=self._provider,
            messages=self.messages,
            tools=self.tools,
            config=config,
            context=tool_context,
            todo_state=self.todo_state,
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
        max_output_tokens: int | None = None,
        temperature: float | None = None,
        timeout: float | None = None,
        max_turns: int | None = None,
        validation_retries: int = 3,
    ) -> Response:
        """
        Internal method for structured output execution.

        Creates a ResponseTool, injects it, forces tool_choice, and validates output.
        """
        # Create respond tool and build tools list (without mutating self.tools)
        respond_tool = ResponseTool(output_type)
        tools_with_respond = [*self.tools, respond_tool]

        last_response: Response | None = None

        for attempt in range(validation_retries):
            # Use empty prompt on retries (session has context)
            current_prompt = prompt if attempt == 0 else ""

            # Add user message if prompt provided
            if current_prompt:
                user_msg = UserMessage(content=current_prompt)
                self.messages.append(user_msg)
                self._save_message(user_msg)

            # Build config
            config_kwargs: dict[str, Any] = {}
            if max_output_tokens is not None:
                config_kwargs["max_output_tokens"] = max_output_tokens
            if temperature is not None:
                config_kwargs["temperature"] = temperature
            if timeout is not None:
                config_kwargs["timeout"] = timeout
            if max_turns is not None:
                config_kwargs["max_turns"] = max_turns
            config = self._build_config(**config_kwargs)

            # Create tool context
            tool_context = ToolContext(
                workdir=self.workdir,
                session_id=self.session_id,
                model=self.model,
                tool_timeout=self.tool_timeout,
            )

            # Execute with tool_choice forcing respond
            # Note: todo_state not passed here since we're forcing structured output
            updated_messages, response = await loop_execute(
                provider=self._provider,
                messages=self.messages,
                tools=tools_with_respond,
                config=config,
                tool_choice={"type": "tool", "name": "respond"},
                context=tool_context,
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
            f"Structured output failed after {validation_retries} attempts"
        )

    def run(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
        timeout: float | None = None,
        max_turns: int | None = None,
        validation_retries: int = 3,
    ) -> Response:
        """
        Run a prompt synchronously.

        Args:
            prompt: User prompt.
            response_format: Pydantic model class for structured output (optional).
                            When provided, forces the model to call a 'respond' tool
                            and validates the output against this schema.
            max_output_tokens: Maximum tokens in response (default: 8192).
            temperature: Sampling temperature (optional).
            timeout: Total loop timeout in seconds (default: 300.0).
            max_turns: Maximum agent loop iterations (default: 50).
            validation_retries: Max validation retry attempts for structured output.

        Returns:
            Response object. If response_format is provided, response.output
            contains the validated Pydantic model instance.
        """
        return asyncio.run(
            self.arun(
                prompt,
                response_format,
                max_output_tokens,
                temperature,
                timeout,
                max_turns,
                validation_retries,
            )
        )

    async def astream(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
        timeout: float | None = None,
        max_turns: int | None = None,
        validation_retries: int = 3,
    ) -> AsyncIterator[Event]:
        """
        Stream events asynchronously.

        Args:
            prompt: User prompt.
            response_format: Pydantic model class for structured output (optional).
                            When provided, yields a StructuredOutputEvent with
                            the validated model after the respond tool is called.
            max_output_tokens: Maximum tokens in response (default: 8192).
            temperature: Sampling temperature (optional).
            timeout: Total loop timeout in seconds (default: 300.0).
            max_turns: Maximum agent loop iterations (default: 50).
            validation_retries: Max validation retry attempts for structured output.

        Yields:
            Event objects. If response_format is provided, includes a
            StructuredOutputEvent with the validated model.
        """
        # Handle structured output via response_format
        if response_format is not None:
            async for event in self._astream_structured(
                prompt=prompt,
                output_type=response_format,
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                timeout=timeout,
                max_turns=max_turns,
                validation_retries=validation_retries,
            ):
                yield event
            return

        # Add user message
        user_msg = UserMessage(content=prompt)
        self.messages.append(user_msg)
        self._save_message(user_msg)

        # Build config
        config_kwargs: dict[str, Any] = {}
        if max_output_tokens is not None:
            config_kwargs["max_output_tokens"] = max_output_tokens
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        if timeout is not None:
            config_kwargs["timeout"] = timeout
        if max_turns is not None:
            config_kwargs["max_turns"] = max_turns
        config = self._build_config(**config_kwargs)

        # Create tool context
        tool_context = ToolContext(
            workdir=self.workdir,
            session_id=self.session_id,
            model=self.model,
            tool_timeout=self.tool_timeout,
        )

        # Stream events
        async for event in loop_stream(
            provider=self._provider,
            messages=self.messages,
            tools=self.tools,
            config=config,
            context=tool_context,
            todo_state=self.todo_state,
        ):
            yield event

    async def _astream_structured(
        self,
        prompt: str,
        output_type: type[T],
        max_output_tokens: int | None = None,
        temperature: float | None = None,
        timeout: float | None = None,
        max_turns: int | None = None,
        validation_retries: int = 3,
    ) -> AsyncIterator[Event]:
        """
        Internal method for streaming structured output with retry support.

        Streams events normally and yields a StructuredOutputEvent when
        the respond tool validation succeeds. Retries on validation failure.
        """
        # Create respond tool and build tools list (without mutating self.tools)
        respond_tool = ResponseTool(output_type)
        tools_with_respond = [*self.tools, respond_tool]

        for attempt in range(validation_retries):
            # Use empty prompt on retries (session has context)
            current_prompt = prompt if attempt == 0 else ""

            # Track tool calls to get the input for validation
            pending_respond_calls: dict[str, str] = {}  # id -> input JSON

            # Add user message if prompt provided
            if current_prompt:
                user_msg = UserMessage(content=current_prompt)
                self.messages.append(user_msg)
                self._save_message(user_msg)

            # Build config
            config_kwargs: dict[str, Any] = {}
            if max_output_tokens is not None:
                config_kwargs["max_output_tokens"] = max_output_tokens
            if temperature is not None:
                config_kwargs["temperature"] = temperature
            if timeout is not None:
                config_kwargs["timeout"] = timeout
            if max_turns is not None:
                config_kwargs["max_turns"] = max_turns
            config = self._build_config(**config_kwargs)

            # Create tool context
            tool_context = ToolContext(
                workdir=self.workdir,
                session_id=self.session_id,
                model=self.model,
                tool_timeout=self.tool_timeout,
            )

            validation_failed = False

            # Stream events with tool_choice forcing respond
            async for event in loop_stream(
                provider=self._provider,
                messages=self.messages,
                tools=tools_with_respond,
                config=config,
                tool_choice={"type": "tool", "name": "respond"},
                context=tool_context,
            ):
                yield event

                # Track respond tool calls
                if isinstance(event, ToolCallEvent) and event.name == "respond":
                    pending_respond_calls[event.id] = event.input

                # Check if this is a ToolResultEvent for the respond tool
                if isinstance(event, ToolResultEvent) and event.tool_name == "respond":
                    if not event.is_error:
                        # Get the input from the tracked tool call
                        input_json = pending_respond_calls.get(event.tool_use_id, "{}")
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
                            # Parsing failed, mark for retry
                            validation_failed = True
                    else:
                        # Validation failed, mark for retry
                        validation_failed = True

            # If validation failed and we have retries left, continue loop
            if not validation_failed:
                # No validation attempt occurred, done
                return

        # All retries exhausted
        yield StructuredOutputEvent(
            output=None,
            success=False,
        )

    def stream(
        self,
        prompt: str,
        response_format: type[T] | None = None,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
        timeout: float | None = None,
        max_turns: int | None = None,
        validation_retries: int = 3,
    ) -> Iterator[Event]:
        """
        Stream events synchronously.

        Args:
            prompt: User prompt.
            response_format: Pydantic model class for structured output (optional).
                            When provided, yields a StructuredOutputEvent with
                            the validated model after the respond tool is called.
            max_output_tokens: Maximum tokens in response (default: 8192).
            temperature: Sampling temperature (optional).
            timeout: Total loop timeout in seconds (default: 300.0).
            max_turns: Maximum agent loop iterations (default: 50).
            validation_retries: Max validation retry attempts for structured output.

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
                            prompt,
                            response_format,
                            max_output_tokens,
                            temperature,
                            timeout,
                            max_turns,
                            validation_retries,
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
                # Check for exception before breaking
                if exception_holder[0]:
                    raise exception_holder[0]
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

        # Add stream method to ask
        ask.stream = lambda prompt, **kwargs: self.stream(prompt, **kwargs)

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

                # Streaming also works within the session
                async for event in ask.astream("Tell me more"):
                    ...
        """

        async def ask(prompt: str, **kwargs: Any) -> Response:
            return await self.arun(prompt, **kwargs)

        # Add astream method to ask
        ask.astream = lambda prompt, **kwargs: self.astream(prompt, **kwargs)

        yield ask


def run(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    max_output_tokens: int | None = None,
    temperature: float | None = None,
    timeout: float | None = None,
    max_turns: int | None = None,
    validation_retries: int = 3,
    **kwargs: Any,
) -> Response:
    """
    One-shot helper for running a prompt.

    Args:
        prompt: User prompt.
        model: Model string (e.g., "anthropic/claude-sonnet-4").
        response_format: Pydantic model class for structured output (optional).
        max_output_tokens: Maximum tokens in response (default: 8192).
        temperature: Sampling temperature (optional).
        timeout: Total loop timeout in seconds (default: 300.0).
        max_turns: Maximum agent loop iterations (default: 50).
        validation_retries: Max validation retry attempts for structured output.
        **kwargs: Additional Loop arguments (tools, system, workdir, etc.).

    Returns:
        Response object. If response_format is provided, response.output
        contains the validated Pydantic model instance.
    """
    return Loop(model=model, **kwargs).run(
        prompt,
        response_format=response_format,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        timeout=timeout,
        max_turns=max_turns,
        validation_retries=validation_retries,
    )


async def arun(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    max_output_tokens: int | None = None,
    temperature: float | None = None,
    timeout: float | None = None,
    max_turns: int | None = None,
    validation_retries: int = 3,
    **kwargs: Any,
) -> Response:
    """
    One-shot async helper for running a prompt.

    Args:
        prompt: User prompt.
        model: Model string (e.g., "anthropic/claude-sonnet-4").
        response_format: Pydantic model class for structured output (optional).
        max_output_tokens: Maximum tokens in response (default: 8192).
        temperature: Sampling temperature (optional).
        timeout: Total loop timeout in seconds (default: 300.0).
        max_turns: Maximum agent loop iterations (default: 50).
        validation_retries: Max validation retry attempts for structured output.
        **kwargs: Additional Loop arguments (tools, system, workdir, etc.).

    Returns:
        Response object. If response_format is provided, response.output
        contains the validated Pydantic model instance.
    """
    return await Loop(model=model, **kwargs).arun(
        prompt,
        response_format=response_format,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        timeout=timeout,
        max_turns=max_turns,
        validation_retries=validation_retries,
    )


def stream(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    max_output_tokens: int | None = None,
    temperature: float | None = None,
    timeout: float | None = None,
    max_turns: int | None = None,
    validation_retries: int = 3,
    **kwargs: Any,
) -> Iterator[Event]:
    """
    One-shot helper for streaming events.

    Args:
        prompt: User prompt.
        model: Model string (e.g., "anthropic/claude-sonnet-4").
        response_format: Pydantic model class for structured output (optional).
        max_output_tokens: Maximum tokens in response (default: 8192).
        temperature: Sampling temperature (optional).
        timeout: Total loop timeout in seconds (default: 300.0).
        max_turns: Maximum agent loop iterations (default: 50).
        validation_retries: Max validation retry attempts for structured output.
        **kwargs: Additional Loop arguments (tools, system, workdir, etc.).

    Yields:
        Event objects. If response_format is provided, includes a
        StructuredOutputEvent with the validated model.
    """
    yield from Loop(model=model, **kwargs).stream(
        prompt,
        response_format=response_format,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        timeout=timeout,
        max_turns=max_turns,
        validation_retries=validation_retries,
    )


async def astream(
    prompt: str,
    model: str,
    response_format: type[T] | None = None,
    max_output_tokens: int | None = None,
    temperature: float | None = None,
    timeout: float | None = None,
    max_turns: int | None = None,
    validation_retries: int = 3,
    **kwargs: Any,
) -> AsyncIterator[Event]:
    """
    One-shot async helper for streaming events.

    Args:
        prompt: User prompt.
        model: Model string (e.g., "anthropic/claude-sonnet-4").
        response_format: Pydantic model class for structured output (optional).
        max_output_tokens: Maximum tokens in response (default: 8192).
        temperature: Sampling temperature (optional).
        timeout: Total loop timeout in seconds (default: 300.0).
        max_turns: Maximum agent loop iterations (default: 50).
        validation_retries: Max validation retry attempts for structured output.
        **kwargs: Additional Loop arguments (tools, system, workdir, etc.).

    Yields:
        Event objects. If response_format is provided, includes a
        StructuredOutputEvent with the validated model.
    """
    async for event in Loop(model=model, **kwargs).astream(
        prompt,
        response_format=response_format,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        timeout=timeout,
        max_turns=max_turns,
        validation_retries=validation_retries,
    ):
        yield event


__all__ = ["Loop", "run", "arun", "stream", "astream"]
