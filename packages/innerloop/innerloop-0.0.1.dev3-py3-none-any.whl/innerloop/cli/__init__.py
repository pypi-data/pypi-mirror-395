"""InnerLoop CLI."""

from __future__ import annotations

import typer

from .run import run_command

app = typer.Typer(
    name="innerloop",
    help="InnerLoop CLI for quick LLM interactions",
    no_args_is_help=True,
)


@app.command(name="run")
def run(
    prompt: str = typer.Argument(..., help="Prompt to execute"),
    model: str = typer.Option(
        "openrouter/z-ai/glm-4.5-air",
        "-m",
        "--model",
        help="Model (e.g., openrouter/z-ai/glm-4.5-air, anthropic/claude-haiku-4-5)",
    ),
    stream: bool = typer.Option(False, "--stream", help="Stream output"),
) -> None:
    """Execute a prompt using InnerLoop."""
    run_command(prompt, model, stream)


def cli() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    cli()


__all__ = ["app", "cli"]
