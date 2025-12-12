"""Dataset management commands."""

from pathlib import Path
from typing import Optional

import typer

from ..config import load_config
from ..client import SyncDocksClient
from ..datasets import DATASET_ALIASES, resolve_dataset_uri
from ..output import (
    console,
    print_datasets_table,
    print_tasks_table,
    print_error,
    print_success,
    print_info,
)

app = typer.Typer()


def get_client() -> SyncDocksClient:
    """Get configured client."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))
    if not settings.tenant_id:
        print_error("Tenant ID not configured. Run: docks auth login")
        raise typer.Exit(1)
    if not settings.token:
        print_error("Token not configured. Run: docks auth login")
        raise typer.Exit(1)
    return SyncDocksClient(settings)


@app.command("list")
def list_datasets():
    """List all datasets."""
    client = get_client()

    try:
        datasets = client.list_datasets()

        if not datasets:
            console.print("[dim]No datasets found[/dim]")
            return

        print_datasets_table(datasets)

    except Exception as e:
        print_error(f"Failed to list datasets: {e}")
        raise typer.Exit(1)


@app.command("get")
def get_dataset(
    dataset_id: str = typer.Argument(..., help="Dataset ID"),
):
    """Get details of a specific dataset."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    import httpx
    from ..config import get_headers

    try:
        url = f"{settings.api_url}/tenants/{settings.tenant_id}/datasets/{dataset_id}"
        with httpx.Client(headers=get_headers(settings), timeout=30.0) as http:
            resp = http.get(url)
            resp.raise_for_status()
            ds = resp.json()

        console.print(f"[cyan]Dataset:[/cyan] {ds.get('name')}")
        console.print(f"  ID:       {ds.get('id')}")
        console.print(f"  Version:  {ds.get('version')}")
        console.print(f"  URI:      {ds.get('uri')}")
        console.print(f"  Created:  {ds.get('created_at')}")

        if ds.get("metadata"):
            console.print(f"  Metadata: {ds.get('metadata')}")

    except Exception as e:
        print_error(f"Failed to get dataset: {e}")
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
):
    """List tasks in a dataset."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    import httpx
    from ..config import get_headers

    try:
        url = f"{settings.api_url}/tenants/{settings.tenant_id}/datasets/{dataset_id}/tasks"
        with httpx.Client(headers=get_headers(settings), timeout=30.0) as http:
            resp = http.get(url)
            resp.raise_for_status()
            tasks = resp.json()

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

    except Exception as e:
        print_error(f"Failed to list tasks: {e}")
        raise typer.Exit(1)


@app.command("sync")
def sync_dataset(
    manifest_file: Path = typer.Argument(..., help="Path to YAML manifest file"),
    replace: bool = typer.Option(
        False, "--replace", "-r", help="Replace existing tasks"
    ),
):
    """
    Sync dataset from YAML manifest file.

    Example:
        docks datasets sync manifests/datasets/swebench-v1.yaml --replace
    """
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    if not manifest_file.exists():
        print_error(f"File not found: {manifest_file}")
        raise typer.Exit(1)

    import httpx
    from ..config import get_headers

    try:
        manifest_content = manifest_file.read_text()

        url = f"{settings.api_url}/tenants/{settings.tenant_id}/datasets/seed"
        with httpx.Client(headers=get_headers(settings), timeout=60.0) as http:
            resp = http.post(
                url,
                json={"manifest": manifest_content, "replace": replace},
            )
            resp.raise_for_status()
            result = resp.json()

        print_success(f"Dataset synced: {result.get('dataset_id')}")
        console.print(f"  Tasks created:  {result.get('tasks_created', 0)}")
        console.print(f"  Tasks replaced: {result.get('tasks_replaced', 0)}")

    except httpx.HTTPStatusError as e:
        print_error(f"API error: {e.response.status_code} - {e.response.text}")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to sync dataset: {e}")
        raise typer.Exit(1)


@app.command("create")
def create_dataset(
    name: str = typer.Option(..., "--name", "-n", help="Dataset name"),
    version: str = typer.Option(..., "--version", "-v", help="Dataset version"),
    uri: str = typer.Option(..., "--uri", "-u", help="Dataset URI (GCS path)"),
):
    """Create a new empty dataset."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    import httpx
    from ..config import get_headers

    try:
        url = f"{settings.api_url}/tenants/{settings.tenant_id}/datasets"
        with httpx.Client(headers=get_headers(settings), timeout=30.0) as http:
            resp = http.post(
                url,
                json={"name": name, "version": version, "uri": uri},
            )
            resp.raise_for_status()
            ds = resp.json()

        print_success(f"Dataset created: {ds['id']}")
        console.print(f"  Name:    {ds.get('name')}")
        console.print(f"  Version: {ds.get('version')}")

    except httpx.HTTPStatusError as e:
        print_error(f"API error: {e.response.status_code} - {e.response.text}")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to create dataset: {e}")
        raise typer.Exit(1)


@app.command("aliases")
def list_aliases():
    """
    List available dataset aliases for use with harbor-run.

    Shows all available dataset names you can use with the -d/--dataset option
    in harbor-run command instead of full GCS URIs.

    Example:
        docks runs harbor-run -n "Test" -d swebench -t astropy__astropy-12907
    """
    console.print("\n[bold]Available Dataset Aliases[/bold]\n")

    # Group aliases by URI to show multiple names pointing to same dataset
    uri_to_aliases: dict[str, list[str]] = {}
    for alias, uri in DATASET_ALIASES.items():
        if uri not in uri_to_aliases:
            uri_to_aliases[uri] = []
        uri_to_aliases[uri].append(alias)

    for uri, aliases in sorted(uri_to_aliases.items()):
        # Show primary alias (first alphabetically) and alternatives
        aliases_sorted = sorted(aliases)
        primary = aliases_sorted[0]
        alternatives = aliases_sorted[1:]

        console.print(f"  [green]{primary}[/green]")
        if alternatives:
            console.print(f"    aliases: {', '.join(alternatives)}")
        console.print(f"    uri: [dim]{uri}[/dim]")
        console.print()

    console.print("[dim]Use any alias with: docks runs harbor-run -d <alias> ...[/dim]")
    console.print("[dim]Full GCS URIs (gs://...) are also accepted.[/dim]\n")


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
