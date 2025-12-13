"""Run management commands."""

import os
import subprocess
from pathlib import Path
from typing import Optional

import typer

from ..api import DocksAPI, APIError
from ..config import load_config
from ..output import (
    console,
    print_runs_table,
    print_run_detail,
    print_eval_runs_table,
    print_eval_run_detail,
    print_trials_table,
    print_trial_detail,
    print_error,
    print_success,
    print_info,
    print_warning,
)
from ..datasets import resolve_dataset_uri, list_available_datasets


app = typer.Typer()


def get_api(debug: bool = False) -> DocksAPI:
    """Get configured API client.

    Args:
        debug: Enable verbose HTTP logging

    Returns:
        Configured DocksAPI instance

    Raises:
        typer.Exit: If config is missing
    """
    from ..cli import state

    try:
        return DocksAPI.from_config(
            profile=state.get("profile", "default"),
            debug=debug,
        )
    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("list")
def list_runs(
    limit: int = typer.Option(20, "--limit", "-n", help="Number of runs to show"),
    status_filter: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status"
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """List evaluation runs."""
    api = get_api(debug=debug)

    try:
        runs = api.list_runs(limit=limit)

        if status_filter:
            runs = [r for r in runs if r.get("status") == status_filter]

        if not runs:
            console.print("[dim]No runs found[/dim]")
            return

        print_runs_table(runs)

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("get")
def get_run(
    run_id: str = typer.Argument(..., help="Run ID"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Get details of a specific run."""
    api = get_api(debug=debug)

    try:
        run = api.get_run(run_id)
        print_run_detail(run)

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("stop")
def stop_run(
    run_id: str = typer.Argument(..., help="Run ID to stop"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Stop a running evaluation."""
    if not force:
        if not typer.confirm(f"Stop run {run_id}?"):
            raise typer.Abort()

    api = get_api(debug=debug)

    try:
        api.stop_run(run_id)
        print_success(f"Run {run_id} stopped")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


def create_run(
    template: str,
    provider: str = "anthropic",
    params: Optional[list[str]] = None,
    debug: bool = False,
):
    """Create a new run (called from root command)."""
    api = get_api(debug=debug)

    # Parse params
    params_dict = {}
    if params:
        for p in params:
            if "=" in p:
                key, value = p.split("=", 1)
                params_dict[key] = value

    try:
        # Find template by name or ID
        templates = api.list_templates()

        template_id = None
        for t in templates:
            if str(t.get("id")) == template or t.get("name") == template:
                template_id = str(t["id"])
                break

        if not template_id:
            print_error(f"Template not found: {template}")
            raise typer.Exit(1)

        # Create run - Note: this uses legacy run API, not harbor runs
        # The new DocksAPI doesn't have create_run with template, so we use httpx directly
        import httpx
        from ..config import get_headers

        settings = load_config()
        run_url = f"{settings.api_url}/tenants/{settings.tenant_id}/runs"
        with httpx.Client(headers=get_headers(settings), timeout=30.0) as http:
            resp = http.post(
                run_url,
                json={
                    "template_id": template_id,
                    "provider": provider,
                    "params": params_dict,
                },
            )
            resp.raise_for_status()
            run = resp.json()

        print_success(f"Run created: {run['id']}")
        console.print(f"  Status: {run.get('status')}")

    except APIError as e:
        e.display()
        raise typer.Exit(1)
    except httpx.HTTPStatusError as e:
        print_error(f"API error: {e.response.status_code} - {e.response.text}")
        raise typer.Exit(1)


# Evaluation run commands


@app.command("eval-run")
def create_harbor_run(
    name: str = typer.Option(..., "--name", "-n", help="Run name"),
    dataset: Optional[str] = typer.Option(
        None, "--dataset", "-d", help="Dataset name or GCS URI (e.g., 'swebench', 'go-gin', or gs://...)"
    ),
    task_slugs: Optional[list[str]] = typer.Option(
        None, "--task", "-t", help="Task slug(s) to run (can specify multiple)"
    ),
    model: Optional[str] = typer.Option(
        None, "--model", "-m", help="Model to use (default from config or claude-sonnet-4-5-20250929)"
    ),
    anthropic_key: Optional[str] = typer.Option(
        None, "--anthropic-key", "-k",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
        envvar="ANTHROPIC_API_KEY",
    ),
    agent: str = typer.Option(
        "claude-code", "--agent", "-a", help="Agent type (claude-code, nop)"
    ),
    concurrent: Optional[int] = typer.Option(
        None, "--concurrent", "-c", help="Max concurrent trials (default from config or 32)"
    ),
    attempts: Optional[int] = typer.Option(
        None, "--attempts", help="Attempts per task (default from config or 1)"
    ),
    start: bool = typer.Option(
        False, "--start", "-s", help="Auto-start the run after creation"
    ),
    env_var: Optional[list[str]] = typer.Option(
        None, "--env", "-e", help="Additional env vars (KEY=VALUE)"
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """
    Create and optionally start an evaluation run.

    Run evaluations with different Anthropic API keys and configurations.

    Dataset aliases: Use friendly names instead of full GCS URIs:
      - swebench, swe-bench: SWE-bench Lite dataset
      - go-gin, gin: Go Gin benchmark

    Examples:

        # Using dataset alias (recommended)
        export ANTHROPIC_API_KEY="sk-ant-api..."
        docks runs eval-run -n "My Test" -d swebench -t astropy__astropy-12907 --start

        # Pass API key directly
        docks runs eval-run -n "Test Run" \\
            --dataset swebench \\
            --task astropy__astropy-12907 \\
            --anthropic-key sk-ant-api... \\
            --model claude-sonnet-4-5-20250514 \\
            --concurrent 16 \\
            --start

        # Multiple tasks
        docks runs eval-run -n "Multi Task" \\
            -d swebench \\
            -t astropy__astropy-12907 \\
            -t django__django-11039 \\
            --start

        # List available dataset aliases
        docks datasets aliases
    """
    from ..cli import state
    settings = load_config(state.get("profile", "default"))

    # Apply config defaults for optional parameters
    if model is None:
        model = settings.default_model
    if concurrent is None:
        concurrent = settings.default_concurrent
    if attempts is None:
        attempts = settings.default_attempts

    api = get_api(debug=debug)

    # Resolve dataset alias to GCS URI
    dataset_uri = None
    if dataset:
        dataset_uri = resolve_dataset_uri(dataset)
        if dataset != dataset_uri:
            print_info(f"Using dataset: {dataset} → {dataset_uri}")

    # Build env_vars dict
    env_vars = {}
    if anthropic_key:
        env_vars["ANTHROPIC_API_KEY"] = anthropic_key

    # Parse additional env vars
    if env_var:
        for e in env_var:
            if "=" in e:
                key, value = e.split("=", 1)
                env_vars[key] = value
            else:
                print_error(f"Invalid env var format: {e} (expected KEY=VALUE)")
                raise typer.Exit(1)

    # Validate we have an API key if using claude-code agent
    if agent == "claude-code" and "ANTHROPIC_API_KEY" not in env_vars:
        print_error(
            "Anthropic API key required for claude-code agent.\n"
            "Either:\n"
            "  - Set ANTHROPIC_API_KEY environment variable\n"
            "  - Pass --anthropic-key option"
        )
        raise typer.Exit(1)

    # Build agent variant config
    agent_variants = [{
        "name": agent,
        "config": {
            "type": agent,
            "model": model,
            "env_vars": env_vars,
        }
    }]

    # Build payload
    payload = {
        "name": name,
        "max_concurrent": concurrent,
        "attempts_per_task": attempts,
        "agent_variants": agent_variants,
    }
    if dataset_uri:
        payload["dataset_uri"] = dataset_uri
    if task_slugs:
        payload["task_slugs"] = task_slugs

    try:
        run = api.create_harbor_run(payload)

        print_success(f"Evaluation run created: {run['id']}")
        console.print(f"  Name: {run.get('name')}")
        console.print(f"  Status: {run.get('status')}")
        console.print(f"  Model: {model}")
        console.print(f"  Agent: {agent}")
        if task_slugs:
            console.print(f"  Tasks: {len(task_slugs)}")

        if start:
            console.print("\n[dim]Starting run...[/dim]")
            started = api.start_harbor_run(run["id"])
            print_success("Run started!")
            console.print(f"  Status: {started.get('status')}")
            console.print(f"  Tasks total: {started.get('tasks_total')}")
            console.print(f"\nMonitor progress with:")
            console.print(f"  docks runs eval-get {run['id']}")
            console.print(f"  docks runs trials {run['id']}")
        else:
            console.print(f"\nStart with: docks runs eval-start {run['id']}")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("eval-start")
def start_harbor_run_cmd(
    run_id: str = typer.Argument(..., help="Evaluation run ID"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Start a queued evaluation run."""
    api = get_api(debug=debug)

    try:
        run = api.start_harbor_run(run_id)
        print_success(f"Evaluation run {run_id} started!")
        console.print(f"  Status: {run.get('status')}")
        console.print(f"  Tasks total: {run.get('tasks_total')}")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("eval-cancel")
def cancel_harbor_run_cmd(
    run_id: str = typer.Argument(..., help="Evaluation run ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Cancel a running evaluation run."""
    if not force:
        if not typer.confirm(f"Cancel evaluation run {run_id}?"):
            raise typer.Abort()

    api = get_api(debug=debug)

    try:
        run = api.cancel_harbor_run(run_id)
        print_success(f"Evaluation run {run_id} cancelled")
        console.print(f"  Status: {run.get('status')}")

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("eval-list")
def list_harbor_runs(
    limit: int = typer.Option(20, "--limit", "-n", help="Number of runs to show"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """List evaluation runs."""
    api = get_api(debug=debug)

    try:
        runs = api.list_harbor_runs(limit=limit)

        if not runs:
            console.print("[dim]No evaluation runs found[/dim]")
            return

        print_eval_runs_table(runs)

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("eval-get")
def get_harbor_run(
    run_id: str = typer.Argument(..., help="Evaluation run ID"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Get details of an evaluation run."""
    api = get_api(debug=debug)

    try:
        run = api.get_harbor_run(run_id)
        print_eval_run_detail(run)

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("trials")
def list_trials(
    run_id: str = typer.Argument(..., help="Evaluation run ID"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """List trials for an evaluation run."""
    api = get_api(debug=debug)

    try:
        trials = api.list_harbor_trials(run_id)

        if not trials:
            console.print("[dim]No trials found[/dim]")
            return

        print_trials_table(trials)

    except APIError as e:
        e.display()
        raise typer.Exit(1)


@app.command("trial")
def get_trial(
    run_id: str = typer.Argument(..., help="Evaluation run ID"),
    trial_id: str = typer.Argument(..., help="Trial ID"),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """Get detailed trial info including artifact URIs."""
    api = get_api(debug=debug)

    try:
        trial = api.get_harbor_trial(run_id, trial_id)
        print_trial_detail(trial)

    except APIError as e:
        e.display()
        raise typer.Exit(1)


def _download_gcs_artifact(uri: str, output_dir: Path, name: str) -> Optional[Path]:
    """Download artifact from GCS using gsutil."""
    if not uri or not uri.startswith("gs://"):
        return None

    # Determine output filename
    ext = Path(uri).suffix or ".json"
    output_path = output_dir / f"{name}{ext}"

    try:
        result = subprocess.run(
            ["gsutil", "cp", uri, str(output_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return output_path
        else:
            console.print(f"[dim]Failed to download {name}: {result.stderr}[/dim]")
            return None
    except FileNotFoundError:
        print_error("gsutil not found. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install")
        return None


@app.command("artifacts")
def download_artifacts(
    run_id: str = typer.Argument(..., help="Evaluation run ID"),
    trial_id: Optional[str] = typer.Option(None, "--trial", "-t", help="Download for specific trial only"),
    output_dir: Path = typer.Option(
        Path("."), "--output", "-o", help="Output directory for artifacts"
    ),
    artifact_type: Optional[str] = typer.Option(
        None, "--type", help="Artifact type: logs, trajectory, diff, result"
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable verbose HTTP logging"),
):
    """
    Download artifacts from completed evaluation trials.

    Downloads artifacts from GCS to local filesystem. Requires gsutil to be installed.

    Examples:
        docks runs artifacts abc123                     # All artifacts for run
        docks runs artifacts abc123 -t xyz789          # Artifacts for specific trial
        docks runs artifacts abc123 --type logs        # Only logs
        docks runs artifacts abc123 -o ./results       # Custom output directory
    """
    api = get_api(debug=debug)

    try:
        if trial_id:
            trials = [api.get_harbor_trial(run_id, trial_id)]
        else:
            trials = api.list_harbor_trials(run_id)

        if not trials:
            console.print("[dim]No trials found[/dim]")
            return

        # Create output directory
        run_output = output_dir / run_id[:12]
        run_output.mkdir(parents=True, exist_ok=True)

        artifact_keys = {
            "logs": "logs_uri",
            "trajectory": "trajectory_uri",
            "diff": "diff_uri",
            "result": "result_uri",
        }

        # Filter by type if specified
        if artifact_type:
            if artifact_type not in artifact_keys:
                print_error(f"Unknown artifact type: {artifact_type}")
                print_info(f"Available types: {', '.join(artifact_keys.keys())}")
                raise typer.Exit(1)
            artifact_keys = {artifact_type: artifact_keys[artifact_type]}

        downloaded = 0
        for trial in trials:
            tid = trial.get("id", "unknown")[:12]
            task = trial.get("task_slug", "unknown")
            trial_dir = run_output / f"{task}_{tid}"
            trial_dir.mkdir(parents=True, exist_ok=True)

            for name, key in artifact_keys.items():
                uri = trial.get(key)
                if uri:
                    path = _download_gcs_artifact(uri, trial_dir, name)
                    if path:
                        console.print(f"  Downloaded: {path}")
                        downloaded += 1

        if downloaded > 0:
            print_success(f"Downloaded {downloaded} artifact(s) to {run_output}")
        else:
            console.print("[dim]No artifacts available to download[/dim]")

    except APIError as e:
        e.display()
        raise typer.Exit(1)
