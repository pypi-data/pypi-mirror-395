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
- **Multiple Providers** - Anthropic, OpenAI, OpenRouter, Google, Ollama, LM Studio

## Install

```bash
uv pip install innerloop
```

## Quick Start

```python
from innerloop import Loop, tool
from pydantic import BaseModel

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: 72°F, sunny"

loop = Loop(
    model="anthropic/claude-sonnet-4",
    tools=[get_weather],
)

# Simple run
response = loop.run("What's the weather in NYC?")
print(response.text)

# Structured output
class Weather(BaseModel):
    city: str
    temperature: int
    condition: str

response = loop.run(
    "Get the weather in NYC",
    response_format=Weather,
)
print(response.output.temperature)  # 72
```

## Multi-turn Sessions

```python
loop = Loop(model="anthropic/claude-sonnet-4")

with loop.session() as ask:
    ask("My name is Alice")
    response = ask("What's my name?")
    print(response.text)  # "Your name is Alice"
```

## Streaming

```python
from innerloop import Loop, TextEvent

loop = Loop(model="anthropic/claude-sonnet-4")

for event in loop.stream("Tell me a joke"):
    if isinstance(event, TextEvent):
        print(event.text, end="", flush=True)
```

## Configuration

API keys are read from environment variables:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export OPENROUTER_API_KEY="sk-or-..."
export GOOGLE_API_KEY="..."
```

Or pass explicitly:

```python
loop = Loop(
    model="anthropic/claude-sonnet-4",
    api_key="sk-ant-...",
)
```

## Documentation

- [Getting Started](https://botassembly.org/innerloop/getting-started)
- [Tools](https://botassembly.org/innerloop/guides/core-concepts/tools)
- [Sessions](https://botassembly.org/innerloop/guides/core-concepts/sessions)
- [Streaming](https://botassembly.org/innerloop/guides/core-concepts/events)
- [Structured Outputs](https://botassembly.org/innerloop/guides/advanced/structured-outputs)
- [Local Models](https://botassembly.org/innerloop/guides/advanced/local-models)
- [Recipes](https://botassembly.org/innerloop/guides/recipes)
- [API Reference](https://botassembly.org/innerloop/reference/api)

## Development

```bash
uv sync --all-extras
make check  # Lint, format, type check
make test   # Run tests
```

## License

MIT
