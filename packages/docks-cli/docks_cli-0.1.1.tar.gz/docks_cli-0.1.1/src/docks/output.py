"""Output formatting with Rich."""

from datetime import datetime, timezone
from typing import Any, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red]Error:[/red] {message}")


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green]{message}[/green]")


def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow]Warning:[/yellow] {message}")


def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue]{message}[/blue]")


def format_time_ago(dt: Optional[str]) -> str:
    """Format datetime as relative time."""
    if not dt:
        return "-"
    try:
        if isinstance(dt, str):
            # Parse ISO format
            dt_obj = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        else:
            dt_obj = dt

        now = datetime.now(timezone.utc)
        delta = now - dt_obj

        if delta.days > 0:
            return f"{delta.days}d ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600}h ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60}m ago"
        else:
            return "just now"
    except Exception:
        return str(dt)[:19]


def status_color(status: str) -> str:
    """Get color for status."""
    colors = {
        "ready": "green",
        "completed": "green",
        "passed": "green",
        "running": "blue",
        "provisioning": "blue",
        "pending": "yellow",
        "queued": "yellow",
        "failed": "red",
        "error": "red",
        "deleted": "dim",
        "cancelled": "dim",
    }
    return colors.get(status.lower(), "white")


def print_runs_table(runs: list[dict]) -> None:
    """Print runs as a table."""
    table = Table(box=box.SIMPLE)
    table.add_column("ID", style="cyan", max_width=12)
    table.add_column("Template", style="white")
    table.add_column("Status", style="white")
    table.add_column("Created", style="dim")

    for run in runs:
        run_id = str(run.get("id", ""))[:12]
        template = run.get("template_name") or str(run.get("template_id", ""))[:12]
        status = run.get("status", "unknown")
        created = format_time_ago(run.get("created_at"))

        table.add_row(
            run_id,
            template,
            f"[{status_color(status)}]{status}[/{status_color(status)}]",
            created,
        )

    console.print(table)


def print_run_detail(run: dict) -> None:
    """Print detailed run information."""
    run_id = run.get("id", "unknown")
    status = run.get("status", "unknown")

    lines = [
        f"[cyan]Run:[/cyan] {run_id}",
        f"  Template:    {run.get('template_name') or run.get('template_id')}",
        f"  Status:      [{status_color(status)}]{status}[/{status_color(status)}]",
    ]

    if run.get("dns_name"):
        lines.append(f"  DNS:         {run['dns_name']}")
    if run.get("remote_ref"):
        lines.append(f"  Remote:      {run['remote_ref']}")
    if run.get("status_reason"):
        lines.append(f"  Reason:      {run['status_reason']}")

    lines.append(f"  Created:     {run.get('created_at', '-')}")

    # Task results summary
    task_results = run.get("task_results", [])
    if task_results:
        passed = sum(1 for t in task_results if t.get("status") == "passed")
        failed = sum(1 for t in task_results if t.get("status") == "failed")
        pending = len(task_results) - passed - failed
        lines.append("")
        lines.append(
            f"  Task Results: [green]{passed} passed[/green], "
            f"[red]{failed} failed[/red], "
            f"[yellow]{pending} pending[/yellow]"
        )

    console.print("\n".join(lines))


def print_datasets_table(datasets: list[dict]) -> None:
    """Print datasets as a table."""
    table = Table(box=box.SIMPLE)
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="white")
    table.add_column("URI", style="dim", max_width=40)
    table.add_column("Created", style="dim")

    for ds in datasets:
        table.add_row(
            ds.get("name", ""),
            ds.get("version", ""),
            ds.get("uri", "")[:40],
            format_time_ago(ds.get("created_at")),
        )

    console.print(table)


def print_tasks_table(tasks: list[dict]) -> None:
    """Print tasks as a table."""
    table = Table(box=box.SIMPLE)
    table.add_column("Slug", style="cyan", max_width=30)
    table.add_column("Title", style="white", max_width=40)
    table.add_column("Difficulty", style="white")
    table.add_column("Role", style="dim")

    for task in tasks:
        diff = task.get("difficulty", "")
        diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(
            diff.lower(), "white"
        )

        table.add_row(
            task.get("slug", "")[:30],
            task.get("title", "")[:40],
            f"[{diff_color}]{diff}[/{diff_color}]",
            task.get("agent_role", ""),
        )

    console.print(table)


def print_images_table(images: list[dict]) -> None:
    """Print prebaked images as a table."""
    table = Table(box=box.SIMPLE)
    table.add_column("Instance ID", style="cyan")
    table.add_column("Size", style="white")
    table.add_column("Status", style="white")
    table.add_column("Modified", style="dim")

    for img in images:
        status = img.get("status", "unknown")
        table.add_row(
            img.get("instance_id", ""),
            img.get("size", ""),
            f"[{status_color(status)}]{status}[/{status_color(status)}]",
            img.get("modified", ""),
        )

    console.print(table)


def print_auth_status(settings: Any) -> None:
    """Print authentication status."""
    lines = [
        "[cyan]Docks CLI Status[/cyan]",
        "",
        f"  API URL:     {settings.api_url}",
        f"  Tenant ID:   {settings.tenant_id or '[red]not set[/red]'}",
        f"  Token:       {'[green]configured[/green]' if settings.token else '[red]not set[/red]'}",
        f"  Profile:     {settings.profile}",
        "",
        f"  GCP Project: {settings.gcp_project}",
        f"  GCS Bucket:  {settings.gcs_bucket}",
    ]
    console.print("\n".join(lines))


def print_eval_runs_table(runs: list[dict]) -> None:
    """Print evaluation runs as a table."""
    table = Table(box=box.SIMPLE)
    table.add_column("ID", style="cyan", max_width=12)
    table.add_column("Name", style="white", max_width=30)
    table.add_column("Status", style="white")
    table.add_column("Trials", style="white")
    table.add_column("Created", style="dim")

    for run in runs:
        run_id = str(run.get("id", ""))[:12]
        name = run.get("name", "")[:30]
        status = run.get("status", "unknown")
        total = run.get("total_trials", 0)
        completed = run.get("completed_trials", 0)
        created = format_time_ago(run.get("created_at"))

        table.add_row(
            run_id,
            name,
            f"[{status_color(status)}]{status}[/{status_color(status)}]",
            f"{completed}/{total}",
            created,
        )

    console.print(table)


def print_eval_run_detail(run: dict) -> None:
    """Print detailed evaluation run information."""
    run_id = run.get("id", "unknown")
    status = run.get("status", "unknown")

    lines = [
        f"[cyan]Evaluation Run:[/cyan] {run_id}",
        f"  Name:        {run.get('name', '-')}",
        f"  Status:      [{status_color(status)}]{status}[/{status_color(status)}]",
        f"  Dataset:     {run.get('dataset_uri', '-')}",
        "",
        f"  Total Trials:     {run.get('total_trials', 0)}",
        f"  Completed:        {run.get('completed_trials', 0)}",
        f"  Passed:           {run.get('passed_trials', 0)}",
        f"  Failed:           {run.get('failed_trials', 0)}",
        "",
        f"  Created:     {run.get('created_at', '-')}",
    ]

    console.print("\n".join(lines))


def print_trials_table(trials: list[dict]) -> None:
    """Print evaluation trials as a table."""
    table = Table(box=box.SIMPLE)
    table.add_column("ID", style="cyan", max_width=12)
    table.add_column("Task", style="white", max_width=30)
    table.add_column("Agent", style="white", max_width=15)
    table.add_column("Status", style="white")
    table.add_column("Passed", style="white")
    table.add_column("Artifacts", style="dim")

    for trial in trials:
        trial_id = str(trial.get("id", ""))[:12]
        task_slug = trial.get("task_slug", "")[:30]
        agent = trial.get("agent_variant", "")[:15]
        status = trial.get("status", "unknown")

        # Get result_data for pass rate
        result_data = trial.get("result_data") or {}
        tests_passed = result_data.get("tests_passed")
        passed_str = str(tests_passed) if tests_passed is not None else "-"

        # Count artifacts
        artifact_count = sum(1 for k in ["logs_uri", "trajectory_uri", "diff_uri", "result_uri"]
                            if trial.get(k))

        table.add_row(
            trial_id,
            task_slug,
            agent,
            f"[{status_color(status)}]{status}[/{status_color(status)}]",
            passed_str,
            f"{artifact_count} files" if artifact_count > 0 else "-",
        )

    console.print(table)


def print_trial_detail(trial: dict) -> None:
    """Print detailed trial information with artifact URIs."""
    trial_id = trial.get("id", "unknown")
    status = trial.get("status", "unknown")
    result_data = trial.get("result_data") or {}

    lines = [
        f"[cyan]Trial:[/cyan] {trial_id}",
        f"  Task:        {trial.get('task_slug', '-')}",
        f"  Agent:       {trial.get('agent_variant', '-')}",
        f"  Status:      [{status_color(status)}]{status}[/{status_color(status)}]",
        "",
    ]

    # Result data
    if result_data:
        lines.append("  [cyan]Results:[/cyan]")
        if "reward" in result_data:
            lines.append(f"    Reward:        {result_data['reward']}")
        if "tests_passed" in result_data:
            lines.append(f"    Tests Passed:  {result_data['tests_passed']}")
        if "duration_seconds" in result_data:
            lines.append(f"    Duration:      {result_data['duration_seconds']:.1f}s")
        if "prompt_tokens" in result_data:
            lines.append(f"    Tokens:        {result_data['prompt_tokens']}")
        lines.append("")

    # Artifacts
    lines.append("  [cyan]Artifacts:[/cyan]")
    artifacts = {
        "logs_uri": "Logs",
        "trajectory_uri": "Trajectory",
        "diff_uri": "Diff",
        "result_uri": "Result",
    }
    has_artifacts = False
    for key, label in artifacts.items():
        uri = trial.get(key)
        if uri:
            has_artifacts = True
            lines.append(f"    {label}: {uri}")

    if not has_artifacts:
        lines.append("    [dim]No artifacts available[/dim]")

    console.print("\n".join(lines))
