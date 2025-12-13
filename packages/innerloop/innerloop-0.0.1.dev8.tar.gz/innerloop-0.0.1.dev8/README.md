# InnerLoop

[![PyPI](https://img.shields.io/pypi/v/innerloop.svg)](https://pypi.org/project/innerloop/)
[![Python](https://img.shields.io/pypi/pyversions/innerloop.svg)](https://pypi.org/project/innerloop/)
[![License](https://img.shields.io/github/license/botassembly/innerloop.svg)](LICENSE)

**Pure Python SDK for LLM agent loops with tools, sessions, and structured outputs.**

## Install

```bash
pip install innerloop
```

## Quick Example

```python
from innerloop import Loop, tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: 72°F, sunny"

loop = Loop(
    model="anthropic/claude-sonnet-4",
    tools=[get_weather],
)

response = loop.run("What's the weather in NYC?")
print(response.text)
```

## Features

- **Tools** - `@tool` decorator for Python functions
- **Structured Output** - Pydantic validation with automatic retry
- **Sessions** - Multi-turn conversations with JSONL persistence
- **Streaming** - Sync and async event streaming
- **Providers** - Anthropic, OpenAI, Google, OpenRouter, Ollama, LM Studio

## Documentation

Full documentation in [docs/](docs/):

- [Getting Started](docs/getting-started.md) - Installation and first steps
- [Configuration](docs/configuration.md) - All configuration options
- [Providers](docs/providers.md) - Cloud and local LLM providers
- [Tools](docs/tools.md) - Creating custom tools
- [Structured Output](docs/structured-output.md) - Pydantic models
- [Sessions](docs/sessions.md) - Multi-turn conversations
- [Streaming](docs/streaming.md) - Events and async patterns

## Development

```bash
uv sync --all-extras
make check  # Lint, format, type check
make test   # Run tests
```

## License

MIT
