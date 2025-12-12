"""Main CLI application."""

from typing import Optional

import typer

from . import __version__
from .config import load_config
from .output import console
from .logging import setup_logging

# Create main app
app = typer.Typer(
    name="docks",
    help="CLI for managing Docks evaluation runs, datasets, and prebaked images.",
    no_args_is_help=True,
)

# Global state
state = {"profile": "default", "verbose": False, "debug": False}


def version_callback(value: bool):
    if value:
        console.print(f"docks version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Config profile to use"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    debug: bool = typer.Option(
        False, "--debug", help="Enable debug output (includes HTTP requests)"
    ),
    version: bool = typer.Option(
        None, "--version", "-V", callback=version_callback, is_eager=True
    ),
):
    """Docks CLI - Manage evaluation runs and datasets."""
    if profile:
        state["profile"] = profile
    state["verbose"] = verbose
    state["debug"] = debug

    # Setup logging based on flags
    setup_logging(verbose=verbose, debug=debug)


# Import and register command groups
from .commands import auth, runs, datasets, images

app.add_typer(auth.app, name="auth", help="Authentication commands")
app.add_typer(runs.app, name="runs", help="Run management commands")
app.add_typer(datasets.app, name="datasets", help="Dataset management commands")
app.add_typer(images.app, name="images", help="Prebaked image commands")


# Convenience commands at root level
@app.command()
def run(
    template: str = typer.Argument(..., help="Template ID or name"),
    provider: str = typer.Option("anthropic", "--provider", "-p", help="Provider name"),
    params: Optional[list[str]] = typer.Option(
        None, "--param", help="Parameters as key=value pairs"
    ),
):
    """Create and launch a new evaluation run."""
    from .commands.runs import create_run

    create_run(template, provider, params)


@app.command()
def status():
    """Show current configuration and auth status."""
    from .commands.auth import status as auth_status

    auth_status()


if __name__ == "__main__":
    app()
