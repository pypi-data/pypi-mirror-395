"""
Sandbox management commands for docks CLI.

Provides interactive access to sandbox environments for task debugging.
"""
import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Optional
from uuid import UUID

import typer
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from ..config import load_config

app = typer.Typer(help="Sandbox environment management")
console = Console()


def get_api_client():
    """Get authenticated API client."""
    config = load_config()
    if not config.api_url or not config.token:
        console.print("[red]Not authenticated. Run 'docks auth login' first.[/red]")
        raise typer.Exit(1)
    return config


def make_request(method: str, path: str, **kwargs) -> dict:
    """Make authenticated API request."""
    config = get_api_client()
    url = f"{config.api_url}{path}"
    headers = {"Authorization": f"Bearer {config.token}"}

    with httpx.Client(timeout=60.0) as client:
        response = client.request(method, url, headers=headers, **kwargs)
        if response.status_code >= 400:
            console.print(f"[red]API Error ({response.status_code}): {response.text}[/red]")
            raise typer.Exit(1)
        return response.json()


def get_tenant_id() -> str:
    """Extract tenant_id from JWT token or config."""
    config = get_api_client()

    # First try to get from config directly
    if config.tenant_id:
        return config.tenant_id

    # Fall back to extracting from JWT token
    import base64
    import json
    token = config.token

    # Decode JWT payload (no verification, just extraction)
    parts = token.split(".")
    if len(parts) != 3:
        console.print("[red]Invalid token format[/red]")
        raise typer.Exit(1)

    # Add padding if needed
    payload = parts[1]
    padding = 4 - len(payload) % 4
    if padding != 4:
        payload += "=" * padding

    decoded = base64.urlsafe_b64decode(payload)
    claims = json.loads(decoded)
    return claims.get("tenant") or claims.get("sub")


@app.command()
def create(
    name: str = typer.Argument(..., help="Sandbox name"),
    image: str = typer.Option("python:3.11-slim", "--image", "-i", help="Docker image to use"),
    mode: str = typer.Option("interactive", "--mode", "-m", help="Sandbox mode: interactive or ephemeral"),
    machine_type: str = typer.Option("e2-medium", "--machine", help="Machine type (e2-medium, e2-standard-2, etc.)"),
    timeout: int = typer.Option(60, "--timeout", "-t", help="Timeout in minutes (5-480)"),
    task_path: Optional[Path] = typer.Option(None, "--task", help="Path to task directory to mount"),
    startup_script: Optional[str] = typer.Option(None, "--startup", "-s", help="Startup script to run"),
    wait: bool = typer.Option(True, "--wait/--no-wait", help="Wait for sandbox to be ready"),
):
    """Create a new sandbox environment.

    Creates an interactive sandbox that you can connect to via shell.

    Examples:
        docks sandbox create my-test --image python:3.11
        docks sandbox create django-debug --image django:4.2 --timeout 120
        docks sandbox create swe-task --task ./swebench-lite/django__django-11039
    """
    tenant_id = get_tenant_id()

    # Build sandbox payload
    payload = {
        "name": name,
        "mode": mode,
        "image": image,
        "machine_type": machine_type,
        "timeout_minutes": timeout,
    }

    if startup_script:
        payload["startup_script"] = startup_script

    # If task path provided, read task config and set up accordingly
    if task_path:
        task_yaml = task_path / "task.yaml"
        if task_yaml.exists():
            import yaml
            with open(task_yaml) as f:
                task_data = yaml.safe_load(f)
            console.print(f"[dim]Loading task: {task_data.get('slug', 'unknown')}[/dim]")
            # Could extend to mount task files, set up environment, etc.

    console.print(f"Creating sandbox [cyan]{name}[/cyan]...")

    result = make_request("POST", f"/tenants/{tenant_id}/sandboxes", json=payload)
    sandbox_id = result["id"]

    console.print(f"[green]Sandbox created:[/green] {sandbox_id}")

    if wait:
        console.print("[dim]Waiting for sandbox to be ready...[/dim]")

        with console.status("[bold cyan]Provisioning...") as status:
            max_attempts = 60
            for i in range(max_attempts):
                time.sleep(5)
                sandbox = make_request("GET", f"/tenants/{tenant_id}/sandboxes/{sandbox_id}")
                sandbox_status = sandbox.get("status")

                if sandbox_status == "running":
                    break
                elif sandbox_status in ["failed", "terminated", "error"]:
                    console.print(f"[red]Sandbox failed: {sandbox.get('status_reason', 'Unknown error')}[/red]")
                    raise typer.Exit(1)

                status.update(f"[bold cyan]Provisioning... ({i*5}s, status: {sandbox_status})")

        # Display connection info
        console.print()
        console.print(Panel.fit(
            f"[green]Sandbox is ready![/green]\n\n"
            f"[bold]ID:[/bold] {sandbox_id}\n"
            f"[bold]Status:[/bold] {sandbox.get('status')}\n"
            f"[bold]Expires:[/bold] {sandbox.get('expires_at', 'N/A')}\n"
            f"[bold]Time remaining:[/bold] {sandbox.get('time_remaining_seconds', 'N/A')}s",
            title="Sandbox Ready"
        ))

        # Show exec command if available
        exec_cmd = sandbox.get("exec_command")
        if exec_cmd:
            console.print()
            console.print("[bold]Connect with:[/bold]")
            console.print(f"  [cyan]{exec_cmd}[/cyan]")
            console.print()
            console.print("[dim]Or use: docks sandbox shell " + sandbox_id[:8] + "[/dim]")
        else:
            console.print()
            console.print("[dim]Use: docks sandbox shell " + sandbox_id[:8] + "[/dim]")
    else:
        console.print(f"[dim]Sandbox is provisioning. Check status with: docks sandbox list[/dim]")


@app.command("list")
def list_sandboxes(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum results"),
):
    """List active sandboxes.

    Examples:
        docks sandbox list
        docks sandbox list --status running
    """
    tenant_id = get_tenant_id()

    params = {"limit": limit}
    if status:
        params["status"] = status

    result = make_request("GET", f"/tenants/{tenant_id}/sandboxes", params=params)

    sandboxes = result if isinstance(result, list) else result.get("items", [])

    if not sandboxes:
        console.print("[dim]No sandboxes found.[/dim]")
        return

    table = Table(title="Sandboxes")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Status", style="bold")
    table.add_column("Mode", style="dim")
    table.add_column("Image", style="dim")
    table.add_column("Time Left", style="yellow")

    for sb in sandboxes:
        status_style = {
            "running": "green",
            "provisioning": "yellow",
            "pending": "yellow",
            "failed": "red",
            "terminated": "dim",
            "stopping": "yellow",
        }.get(sb.get("status", ""), "white")

        time_left = sb.get("time_remaining_seconds")
        if time_left:
            mins = time_left // 60
            time_str = f"{mins}m"
        else:
            time_str = "-"

        table.add_row(
            sb["id"][:8],
            sb.get("name", "-"),
            f"[{status_style}]{sb.get('status', '-')}[/{status_style}]",
            sb.get("mode", "-"),
            (sb.get("image", "-") or "-")[:30],
            time_str,
        )

    console.print(table)


@app.command()
def get(
    sandbox_id: str = typer.Argument(..., help="Sandbox ID (full or prefix)"),
):
    """Get details for a specific sandbox.

    Examples:
        docks sandbox get abc12345
        docks sandbox get abc12345-6789-...
    """
    tenant_id = get_tenant_id()

    # If short ID provided, list and find matching
    if len(sandbox_id) < 36:
        sandboxes = make_request("GET", f"/tenants/{tenant_id}/sandboxes", params={"limit": 100})
        if isinstance(sandboxes, dict):
            sandboxes = sandboxes.get("items", [])

        matches = [s for s in sandboxes if s["id"].startswith(sandbox_id)]
        if not matches:
            console.print(f"[red]No sandbox found with ID prefix: {sandbox_id}[/red]")
            raise typer.Exit(1)
        if len(matches) > 1:
            console.print(f"[yellow]Multiple sandboxes match '{sandbox_id}':[/yellow]")
            for m in matches:
                console.print(f"  {m['id'][:8]} - {m.get('name', 'unnamed')}")
            raise typer.Exit(1)
        sandbox_id = matches[0]["id"]

    sandbox = make_request("GET", f"/tenants/{tenant_id}/sandboxes/{sandbox_id}")

    console.print(Panel.fit(
        f"[bold]ID:[/bold] {sandbox['id']}\n"
        f"[bold]Name:[/bold] {sandbox.get('name', '-')}\n"
        f"[bold]Status:[/bold] {sandbox.get('status', '-')}\n"
        f"[bold]Mode:[/bold] {sandbox.get('mode', '-')}\n"
        f"[bold]Image:[/bold] {sandbox.get('image', '-')}\n"
        f"[bold]Machine:[/bold] {sandbox.get('machine_type', '-')}\n"
        f"[bold]Created:[/bold] {sandbox.get('created_at', '-')}\n"
        f"[bold]Expires:[/bold] {sandbox.get('expires_at', '-')}\n"
        f"[bold]Time Left:[/bold] {sandbox.get('time_remaining_seconds', 'N/A')}s\n"
        f"[bold]Zone:[/bold] {sandbox.get('zone', '-')}\n"
        f"[bold]Remote Ref:[/bold] {sandbox.get('remote_ref', '-')}",
        title=f"Sandbox: {sandbox.get('name', sandbox['id'][:8])}"
    ))

    exec_cmd = sandbox.get("exec_command")
    if exec_cmd:
        console.print()
        console.print("[bold]Exec Command:[/bold]")
        console.print(f"  [cyan]{exec_cmd}[/cyan]")


@app.command()
def shell(
    sandbox_id: str = typer.Argument(..., help="Sandbox ID (full or prefix)"),
    command: Optional[str] = typer.Option(None, "-c", "--command", help="Command to run instead of shell"),
):
    """Connect to a sandbox via interactive shell.

    Opens an interactive shell session in the sandbox. Use Ctrl+D or 'exit' to disconnect.

    Examples:
        docks sandbox shell abc12345
        docks sandbox shell abc12345 -c "ls -la"
        docks sandbox shell abc12345 -c "python --version"
    """
    tenant_id = get_tenant_id()

    # Resolve short ID
    if len(sandbox_id) < 36:
        sandboxes = make_request("GET", f"/tenants/{tenant_id}/sandboxes", params={"limit": 100})
        if isinstance(sandboxes, dict):
            sandboxes = sandboxes.get("items", [])

        matches = [s for s in sandboxes if s["id"].startswith(sandbox_id)]
        if not matches:
            console.print(f"[red]No sandbox found with ID prefix: {sandbox_id}[/red]")
            raise typer.Exit(1)
        if len(matches) > 1:
            console.print(f"[yellow]Multiple sandboxes match '{sandbox_id}':[/yellow]")
            for m in matches:
                console.print(f"  {m['id'][:8]} - {m.get('name', 'unnamed')}")
            raise typer.Exit(1)
        sandbox_id = matches[0]["id"]

    # Get sandbox details
    sandbox = make_request("GET", f"/tenants/{tenant_id}/sandboxes/{sandbox_id}")

    if sandbox.get("status") != "running":
        console.print(f"[red]Sandbox is not running (status: {sandbox.get('status')})[/red]")
        if sandbox.get("status") in ["pending", "provisioning"]:
            console.print("[dim]Wait for sandbox to be ready or use --wait when creating[/dim]")
        raise typer.Exit(1)

    exec_cmd = sandbox.get("exec_command")

    if not exec_cmd:
        # Fall back to kubectl exec if we have remote_ref
        remote_ref = sandbox.get("remote_ref")
        zone = sandbox.get("zone")

        if remote_ref and zone:
            # Construct kubectl command for GKE
            console.print("[dim]Constructing kubectl command...[/dim]")
            # Extract pod info from remote_ref (format varies by provider)
            exec_cmd = f"kubectl exec -it {remote_ref} -- /bin/bash"
        else:
            # Try to use exec API for ephemeral sandboxes
            if command:
                console.print(f"[dim]Executing via API: {command}[/dim]")
                result = make_request(
                    "POST",
                    f"/tenants/{tenant_id}/sandboxes/{sandbox_id}/exec",
                    json={"command": command, "timeout_seconds": 300}
                )
                console.print(result.get("stdout", ""))
                if result.get("stderr"):
                    console.print(f"[red]{result.get('stderr')}[/red]", file=sys.stderr)
                raise typer.Exit(result.get("exit_code", 0))
            else:
                console.print("[yellow]No exec_command available for this sandbox.[/yellow]")
                console.print("[dim]Interactive sandboxes require GKE provider.[/dim]")
                console.print()
                console.print("For ephemeral sandboxes, run commands with -c:")
                console.print(f"  docks sandbox shell {sandbox_id[:8]} -c 'ls -la'")
                raise typer.Exit(1)

    # If we have an exec command, run it
    if command:
        # Modify exec_cmd to run specific command
        if "kubectl exec" in exec_cmd:
            # Replace -- /bin/bash with -- {command}
            exec_cmd = exec_cmd.rsplit("--", 1)[0] + f"-- {command}"
        console.print(f"[dim]Running: {exec_cmd}[/dim]")
    else:
        console.print(f"[dim]Connecting to sandbox...[/dim]")
        console.print(f"[dim]Command: {exec_cmd}[/dim]")
        console.print()

    # Execute the shell command
    try:
        result = subprocess.run(exec_cmd, shell=True)
        raise typer.Exit(result.returncode)
    except KeyboardInterrupt:
        console.print("\n[dim]Disconnected.[/dim]")
        raise typer.Exit(0)


@app.command()
def exec(
    sandbox_id: str = typer.Argument(..., help="Sandbox ID (full or prefix)"),
    command: str = typer.Argument(..., help="Command to execute"),
    timeout: int = typer.Option(60, "--timeout", "-t", help="Command timeout in seconds"),
):
    """Execute a command in a sandbox (non-interactive).

    Runs a command and returns the output. For interactive sessions, use 'shell'.

    Examples:
        docks sandbox exec abc12345 "ls -la"
        docks sandbox exec abc12345 "python -c 'print(1+1)'"
        docks sandbox exec abc12345 "pytest tests/" --timeout 300
    """
    tenant_id = get_tenant_id()

    # Resolve short ID
    if len(sandbox_id) < 36:
        sandboxes = make_request("GET", f"/tenants/{tenant_id}/sandboxes", params={"limit": 100})
        if isinstance(sandboxes, dict):
            sandboxes = sandboxes.get("items", [])

        matches = [s for s in sandboxes if s["id"].startswith(sandbox_id)]
        if not matches:
            console.print(f"[red]No sandbox found with ID prefix: {sandbox_id}[/red]")
            raise typer.Exit(1)
        if len(matches) > 1:
            console.print(f"[yellow]Multiple sandboxes match '{sandbox_id}':[/yellow]")
            for m in matches:
                console.print(f"  {m['id'][:8]} - {m.get('name', 'unnamed')}")
            raise typer.Exit(1)
        sandbox_id = matches[0]["id"]

    # Execute command via API
    console.print(f"[dim]Executing: {command}[/dim]")

    result = make_request(
        "POST",
        f"/tenants/{tenant_id}/sandboxes/{sandbox_id}/exec",
        json={"command": command, "timeout_seconds": timeout}
    )

    # Print output
    if result.get("stdout"):
        console.print(result["stdout"])
    if result.get("stderr"):
        console.print(result["stderr"], file=sys.stderr, style="red")

    exit_code = result.get("exit_code", 0)
    duration = result.get("duration_ms", 0)

    console.print(f"[dim]Exit code: {exit_code}, Duration: {duration}ms[/dim]")
    raise typer.Exit(exit_code)


@app.command()
def stop(
    sandbox_id: str = typer.Argument(..., help="Sandbox ID (full or prefix)"),
    force: bool = typer.Option(False, "--force", "-f", help="Force stop without confirmation"),
):
    """Stop and terminate a sandbox.

    Examples:
        docks sandbox stop abc12345
        docks sandbox stop abc12345 --force
    """
    tenant_id = get_tenant_id()

    # Resolve short ID
    if len(sandbox_id) < 36:
        sandboxes = make_request("GET", f"/tenants/{tenant_id}/sandboxes", params={"limit": 100})
        if isinstance(sandboxes, dict):
            sandboxes = sandboxes.get("items", [])

        matches = [s for s in sandboxes if s["id"].startswith(sandbox_id)]
        if not matches:
            console.print(f"[red]No sandbox found with ID prefix: {sandbox_id}[/red]")
            raise typer.Exit(1)
        if len(matches) > 1:
            console.print(f"[yellow]Multiple sandboxes match '{sandbox_id}':[/yellow]")
            for m in matches:
                console.print(f"  {m['id'][:8]} - {m.get('name', 'unnamed')}")
            raise typer.Exit(1)

        sandbox_id = matches[0]["id"]
        sandbox_name = matches[0].get("name", "unnamed")
    else:
        sandbox = make_request("GET", f"/tenants/{tenant_id}/sandboxes/{sandbox_id}")
        sandbox_name = sandbox.get("name", "unnamed")

    if not force:
        confirm = typer.confirm(f"Stop sandbox '{sandbox_name}' ({sandbox_id[:8]})?")
        if not confirm:
            console.print("[dim]Cancelled.[/dim]")
            raise typer.Exit(0)

    console.print(f"Stopping sandbox [cyan]{sandbox_id[:8]}[/cyan]...")

    make_request("POST", f"/tenants/{tenant_id}/sandboxes/{sandbox_id}/stop")

    console.print("[green]Sandbox stopped.[/green]")


@app.command()
def extend(
    sandbox_id: str = typer.Argument(..., help="Sandbox ID (full or prefix)"),
    minutes: int = typer.Option(30, "--minutes", "-m", help="Minutes to extend"),
):
    """Extend sandbox timeout.

    Examples:
        docks sandbox extend abc12345 --minutes 60
    """
    tenant_id = get_tenant_id()

    # Resolve short ID
    if len(sandbox_id) < 36:
        sandboxes = make_request("GET", f"/tenants/{tenant_id}/sandboxes", params={"limit": 100})
        if isinstance(sandboxes, dict):
            sandboxes = sandboxes.get("items", [])

        matches = [s for s in sandboxes if s["id"].startswith(sandbox_id)]
        if not matches:
            console.print(f"[red]No sandbox found with ID prefix: {sandbox_id}[/red]")
            raise typer.Exit(1)
        if len(matches) > 1:
            console.print(f"[yellow]Multiple sandboxes match '{sandbox_id}':[/yellow]")
            for m in matches:
                console.print(f"  {m['id'][:8]} - {m.get('name', 'unnamed')}")
            raise typer.Exit(1)
        sandbox_id = matches[0]["id"]

    console.print(f"Extending sandbox by {minutes} minutes...")

    result = make_request(
        "POST",
        f"/tenants/{tenant_id}/sandboxes/{sandbox_id}/extend",
        json={"additional_minutes": minutes}
    )

    new_expiry = result.get("expires_at", "unknown")
    console.print(f"[green]Sandbox extended. New expiry: {new_expiry}[/green]")


if __name__ == "__main__":
    app()
