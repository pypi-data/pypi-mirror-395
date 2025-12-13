"""Dataset management commands."""

from pathlib import Path
from typing import Optional

import typer

from ..api import DocksAPI, APIError
from ..datasets import DATASET_ALIASES, resolve_dataset_uri, list_available_datasets
from ..output import (
    console,
    print_datasets_table,
    print_tasks_table,
    print_error,
    print_success,
    print_info,
)

app = typer.Typer()


def get_api(debug: bool = False) -> DocksAPI:
    """Get configured API client."""
    from ..cli import state

    try:
        return DocksAPI.from_config(profile=state.get("profile", "default"), debug=debug)
    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("list")
def list_datasets(
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """List all datasets."""
    api = get_api(debug=debug)

    try:
        datasets = api.list_datasets()

        if not datasets:
            console.print("[dim]No datasets found[/dim]")
            return

        print_datasets_table(datasets)

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("get")
def get_dataset(
    dataset_id: str = typer.Argument(..., help="Dataset ID"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Get details of a specific dataset."""
    api = get_api(debug=debug)

    try:
        ds = api.get_dataset(dataset_id)

        console.print(f"[cyan]Dataset:[/cyan] {ds.get('name')}")
        console.print(f"  ID:       {ds.get('id')}")
        console.print(f"  Version:  {ds.get('version')}")
        console.print(f"  URI:      {ds.get('uri')}")
        console.print(f"  Created:  {ds.get('created_at')}")

        if ds.get("metadata"):
            console.print(f"  Metadata: {ds.get('metadata')}")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("tasks")
def list_tasks(
    dataset_id: str = typer.Argument(..., help="Dataset ID"),
    difficulty: Optional[str] = typer.Option(
        None, "--difficulty", "-d", help="Filter by difficulty"
    ),
    role: Optional[str] = typer.Option(
        None, "--role", "-r", help="Filter by agent role"
    ),
    limit: int = typer.Option(50, "--limit", "-n", help="Number of tasks to show"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """List tasks in a dataset."""
    api = get_api(debug=debug)

    try:
        tasks = api.list_tasks(dataset_id)

        # Apply filters
        if difficulty:
            tasks = [t for t in tasks if t.get("difficulty") == difficulty]
        if role:
            tasks = [t for t in tasks if t.get("agent_role") == role]

        tasks = tasks[:limit]

        if not tasks:
            console.print("[dim]No tasks found[/dim]")
            return

        print_tasks_table(tasks)
        console.print(f"\n[dim]Showing {len(tasks)} tasks[/dim]")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("sync")
def sync_dataset(
    manifest_file: Path = typer.Argument(..., help="Path to YAML manifest file"),
    replace: bool = typer.Option(
        False, "--replace", "-r", help="Replace existing tasks"
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """
    Sync dataset from YAML manifest file.

    Example:
        docks datasets sync manifests/datasets/swebench-v1.yaml --replace
    """
    if not manifest_file.exists():
        print_error(f"File not found: {manifest_file}")
        raise typer.Exit(1)

    api = get_api(debug=debug)

    try:
        manifest_content = manifest_file.read_text()

        # Use internal _request_json for seed endpoint (not in standard API)
        result = api._request_json(
            "POST",
            "/datasets/seed",
            json={"manifest": manifest_content, "replace": replace},
        )

        print_success(f"Dataset synced: {result.get('dataset_id')}")
        console.print(f"  Tasks created:  {result.get('tasks_created', 0)}")
        console.print(f"  Tasks replaced: {result.get('tasks_replaced', 0)}")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("create")
def create_dataset(
    name: str = typer.Option(..., "--name", "-n", help="Dataset name"),
    version: str = typer.Option(..., "--version", "-v", help="Dataset version"),
    uri: str = typer.Option(..., "--uri", "-u", help="Dataset URI (GCS path)"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Create a new empty dataset."""
    api = get_api(debug=debug)

    try:
        # Use internal _request_json for create endpoint
        ds = api._request_json(
            "POST",
            "/datasets",
            json={"name": name, "version": version, "uri": uri},
        )

        print_success(f"Dataset created: {ds['id']}")
        console.print(f"  Name:    {ds.get('name')}")
        console.print(f"  Version: {ds.get('version')}")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("aliases")
def list_aliases():
    """
    List available datasets for use with eval-run.

    Shows all available dataset names you can use with the -d/--dataset option
    in eval-run command instead of full GCS URIs. Includes both explicit aliases
    and datasets discovered from the GCS bucket.

    Example:
        docks runs eval-run -n "Test" -d swebench -t astropy__astropy-12907
    """
    console.print("\n[bold]Available Datasets[/bold]")
    console.print("[dim]Discovering datasets from GCS bucket...[/dim]\n")

    # Get all datasets (explicit aliases + discovered from GCS)
    all_datasets = list_available_datasets(include_discovered=True)

    # Separate explicit aliases from discovered datasets
    explicit_alias_names = set(DATASET_ALIASES.keys())

    # Group by URI to show aliases pointing to same dataset
    uri_to_names: dict[str, list[str]] = {}
    for name, uri in all_datasets.items():
        if uri not in uri_to_names:
            uri_to_names[uri] = []
        uri_to_names[uri].append(name)

    # Show explicit aliases first
    console.print("[bold cyan]Explicit Aliases:[/bold cyan]")
    shown_uris = set()
    for uri, names in sorted(uri_to_names.items()):
        # Check if any name is an explicit alias
        alias_names = [n for n in names if n in explicit_alias_names]
        if alias_names:
            names_sorted = sorted(alias_names)
            primary = names_sorted[0]
            alternatives = names_sorted[1:]

            console.print(f"  [green]{primary}[/green]")
            if alternatives:
                console.print(f"    aliases: {', '.join(alternatives)}")
            shown_uris.add(uri)

    # Show discovered datasets
    console.print("\n[bold cyan]Available Datasets (from GCS):[/bold cyan]")
    discovered_count = 0
    for uri, names in sorted(uri_to_names.items()):
        # Only show datasets not covered by explicit aliases
        non_alias_names = [n for n in names if n not in explicit_alias_names]
        if non_alias_names:
            for name in sorted(non_alias_names):
                console.print(f"  [green]{name}[/green]")
                discovered_count += 1

    if discovered_count == 0:
        console.print("  [dim](No additional datasets discovered)[/dim]")

    console.print()
    console.print("[dim]Use any name with: docks runs eval-run -d <name> ...[/dim]")
    console.print("[dim]Convention: Any folder name in gs://izumi-harbor-datasets/ works automatically.[/dim]\n")


@app.command("resolve")
def resolve_alias(
    dataset: str = typer.Argument(..., help="Dataset alias or URI to resolve"),
):
    """
    Resolve a dataset alias to its full GCS URI.

    Example:
        docks datasets resolve swebench
    """
    resolved = resolve_dataset_uri(dataset)
    if dataset == resolved:
        console.print(f"[dim]Already a full URI:[/dim] {resolved}")
    else:
        console.print(f"[green]{dataset}[/green] → {resolved}")
