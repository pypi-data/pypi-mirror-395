"""
Structured Output

Tool-based structured output using Pydantic models.
Forces the model to call a 'respond' tool with validated schema.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ValidationError

from .types import Tool


class ResponseTool(Tool):
    """
    Special tool for structured output.

    The model is forced to call this tool (via tool_choice).
    The tool's input is validated against the Pydantic schema.
    """

    _output_type: type[BaseModel]

    def __init__(self, output_type: type[BaseModel]):
        # Get schema from Pydantic model
        schema = output_type.model_json_schema()

        # Inline $defs if present (simpler schema)
        if "$defs" in schema:
            schema = _inline_defs(schema)

        super().__init__(
            name="respond",
            description=f"Submit your final response as {output_type.__name__}",
            input_schema=schema,
        )

        object.__setattr__(self, "_output_type", output_type)

    async def execute(self, input: dict[str, Any]) -> tuple[str, bool]:
        """
        Validate and return the structured output.

        Returns:
            ("Success", False) if valid
            (error_message, True) if validation fails
        """
        try:
            self._output_type.model_validate(input)
            return "Success", False
        except ValidationError as e:
            error_msg = f"Validation error: {e}. Fix the errors and call respond again."
            return error_msg, True


def _inline_defs(schema: dict[str, Any]) -> dict[str, Any]:
    """Inline $defs references for simpler schema.

    Recursively resolves all $ref pointers by substituting the
    referenced definitions inline. This produces a schema without
    $defs that LLMs can properly interpret.

    For self-referential schemas (e.g., a Node with child: Node),
    the $ref is preserved to avoid infinite recursion.
    """
    from copy import deepcopy

    if "$defs" not in schema:
        return schema

    defs = schema.get("$defs", {})
    result = deepcopy(schema)
    result.pop("$defs", None)

    def resolve_refs(obj: Any, expanding: frozenset[str] = frozenset()) -> Any:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref_path = obj["$ref"]
                # Parse ref like '#/$defs/Inner'
                if ref_path.startswith("#/$defs/"):
                    def_name = ref_path.split("/")[-1]
                    if def_name in defs:
                        # Cycle detection: skip if already expanding this def
                        if def_name in expanding:
                            return obj  # Preserve $ref to avoid infinite loop
                        # Replace the $ref with the actual definition (resolved)
                        resolved = deepcopy(defs[def_name])
                        return resolve_refs(resolved, expanding | {def_name})
                return obj
            else:
                return {k: resolve_refs(v, expanding) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve_refs(item, expanding) for item in obj]
        return obj

    return resolve_refs(result)


__all__ = [
    "ResponseTool",
    "_inline_defs",
]
