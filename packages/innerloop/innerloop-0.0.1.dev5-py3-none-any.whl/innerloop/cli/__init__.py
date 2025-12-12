"""InnerLoop CLI."""

from __future__ import annotations

import typer

from .auth_cmd import auth_remove, auth_set, auth_show
from .config_cmd import init_command, set_config, show_config
from .models_cmd import list_models
from .run import run_command
from .sessions import (
    clear_sessions,
    delete_session,
    list_sessions,
    show_session,
)

app = typer.Typer(
    name="innerloop",
    help="InnerLoop CLI for LLM interactions",
    no_args_is_help=True,
)

# =============================================================================
# Run Command
# =============================================================================


@app.command(name="run")
def run(
    prompt: str = typer.Argument(..., help="Prompt to execute"),
    model: str | None = typer.Option(
        None,
        "-m",
        "--model",
        help="Model or alias (default: from config or openrouter/z-ai/glm-4.5-air)",
    ),
    stream: bool = typer.Option(False, "--stream", help="Stream output"),
    continue_session: bool = typer.Option(
        False,
        "-c",
        "--continue",
        help="Continue a previous session (interactive picker)",
    ),
    continue_id: str | None = typer.Option(
        None,
        "--continue-session",
        help="Continue specific session by ID or list number",
    ),
    yes: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Non-interactive: auto-select most recent session",
    ),
) -> None:
    """Execute a prompt using InnerLoop."""
    run_command(prompt, model, stream, continue_session, continue_id, yes)


# =============================================================================
# Sessions Commands
# =============================================================================

sessions_app = typer.Typer(help="Manage conversation sessions")
app.add_typer(sessions_app, name="sessions")


@sessions_app.callback(invoke_without_command=True)
def sessions_default(
    ctx: typer.Context,
    show_all: bool = typer.Option(False, "--all", "-a", help="Show all sessions"),
    here: bool = typer.Option(
        False, "--here", "-h", help="Only show sessions from current directory"
    ),
) -> None:
    """List recent sessions."""
    if ctx.invoked_subcommand is None:
        list_sessions(show_all=show_all, current_dir_only=here)


@sessions_app.command(name="show")
def sessions_show(
    session_id: str = typer.Argument(..., help="Session ID to show"),
) -> None:
    """Show session contents."""
    show_session(session_id)


@sessions_app.command(name="delete")
def sessions_delete(
    session_id: str = typer.Argument(..., help="Session ID to delete"),
) -> None:
    """Delete a session."""
    delete_session(session_id)


@sessions_app.command(name="clear")
def sessions_clear() -> None:
    """Delete all sessions."""
    clear_sessions()


# =============================================================================
# Auth Commands
# =============================================================================

auth_app = typer.Typer(help="Manage API keys")
app.add_typer(auth_app, name="auth")


@auth_app.callback(invoke_without_command=True)
def auth_default(ctx: typer.Context) -> None:
    """Show configured providers."""
    if ctx.invoked_subcommand is None:
        auth_show()


@auth_app.command(name="set")
def auth_set_cmd(
    provider: str = typer.Argument(..., help="Provider name (e.g., anthropic, openai)"),
    api_key: str | None = typer.Argument(None, help="API key (prompts if omitted)"),
    local: bool = typer.Option(False, "--local", "-l", help="Save to project config"),
) -> None:
    """Set API key for a provider."""
    auth_set(provider, api_key, local)


@auth_app.command(name="show")
def auth_show_cmd() -> None:
    """Show configured providers."""
    auth_show()


@auth_app.command(name="remove")
def auth_remove_cmd(
    provider: str = typer.Argument(..., help="Provider name"),
    local: bool = typer.Option(
        False, "--local", "-l", help="Remove from project config"
    ),
) -> None:
    """Remove API key for a provider."""
    auth_remove(provider, local)


# =============================================================================
# Models Command
# =============================================================================


@app.command(name="models")
def models(
    aliases: bool = typer.Option(False, "--aliases", "-a", help="Show only aliases"),
    provider: str | None = typer.Option(
        None, "--provider", "-p", help="Filter by provider"
    ),
) -> None:
    """List available models and aliases."""
    list_models(show_aliases=aliases, provider_filter=provider)


# =============================================================================
# Config Commands
# =============================================================================

config_app = typer.Typer(help="Manage configuration")
app.add_typer(config_app, name="config")


@config_app.callback(invoke_without_command=True)
def config_default(ctx: typer.Context) -> None:
    """Show effective configuration."""
    if ctx.invoked_subcommand is None:
        show_config()


@config_app.command(name="set")
def config_set_cmd(
    key: str = typer.Argument(..., help="Config key (e.g., default_model)"),
    value: str = typer.Argument(..., help="Value to set"),
    local: bool = typer.Option(False, "--local", "-l", help="Save to project config"),
) -> None:
    """Set a configuration value."""
    set_config(key, value, local)


# =============================================================================
# Init Command
# =============================================================================


@app.command(name="init")
def init() -> None:
    """Initialize project-local configuration."""
    init_command()


# =============================================================================
# Entry Point
# =============================================================================


def cli() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    cli()


__all__ = ["app", "cli"]
