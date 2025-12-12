"""
Tool System

Tools can be:
1. Python functions decorated with @tool
2. MCP server tools (MCPTool) - deferred to later sprint

All tools implement the Tool interface from types.py.
"""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Callable
from typing import (
    Any,
    Literal,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from pydantic import BaseModel, ValidationError, validate_call

from .types import Tool


class LocalTool(Tool):
    """Tool backed by a Python function."""

    _handler: Callable[..., Any]
    _validated_handler: Callable[..., Any]

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable[..., Any],
    ):
        super().__init__(
            name=name, description=description, input_schema=input_schema
        )
        object.__setattr__(self, "_handler", handler)
        # Wrap handler with Pydantic validation
        # This converts dict args to proper types (including Pydantic models)
        object.__setattr__(self, "_validated_handler", validate_call(handler))

    async def execute(self, input: dict[str, Any]) -> tuple[str, bool]:
        """Execute the tool function.

        Returns:
            (result_string, is_error) tuple

        Note: Uses pydantic.validate_call to ensure input dict
        matches function signature, including Pydantic model conversion.
        """
        try:
            result = self._validated_handler(**input)
            # Handle async functions
            if asyncio.iscoroutine(result):
                result = await result
            return str(result), False
        except ValidationError as e:
            # Pydantic validation failed
            return f"Validation error: {e}", True
        except Exception as e:
            return f"Error: {e}", True


def tool(fn: Callable[..., Any]) -> LocalTool:
    """
    Decorator to create a tool from a Python function.

    Uses type hints to generate JSON Schema.
    Uses docstring as description.

    Example:
        @tool
        def read_file(path: str) -> str:
            '''Read contents of a file.'''
            return Path(path).read_text()

        @tool
        async def fetch_url(url: str) -> str:
            '''Fetch content from a URL.'''
            async with httpx.AsyncClient() as client:
                return (await client.get(url)).text
    """
    # Get type hints (handles forward references)
    try:
        hints = get_type_hints(fn)
    except Exception:
        hints = {}

    sig = inspect.signature(fn)

    # Build JSON Schema from type hints
    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        annotation = hints.get(name, Any)
        prop = _type_to_schema(annotation)

        # Extract description from docstring (Google style)
        prop_desc = _extract_param_doc(fn.__doc__, name)
        if prop_desc:
            prop["description"] = prop_desc

        properties[name] = prop

        if param.default is inspect.Parameter.empty:
            required.append(name)

    # Extract summary from docstring
    description = _extract_summary(fn.__doc__) or f"Call {fn.__name__}"

    return LocalTool(
        name=fn.__name__,
        description=description,
        input_schema={
            "type": "object",
            "properties": properties,
            "required": required,
        },
        handler=fn,
    )


def _type_to_schema(t: type) -> dict[str, Any]:
    """Convert Python type to JSON Schema."""
    origin = get_origin(t)
    args = get_args(t)

    # Handle None type
    if t is type(None):
        return {"type": "null"}

    # Handle Optional[X] (Union[X, None]) - works for both typing.Union and types.UnionType
    if origin is Union or type(t).__name__ == "UnionType":
        non_none_args = [a for a in args if a is not type(None)]
        if len(non_none_args) == 1:
            # Optional[X] -> just schema for X (nullable implied)
            return _type_to_schema(non_none_args[0])
        # Union of multiple types
        return {"anyOf": [_type_to_schema(a) for a in non_none_args]}

    # Handle list[X]
    if origin is list:
        item_type = args[0] if args else Any
        return {"type": "array", "items": _type_to_schema(item_type)}

    # Handle dict[str, X]
    if origin is dict:
        return {"type": "object"}

    # Handle Literal["a", "b"]
    if origin is Literal:
        values = list(args)
        if all(isinstance(v, str) for v in values):
            return {"type": "string", "enum": values}
        elif all(isinstance(v, int) for v in values):
            return {"type": "integer", "enum": values}
        else:
            return {"enum": values}

    # Handle Pydantic models
    if isinstance(t, type) and issubclass(t, BaseModel):
        return t.model_json_schema()

    # Primitives
    type_map: dict[type, dict[str, Any]] = {
        str: {"type": "string"},
        int: {"type": "integer"},
        float: {"type": "number"},
        bool: {"type": "boolean"},
        Any: {},
    }

    return type_map.get(t, {"type": "string"})


def _extract_summary(docstring: str | None) -> str | None:
    """Extract first line of docstring as summary."""
    if not docstring:
        return None
    lines = docstring.strip().split("\n")
    if lines:
        return lines[0].strip()
    return None


def _extract_param_doc(docstring: str | None, param: str) -> str | None:
    """Extract parameter description from Google-style docstring.

    Looks for patterns like:
        param_name: Description text
        param_name (type): Description text
    """
    if not docstring:
        return None

    import re

    # Try Google style: "param_name: description" or "param_name (type): description"
    pattern = rf"^\s*{re.escape(param)}(?:\s*\([^)]*\))?:\s*(.+?)(?:\n|$)"
    match = re.search(pattern, docstring, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Try simpler pattern
    pattern = rf"{re.escape(param)}:\s*(.+?)(?:\n|$)"
    match = re.search(pattern, docstring)
    if match:
        return match.group(1).strip()

    return None


__all__ = [
    "LocalTool",
    "tool",
]
