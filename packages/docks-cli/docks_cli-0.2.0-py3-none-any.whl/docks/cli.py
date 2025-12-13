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
from .commands import auth, runs, datasets, images, report, tasks, sandbox

app.add_typer(auth.app, name="auth", help="Authentication commands")
app.add_typer(runs.app, name="runs", help="Run management commands")
app.add_typer(datasets.app, name="datasets", help="Dataset management commands")
app.add_typer(images.app, name="images", help="Prebaked image commands")
app.add_typer(report.app, name="report", help="Generate run reports (TUI and HTML)")
app.add_typer(tasks.app, name="tasks", help="Task creation and validation")
app.add_typer(sandbox.app, name="sandbox", help="Sandbox environment management")


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


@app.command("agent-docs")
def agent_docs(
    path_only: bool = typer.Option(False, "--path", help="Only print the file path"),
):
    """Print agent documentation for AI-assisted CLI usage.

    This outputs structured instructions optimized for LLM agents
    to understand and operate the Docks CLI effectively.
    """
    from pathlib import Path
    import importlib.resources

    # Try to find AGENTS.md in the package
    try:
        # Python 3.9+ way
        agents_md = importlib.resources.files("docks").joinpath("AGENTS.md")
        if agents_md.is_file():
            if path_only:
                console.print(str(agents_md))
            else:
                console.print(agents_md.read_text())
            return
    except (AttributeError, TypeError):
        pass

    # Fallback: look in the package directory
    package_dir = Path(__file__).parent
    agents_md_path = package_dir / "AGENTS.md"

    if agents_md_path.exists():
        if path_only:
            console.print(str(agents_md_path))
        else:
            console.print(agents_md_path.read_text())
    else:
        console.print("[red]AGENTS.md not found in package[/red]")
        console.print(f"Expected at: {agents_md_path}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
