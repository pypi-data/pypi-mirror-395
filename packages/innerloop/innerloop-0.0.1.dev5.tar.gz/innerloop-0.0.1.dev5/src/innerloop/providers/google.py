"""
Google Provider

Implements streaming for Gemini models via the Google Generative AI SDK.
Handles:
- Message format conversion
- Tool calls with streaming
- Safety settings
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
    import google.generativeai as genai


class GoogleProvider(Provider):
    """Google Gemini provider."""

    def __init__(
        self,
        model_id: str,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        self._model_id = model_id
        self._api_key = api_key
        self._base_url = base_url  # Not used, but kept for interface consistency
        self._client: genai.GenerativeModel | None = None

    @property
    def name(self) -> str:
        return "google"

    @property
    def model_id(self) -> str:
        return self._model_id

    def _get_client(self) -> genai.GenerativeModel:
        """Lazy-load the Gemini client."""
        if self._client is None:
            import google.generativeai as genai

            if self._api_key:
                genai.configure(api_key=self._api_key)

            self._client = genai.GenerativeModel(self._model_id)
        return self._client

    async def stream(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        config: Config | None = None,
        tool_choice: dict[str, str] | None = None,
    ) -> AsyncIterator[Event]:
        """Stream a response from Google Gemini."""
        import google.generativeai as genai
        from google.api_core import exceptions as google_exceptions

        config = config or Config()
        model = self._get_client()

        # Convert messages to Gemini format
        history, last_content = _convert_messages(messages, config.system)

        # Build generation config
        generation_config = genai.GenerationConfig(
            max_output_tokens=config.max_tokens,
        )
        if config.temperature is not None:
            generation_config.temperature = config.temperature

        # Build tool config
        gemini_tools = None
        if tools:
            gemini_tools = _convert_tools(tools)
            # Respect forced tool selection by restricting allowed functions
            if tool_choice and tool_choice.get("name"):
                tool_config = genai.protos.ToolConfig(
                    function_calling_config=genai.protos.FunctionCallingConfig(
                        mode=genai.protos.FunctionCallingConfig.Mode.ANY,
                        allowed_function_names=[tool_choice["name"]],
                    )
                )
            else:
                tool_config = None
        else:
            tool_config = None

        try:
            # Create chat with history
            chat = model.start_chat(history=history)

            # Stream the response
            response = await chat.send_message_async(
                last_content,
                generation_config=generation_config,
                tools=gemini_tools,
                tool_config=tool_config,
                stream=True,
            )

            input_tokens = 0
            output_tokens = 0

            async for chunk in response:
                # Handle text content and function calls
                if chunk.candidates:
                    for candidate in chunk.candidates:
                        if candidate.content and candidate.content.parts:
                            for part in candidate.content.parts:
                                if hasattr(part, "text") and part.text:
                                    yield TextEvent(text=part.text)
                                if (
                                    hasattr(part, "function_call")
                                    and part.function_call
                                ):
                                    fc = part.function_call
                                    # Convert args to JSON string
                                    args_dict = dict(fc.args) if fc.args else {}
                                    yield ToolCallEvent(
                                        id=f"call_{fc.name}",
                                        name=fc.name,
                                        input=json.dumps(args_dict),
                                    )

                # Extract usage if available
                if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                    usage = chunk.usage_metadata
                    input_tokens = getattr(usage, "prompt_token_count", 0)
                    output_tokens = getattr(usage, "candidates_token_count", 0)

            # Emit usage
            yield UsageEvent(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

            # Determine stop reason
            stop_reason = "end_turn"
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call") and part.function_call:
                            stop_reason = "tool_use"
                            break

            yield DoneEvent(stop_reason=stop_reason)

        except google_exceptions.GoogleAPIError as e:
            yield ErrorEvent(
                error=str(e),
                code=getattr(e, "code", None),
                recoverable=_is_recoverable(e),
            )
            yield DoneEvent(stop_reason="error")


def _convert_messages(
    messages: list[Message], system: str | None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Convert InnerLoop messages to Gemini format.

    Returns (history, last_content) where history is the chat history
    and last_content is the content for the final send_message call.
    """
    import google.generativeai as genai

    history: list[dict[str, Any]] = []

    for msg in messages:
        if isinstance(msg, UserMessage):
            user_parts: list[Any] = [msg.content]
            # Prepend system message to first user message
            if system and not history:
                user_parts = [f"System: {system}\n\n{msg.content}"]
            history.append({"role": "user", "parts": user_parts})

        elif isinstance(msg, AssistantMessage):
            assistant_parts: list[Any] = []
            for part in msg.content:
                if isinstance(part, TextPart):
                    assistant_parts.append(part.text)
                elif isinstance(part, ToolUsePart):
                    # Create function call part
                    assistant_parts.append(
                        genai.protos.Part(
                            function_call=genai.protos.FunctionCall(
                                name=part.name,
                                args=part.input,
                            )
                        )
                    )
            if assistant_parts:
                history.append({"role": "model", "parts": assistant_parts})

        elif isinstance(msg, ToolResultMessage):
            # Function response
            parts = [
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=msg.tool_use_id.replace("call_", ""),
                        response={"result": msg.content},
                    )
                )
            ]
            history.append({"role": "user", "parts": parts})

    # Pop the last user message as it will be sent via send_message
    if history and history[-1]["role"] == "user":
        last = history.pop()
        return history, last["parts"]

    # If no user message at end, return empty content
    return history, []


def _convert_tools(tools: list[Tool]) -> list[Any]:
    """Convert InnerLoop tools to Gemini format."""
    import google.generativeai as genai

    function_declarations = []
    for tool in tools:
        # Convert JSON Schema to Gemini format
        parameters = _convert_schema(tool.input_schema)
        function_declarations.append(
            genai.protos.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=parameters,
            )
        )

    return [genai.protos.Tool(function_declarations=function_declarations)]


def _convert_schema(schema: dict[str, Any]) -> Any:
    """Convert JSON Schema to Gemini Schema format."""
    import google.generativeai as genai

    if not schema:
        return None

    schema_type = schema.get("type", "object")
    type_map = {
        "string": genai.protos.Type.STRING,
        "number": genai.protos.Type.NUMBER,
        "integer": genai.protos.Type.INTEGER,
        "boolean": genai.protos.Type.BOOLEAN,
        "array": genai.protos.Type.ARRAY,
        "object": genai.protos.Type.OBJECT,
    }

    gemini_schema = genai.protos.Schema(
        type=type_map.get(schema_type, genai.protos.Type.OBJECT),
        description=schema.get("description"),
    )

    # Handle properties for objects
    if schema_type == "object" and "properties" in schema:
        gemini_schema.properties = {
            key: _convert_schema(val) for key, val in schema["properties"].items()
        }
        if "required" in schema:
            gemini_schema.required = schema["required"]

    # Handle array items
    if schema_type == "array" and "items" in schema:
        gemini_schema.items = _convert_schema(schema["items"])

    return gemini_schema


def _is_recoverable(error: Exception) -> bool:
    """Check if an error is recoverable."""
    from google.api_core import exceptions as google_exceptions

    if isinstance(error, google_exceptions.ResourceExhausted):
        return True
    if isinstance(error, google_exceptions.ServiceUnavailable):
        return True
    if isinstance(error, google_exceptions.InternalServerError):
        return True
    return False


# Register this provider
register_provider("google", GoogleProvider)


__all__ = ["GoogleProvider"]
