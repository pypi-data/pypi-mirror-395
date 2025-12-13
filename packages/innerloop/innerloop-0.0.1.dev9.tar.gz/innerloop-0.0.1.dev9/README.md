# InnerLoop

[![PyPI](https://img.shields.io/pypi/v/innerloop.svg)](https://pypi.org/project/innerloop/)
[![Python](https://img.shields.io/pypi/pyversions/innerloop.svg)](https://pypi.org/project/innerloop/)
[![License](https://img.shields.io/github/license/botassembly/innerloop.svg)](LICENSE)

**Pure Python SDK for LLM agent loops.**

```bash
pip install innerloop
```

## One-liner

```python
from innerloop import run

response = run("What is 2+2?", model="openai/gpt-4o-mini")
print(response.text)  # "4"
```

## Tools are just functions

```python
from innerloop import Loop, tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: 72°F"

loop = Loop(model="anthropic/claude-sonnet-4", tools=[get_weather])
response = loop.run("What's the weather in NYC?")
```

## Any provider, same API

```python
loop = Loop(model="anthropic/claude-sonnet-4")
loop = Loop(model="openai/gpt-4o")
loop = Loop(model="google/gemini-2.0-flash")
loop = Loop(model="openrouter/meta-llama/llama-3.1-8b-instruct:free")  # Free
loop = Loop(model="ollama/llama3")  # Local
```

## System prompt

```python
loop = Loop(
    model="anthropic/claude-sonnet-4",
    system="You are a helpful coding assistant. Be concise.",
)
```

## Structured output with Pydantic

```python
from pydantic import BaseModel
from innerloop import Loop

class City(BaseModel):
    name: str
    country: str
    population: int

loop = Loop(model="openai/gpt-4o")
response = loop.run("Tell me about Tokyo", response_format=City)
print(response.output.model_dump())
# {'name': 'Tokyo', 'country': 'Japan', 'population': 13929286}
```

If validation fails, it automatically retries (up to 3 times).

## Sessions without a database

```python
loop = Loop(model="anthropic/claude-sonnet-4")

with loop.session() as ask:
    ask("Remember: the secret word is 'banana'")
    response = ask("What's the secret word?")

print(response.session_id)  # "20251207144323-SA9MWJ"
```

Conversations save to `~/.local/share/innerloop/sessions/`. Resume anytime:

```python
loop = Loop(model="...", session="20251207144323-SA9MWJ")
```

## Streaming

```python
from innerloop import Loop, TextEvent

loop = Loop(model="anthropic/claude-sonnet-4")

for event in loop.stream("Write a poem"):
    if isinstance(event, TextEvent):
        print(event.text, end="", flush=True)
```

## Async

```python
import asyncio
from innerloop import Loop

async def main():
    loop = Loop(model="anthropic/claude-sonnet-4")
    response = await loop.arun("Hello!")

    async for event in loop.astream("Write a story"):
        ...

asyncio.run(main())
```

## Built-in tools

```python
from innerloop import Loop, SAFE_FS_TOOLS, FS_TOOLS, WEB_TOOLS

# SAFE_FS_TOOLS: read, glob, ls, grep (read-only)
# FS_TOOLS: read, write, edit, glob, ls, grep
# WEB_TOOLS: fetch, download, search

loop = Loop(model="...", tools=FS_TOOLS)
loop.run("Read main.py and add type hints")
```

Constrain bash for safety:

```python
from innerloop import bash

safe_bash = bash(allow={"make": "Run builds"}, deny=["rm -rf", "sudo"])
loop = Loop(model="...", tools=[safe_bash])
```

## Response details

```python
response = loop.run("What's 2+2?")

response.text           # "4"
response.usage          # Usage(input_tokens=12, output_tokens=5)
response.tool_results   # List of tool calls and outputs
response.session_id     # "20251207144323-SA9MWJ"
```

## Documentation

- [Getting Started](docs/getting-started.md)
- [Custom Tools](docs/custom-tools.md)
- [Structured Output](docs/structured-output.md)
- [Sessions](docs/sessions.md)
- [Streaming](docs/streaming.md)
- [Providers](docs/providers.md)
- [Built-in Tools](docs/builtin-tools.md)
- [Bash Tool](docs/bash.md)
- [Configuration](docs/configuration.md)

## License

MIT
