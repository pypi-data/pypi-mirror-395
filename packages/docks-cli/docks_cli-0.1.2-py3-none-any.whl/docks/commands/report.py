"""Report commands for Harbor evaluation runs."""

import json
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from ..client import SyncDocksClient
from ..output import console, print_error, print_info, print_success, status_color

app = typer.Typer(no_args_is_help=True)


def get_client() -> SyncDocksClient:
    """Get authenticated client."""
    from ..cli import state
    from ..config import load_config

    settings = load_config(state.get("profile", "default"))
    if not settings.tenant_id:
        print_error("Tenant ID not configured. Run: docks auth login")
        raise typer.Exit(1)
    return SyncDocksClient(settings)


def get_reports_dir(tenant_id: str, run_id: str) -> Path:
    """Get the reports directory for a run."""
    reports_dir = Path.home() / ".docks" / "reports" / tenant_id / run_id
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


def compute_metrics(run: dict, trials: list) -> dict:
    """Compute summary metrics from run and trials data."""
    # Extract leaderboard data if available
    leaderboard = run.get("leaderboard", [])

    # Count trials by status
    status_counts = {"completed": 0, "failed": 0, "running": 0, "pending": 0, "partial": 0}
    total_pass_rate = 0.0
    pass_rate_count = 0

    for trial in trials:
        status = trial.get("status", "pending").lower()
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts["pending"] += 1

        # Compute pass rate from result_data
        result_data = trial.get("result_data") or {}
        if isinstance(result_data, str):
            try:
                result_data = json.loads(result_data)
            except json.JSONDecodeError:
                result_data = {}

        tests_passed = result_data.get("tests_passed", 0)
        tests_total = result_data.get("tests_total", 0)
        if tests_total > 0:
            total_pass_rate += (tests_passed / tests_total) * 100
            pass_rate_count += 1

    avg_pass_rate = total_pass_rate / pass_rate_count if pass_rate_count > 0 else 0.0

    # Compute agent variant stats from leaderboard
    variant_stats = []
    for entry in leaderboard:
        variant_stats.append({
            "name": entry.get("variant_name", "unknown"),
            "trials": entry.get("trial_count", 0),
            "avg_pass_rate": entry.get("avg_pass_rate", 0.0),
            "completed": entry.get("completed_count", 0),
            "failed": entry.get("failed_count", 0),
        })

    return {
        "total_trials": len(trials),
        "status_counts": status_counts,
        "avg_pass_rate": avg_pass_rate,
        "variant_stats": variant_stats,
        "run_status": run.get("status", "unknown"),
        "run_name": run.get("name", "Unnamed Run"),
        "created_at": run.get("created_at", ""),
        "completed_at": run.get("completed_at", ""),
    }


def create_summary_panel(metrics: dict) -> Panel:
    """Create a Rich panel with run summary."""
    status = metrics["run_status"]
    status_style = status_color(status)

    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="dim")
    summary.add_column()

    summary.add_row("Run Name:", metrics["run_name"])
    summary.add_row("Status:", f"[{status_style}]{status.upper()}[/{status_style}]")
    summary.add_row("Created:", metrics["created_at"][:19] if metrics["created_at"] else "N/A")
    if metrics["completed_at"]:
        summary.add_row("Completed:", metrics["completed_at"][:19])
    summary.add_row("Total Trials:", str(metrics["total_trials"]))
    summary.add_row("Avg Pass Rate:", f"{metrics['avg_pass_rate']:.1f}%")

    return Panel(summary, title="Run Summary", border_style="blue")


def create_status_panel(metrics: dict) -> Panel:
    """Create a panel showing trial status distribution."""
    counts = metrics["status_counts"]
    total = metrics["total_trials"] or 1  # Avoid division by zero

    table = Table.grid(padding=(0, 2))
    table.add_column(width=12)
    table.add_column(width=6, justify="right")
    table.add_column(width=30)

    for status, count in counts.items():
        if count > 0:
            pct = (count / total) * 100
            bar_width = int((count / total) * 20)
            bar = "█" * bar_width + "░" * (20 - bar_width)
            style = status_color(status)
            table.add_row(
                f"[{style}]{status.capitalize()}[/{style}]",
                str(count),
                f"[{style}]{bar}[/{style}] {pct:.0f}%"
            )

    return Panel(table, title="Trial Status", border_style="green")


def create_leaderboard_table(metrics: dict) -> Panel:
    """Create a leaderboard table for agent variants."""
    table = Table(show_header=True, header_style="bold cyan", box=None)
    table.add_column("Agent Variant", style="white")
    table.add_column("Trials", justify="right")
    table.add_column("Completed", justify="right")
    table.add_column("Failed", justify="right")
    table.add_column("Avg Pass Rate", justify="right")

    for variant in metrics["variant_stats"]:
        pass_rate = variant["avg_pass_rate"]
        rate_style = "green" if pass_rate >= 80 else "yellow" if pass_rate >= 50 else "red"

        table.add_row(
            variant["name"],
            str(variant["trials"]),
            f"[green]{variant['completed']}[/green]",
            f"[red]{variant['failed']}[/red]" if variant["failed"] > 0 else "0",
            f"[{rate_style}]{pass_rate:.1f}%[/{rate_style}]"
        )

    if not metrics["variant_stats"]:
        table.add_row("[dim]No variant data available[/dim]", "", "", "", "")

    return Panel(table, title="Agent Variant Leaderboard", border_style="magenta")


def create_trials_table(trials: list, limit: int = 10) -> Panel:
    """Create a table showing recent trials."""
    table = Table(show_header=True, header_style="bold", box=None)
    table.add_column("Task", style="white", max_width=40)
    table.add_column("Variant", max_width=15)
    table.add_column("Status", justify="center")
    table.add_column("Pass Rate", justify="right")
    table.add_column("Duration", justify="right")

    # Sort by created_at descending
    sorted_trials = sorted(
        trials,
        key=lambda t: t.get("created_at", ""),
        reverse=True
    )[:limit]

    for trial in sorted_trials:
        task_slug = trial.get("task_slug", "unknown")
        variant = trial.get("variant_name", "unknown")
        status = trial.get("status", "pending")

        # Parse result_data
        result_data = trial.get("result_data") or {}
        if isinstance(result_data, str):
            try:
                result_data = json.loads(result_data)
            except json.JSONDecodeError:
                result_data = {}

        tests_passed = result_data.get("tests_passed", 0)
        tests_total = result_data.get("tests_total", 0)
        pass_rate = (tests_passed / tests_total * 100) if tests_total > 0 else 0
        duration = result_data.get("duration_seconds", 0)

        status_style = status_color(status)
        rate_style = "green" if pass_rate >= 80 else "yellow" if pass_rate >= 50 else "red"

        table.add_row(
            task_slug[:40],
            variant[:15],
            f"[{status_style}]{status}[/{status_style}]",
            f"[{rate_style}]{pass_rate:.0f}%[/{rate_style}]" if tests_total > 0 else "[dim]N/A[/dim]",
            f"{duration:.0f}s" if duration else "[dim]N/A[/dim]"
        )

    if not trials:
        table.add_row("[dim]No trials yet[/dim]", "", "", "", "")

    return Panel(table, title=f"Recent Trials (showing {min(len(trials), limit)})", border_style="yellow")


def render_dashboard(run: dict, trials: list) -> Layout:
    """Render the full TUI dashboard."""
    metrics = compute_metrics(run, trials)

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )

    # Header
    header_text = Text()
    header_text.append("DOCKS EVALUATION REPORT", style="bold white on blue")
    header_text.append(f"  Run ID: {run.get('id', 'N/A')[:8]}...", style="dim")
    layout["header"].update(Panel(header_text, style="blue"))

    # Body - split into columns
    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=2),
    )

    # Left column - summary and status
    layout["left"].split_column(
        Layout(create_summary_panel(metrics)),
        Layout(create_status_panel(metrics)),
    )

    # Right column - leaderboard and trials
    layout["right"].split_column(
        Layout(create_leaderboard_table(metrics), size=12),
        Layout(create_trials_table(trials)),
    )

    # Footer
    footer_text = Text()
    footer_text.append(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
    footer_text.append("  |  ", style="dim")
    footer_text.append("Press Ctrl+C to exit", style="dim italic")
    layout["footer"].update(Panel(footer_text, style="dim"))

    return layout


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docks Evaluation Report - {{ run.name }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent-blue: #3b82f6;
            --accent-green: #22c55e;
            --accent-yellow: #eab308;
            --accent-red: #ef4444;
            --accent-purple: #a855f7;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 2rem;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--bg-card);
        }

        header h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        header .subtitle {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .grid {
            display: grid;
            gap: 1.5rem;
        }

        .grid-2 {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }

        .grid-3 {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }

        .card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }

        .card h2 {
            font-size: 1rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--bg-card);
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }

        .status-completed { color: var(--accent-green); }
        .status-failed { color: var(--accent-red); }
        .status-running { color: var(--accent-blue); }
        .status-pending { color: var(--accent-yellow); }
        .status-partial { color: var(--accent-purple); }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--bg-card);
        }

        th {
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }

        tr:hover {
            background: var(--bg-card);
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .badge-green { background: rgba(34, 197, 94, 0.2); color: var(--accent-green); }
        .badge-red { background: rgba(239, 68, 68, 0.2); color: var(--accent-red); }
        .badge-blue { background: rgba(59, 130, 246, 0.2); color: var(--accent-blue); }
        .badge-yellow { background: rgba(234, 179, 8, 0.2); color: var(--accent-yellow); }

        .progress-bar {
            height: 8px;
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }

        .chart-container {
            position: relative;
            height: 300px;
        }

        .logs-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--accent-blue);
            text-decoration: none;
            font-size: 0.875rem;
        }

        .logs-link:hover {
            text-decoration: underline;
        }

        footer {
            margin-top: 2rem;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ run.name }}</h1>
            <p class="subtitle">
                Run ID: {{ run.id }} |
                Created: {{ run.created_at[:19] if run.created_at else 'N/A' }} |
                Status: <span class="status-{{ run.status }}">{{ run.status | upper }}</span>
            </p>
        </header>

        <div class="grid grid-3" style="margin-bottom: 1.5rem;">
            <div class="card">
                <h2>Total Trials</h2>
                <div class="stat-value">{{ metrics.total_trials }}</div>
                <div class="stat-label">evaluation trials</div>
            </div>
            <div class="card">
                <h2>Pass Rate</h2>
                <div class="stat-value" style="color: {{ 'var(--accent-green)' if metrics.avg_pass_rate >= 80 else 'var(--accent-yellow)' if metrics.avg_pass_rate >= 50 else 'var(--accent-red)' }}">
                    {{ "%.1f" | format(metrics.avg_pass_rate) }}%
                </div>
                <div class="stat-label">average across all trials</div>
            </div>
            <div class="card">
                <h2>Completed</h2>
                <div class="stat-value status-completed">{{ metrics.status_counts.completed }}</div>
                <div class="stat-label">of {{ metrics.total_trials }} trials</div>
            </div>
        </div>

        <div class="grid grid-2">
            <div class="card">
                <h2>Trial Status Distribution</h2>
                <div class="chart-container">
                    <canvas id="statusChart"></canvas>
                </div>
            </div>
            <div class="card">
                <h2>Pass Rate by Variant</h2>
                <div class="chart-container">
                    <canvas id="variantChart"></canvas>
                </div>
            </div>
        </div>

        <div class="card" style="margin-top: 1.5rem;">
            <h2>Agent Variant Leaderboard</h2>
            <table>
                <thead>
                    <tr>
                        <th>Variant</th>
                        <th>Trials</th>
                        <th>Completed</th>
                        <th>Failed</th>
                        <th>Avg Pass Rate</th>
                    </tr>
                </thead>
                <tbody>
                    {% for variant in metrics.variant_stats %}
                    <tr>
                        <td><strong>{{ variant.name }}</strong></td>
                        <td>{{ variant.trials }}</td>
                        <td><span class="badge badge-green">{{ variant.completed }}</span></td>
                        <td>{% if variant.failed > 0 %}<span class="badge badge-red">{{ variant.failed }}</span>{% else %}0{% endif %}</td>
                        <td>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <div class="progress-bar" style="flex: 1; max-width: 100px;">
                                    <div class="progress-fill" style="width: {{ variant.avg_pass_rate }}%; background: {{ 'var(--accent-green)' if variant.avg_pass_rate >= 80 else 'var(--accent-yellow)' if variant.avg_pass_rate >= 50 else 'var(--accent-red)' }};"></div>
                                </div>
                                <span>{{ "%.1f" | format(variant.avg_pass_rate) }}%</span>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                    {% if not metrics.variant_stats %}
                    <tr>
                        <td colspan="5" style="text-align: center; color: var(--text-secondary);">No variant data available</td>
                    </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>

        <div class="card" style="margin-top: 1.5rem;">
            <h2>Trial Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Task</th>
                        <th>Variant</th>
                        <th>Status</th>
                        <th>Tests</th>
                        <th>Duration</th>
                        <th>Logs</th>
                    </tr>
                </thead>
                <tbody>
                    {% for trial in trials[:50] %}
                    <tr>
                        <td>{{ trial.task_slug }}</td>
                        <td>{{ trial.variant_name }}</td>
                        <td>
                            <span class="badge badge-{{ 'green' if trial.status == 'completed' else 'red' if trial.status == 'failed' else 'blue' if trial.status == 'running' else 'yellow' }}">
                                {{ trial.status }}
                            </span>
                        </td>
                        <td>
                            {% set rd = trial.result_data or {} %}
                            {% if rd.tests_total %}
                                {{ rd.tests_passed }}/{{ rd.tests_total }}
                            {% else %}
                                -
                            {% endif %}
                        </td>
                        <td>
                            {% if rd.duration_seconds %}
                                {{ "%.0f" | format(rd.duration_seconds) }}s
                            {% else %}
                                -
                            {% endif %}
                        </td>
                        <td>
                            {% if trial.logs_uri %}
                            <a href="{{ trial.logs_uri }}" class="logs-link" target="_blank">View Logs</a>
                            {% else %}
                            <span style="color: var(--text-secondary);">-</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% if trials | length > 50 %}
            <p style="text-align: center; margin-top: 1rem; color: var(--text-secondary);">
                Showing 50 of {{ trials | length }} trials
            </p>
            {% endif %}
        </div>

        <footer>
            <p>Generated by Docks CLI on {{ generated_at }}</p>
            <p>Izumi Evaluation Platform</p>
        </footer>
    </div>

    <script>
        // Status distribution chart
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Failed', 'Running', 'Pending', 'Partial'],
                datasets: [{
                    data: [
                        {{ metrics.status_counts.completed }},
                        {{ metrics.status_counts.failed }},
                        {{ metrics.status_counts.running }},
                        {{ metrics.status_counts.pending }},
                        {{ metrics.status_counts.partial }}
                    ],
                    backgroundColor: [
                        '#22c55e',
                        '#ef4444',
                        '#3b82f6',
                        '#eab308',
                        '#a855f7'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94a3b8' }
                    }
                }
            }
        });

        // Variant pass rate chart
        const variantCtx = document.getElementById('variantChart').getContext('2d');
        new Chart(variantCtx, {
            type: 'bar',
            data: {
                labels: [{% for v in metrics.variant_stats %}'{{ v.name }}'{% if not loop.last %}, {% endif %}{% endfor %}],
                datasets: [{
                    label: 'Pass Rate (%)',
                    data: [{% for v in metrics.variant_stats %}{{ v.avg_pass_rate }}{% if not loop.last %}, {% endif %}{% endfor %}],
                    backgroundColor: [{% for v in metrics.variant_stats %}'{{ "#22c55e" if v.avg_pass_rate >= 80 else "#eab308" if v.avg_pass_rate >= 50 else "#ef4444" }}'{% if not loop.last %}, {% endif %}{% endfor %}],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: '#334155' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    </script>
</body>
</html>
'''


def generate_html_report(run: dict, trials: list, output_path: Path) -> Path:
    """Generate an HTML report using Jinja2 templating."""
    try:
        from jinja2 import Template
    except ImportError:
        print_error("jinja2 is required for HTML reports. Install with: pip install jinja2")
        raise typer.Exit(1)

    # Ensure result_data is parsed for each trial
    processed_trials = []
    for trial in trials:
        trial_copy = trial.copy()
        result_data = trial_copy.get("result_data") or {}
        if isinstance(result_data, str):
            try:
                result_data = json.loads(result_data)
            except json.JSONDecodeError:
                result_data = {}
        trial_copy["result_data"] = result_data
        processed_trials.append(trial_copy)

    metrics = compute_metrics(run, trials)

    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        run=run,
        trials=processed_trials,
        metrics=metrics,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    with open(output_path, "w") as f:
        f.write(html_content)

    return output_path


@app.command("show")
def show_report(
    run_id: str = typer.Argument(..., help="Harbor run ID to report on"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch for updates and refresh"),
    refresh_interval: int = typer.Option(10, "--interval", "-i", help="Refresh interval in seconds (with --watch)"),
):
    """Display a TUI dashboard for a Harbor evaluation run."""
    client = get_client()

    try:
        run = client.get_harbor_run(run_id)
        trials = client.list_harbor_trials(run_id)
    except Exception as e:
        print_error(f"Failed to fetch run data: {e}")
        raise typer.Exit(1)

    if watch:
        print_info(f"Watching run {run_id[:8]}... (Ctrl+C to exit)")
        try:
            with Live(render_dashboard(run, trials), refresh_per_second=1, screen=True) as live:
                while True:
                    time.sleep(refresh_interval)
                    try:
                        run = client.get_harbor_run(run_id)
                        trials = client.list_harbor_trials(run_id)
                        live.update(render_dashboard(run, trials))
                    except Exception:
                        pass  # Keep displaying last known state on fetch errors
        except KeyboardInterrupt:
            pass
    else:
        console.print(render_dashboard(run, trials))


@app.command("html")
def generate_html(
    run_id: str = typer.Argument(..., help="Harbor run ID to report on"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    open_browser: bool = typer.Option(False, "--open", help="Open report in browser"),
):
    """Generate an HTML report for a Harbor evaluation run."""
    client = get_client()

    print_info(f"Fetching data for run {run_id[:8]}...")

    try:
        run = client.get_harbor_run(run_id)
        trials = client.list_harbor_trials(run_id)
    except Exception as e:
        print_error(f"Failed to fetch run data: {e}")
        raise typer.Exit(1)

    # Determine output path
    if output:
        output_path = output
    else:
        from ..cli import state
        from ..config import load_config
        settings = load_config(state.get("profile", "default"))
        reports_dir = get_reports_dir(settings.tenant_id, run_id)
        output_path = reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    # Generate report
    report_path = generate_html_report(run, trials, output_path)
    print_success(f"Report generated: {report_path}")

    if open_browser:
        webbrowser.open(f"file://{report_path.absolute()}")
        print_info("Opened report in browser")


@app.command("summary")
def show_summary(
    run_id: str = typer.Argument(..., help="Harbor run ID to summarize"),
):
    """Show a compact summary of a Harbor evaluation run."""
    client = get_client()

    try:
        run = client.get_harbor_run(run_id)
        trials = client.list_harbor_trials(run_id)
    except Exception as e:
        print_error(f"Failed to fetch run data: {e}")
        raise typer.Exit(1)

    metrics = compute_metrics(run, trials)

    # Compact summary output
    console.print()
    console.print(Panel(
        f"[bold]{metrics['run_name']}[/bold]\n"
        f"[dim]ID: {run.get('id', 'N/A')}[/dim]",
        title="Run Summary",
        border_style="blue"
    ))

    # Quick stats
    status_style = status_color(metrics["run_status"])
    stats = Table.grid(padding=(0, 4))
    stats.add_column()
    stats.add_column()
    stats.add_column()
    stats.add_column()

    stats.add_row(
        f"[dim]Status:[/dim] [{status_style}]{metrics['run_status'].upper()}[/{status_style}]",
        f"[dim]Trials:[/dim] {metrics['total_trials']}",
        f"[dim]Completed:[/dim] [green]{metrics['status_counts']['completed']}[/green]",
        f"[dim]Failed:[/dim] [red]{metrics['status_counts']['failed']}[/red]",
    )

    pass_style = "green" if metrics["avg_pass_rate"] >= 80 else "yellow" if metrics["avg_pass_rate"] >= 50 else "red"
    stats.add_row(
        f"[dim]Avg Pass Rate:[/dim] [{pass_style}]{metrics['avg_pass_rate']:.1f}%[/{pass_style}]",
        f"[dim]Running:[/dim] [blue]{metrics['status_counts']['running']}[/blue]",
        f"[dim]Pending:[/dim] [yellow]{metrics['status_counts']['pending']}[/yellow]",
        f"[dim]Partial:[/dim] [magenta]{metrics['status_counts']['partial']}[/magenta]",
    )

    console.print(stats)
    console.print()
