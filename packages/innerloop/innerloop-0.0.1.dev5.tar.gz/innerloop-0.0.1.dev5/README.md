# InnerLoop

[![PyPI](https://img.shields.io/pypi/v/innerloop.svg)](https://pypi.org/project/innerloop/)
[![Python](https://img.shields.io/pypi/pyversions/innerloop.svg)](https://pypi.org/project/innerloop/)
[![License](https://img.shields.io/github/license/botassembly/innerloop.svg)](LICENSE)

**Agents are just LLMs in a loop. InnerLoop makes that loop simple, typed, and secure.**

Pure Python SDK for building LLM agent loops with tools, sessions, and structured outputs.

## Features

- **Pure Python** - No subprocesses, no external CLI dependencies
- **Tool Calling** - `@tool` decorator for custom Python functions
- **Structured Output** - Pydantic model validation with automatic retry
- **Sessions** - Multi-turn conversations with JSONL persistence
- **Streaming** - Sync and async event streaming
- **Multiple Providers** - OpenRouter, Anthropic, OpenAI, Google, Ollama, LM Studio
- **Security** - Zone-based tool isolation with CWD jailing

## Install

```bash
uv pip install innerloop
```

## Quick Start

```python
from innerloop import Loop, tool
from pydantic import BaseModel

# Custom tool
@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

# Create loop
loop = Loop(
    model="openrouter/z-ai/glm-4.5-air",  # Free model
    tools=[calculate],
)

# Run with tool calling
response = loop.run("What is (15 * 7) + 23?")
print(response.text)  # "The result is 128"

# Structured output
class MathResult(BaseModel):
    expression: str
    result: float

response = loop.run(
    "Calculate 15 * 7",
    response_format=MathResult,
)
print(response.output.result)  # 105.0
```

## Configuration

```bash
export OPENROUTER_API_KEY="sk-or-..."  # OpenRouter (free models available)
export ANTHROPIC_API_KEY="sk-ant-..."  # Anthropic
export OPENAI_API_KEY="sk-..."         # OpenAI
```

## Documentation

**[Read the full documentation](https://botassembly.org/innerloop)**

- [Getting Started](https://botassembly.org/innerloop/getting-started) - Installation and first steps
- [Tools & Functions](https://botassembly.org/innerloop/guides/core-concepts/tools) - Creating custom tools
- [Structured Outputs](https://botassembly.org/innerloop/guides/advanced/structured-outputs) - Type-safe responses
- [Sessions](https://botassembly.org/innerloop/guides/core-concepts/sessions) - Multi-turn conversations
- [Streaming](https://botassembly.org/innerloop/guides/core-concepts/events) - Real-time event streaming
- [Providers](https://botassembly.org/innerloop/guides/advanced/providers) - OpenRouter, Anthropic, OpenAI, etc.
- [Local Models](https://botassembly.org/innerloop/guides/advanced/local-models) - Ollama and LM Studio
- [Security](https://botassembly.org/innerloop/guides/advanced/security) - Zones and sandboxing
- [Recipes](https://botassembly.org/innerloop/guides/recipes) - Common patterns
- [API Reference](https://botassembly.org/innerloop/reference/api) - Complete API docs

## Development

```bash
uv sync --all-extras
make check  # Lint, format, type check
make test   # Run tests
```

## License

MIT
