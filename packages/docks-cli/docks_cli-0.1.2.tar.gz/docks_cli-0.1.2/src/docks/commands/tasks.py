"""Task management commands for creating and validating evaluation tasks."""

import json
import sys
from pathlib import Path
from typing import Optional

import typer
import yaml

from ..output import console, print_error, print_success, print_info

app = typer.Typer()

# Valid values for task fields
VALID_ROLES = ["coding", "sre", "code_review", "architect", "security"]
VALID_DIFFICULTIES = ["easy", "medium", "hard"]
VALID_TEMPLATES = ["dev-docks", "swebench", "harbor", "minimal", "nova"]


def get_template_dir() -> Path:
    """Get the templates directory path."""
    return Path(__file__).parent.parent / "templates"


def load_schema() -> dict:
    """Load the Nova task JSON schema."""
    # Try multiple possible locations
    possible_paths = [
        # From CLI package location (cli/src/docks/commands/tasks.py -> tasks/schema/)
        Path(__file__).parent.parent.parent.parent.parent / "tasks" / "schema" / "task.schema.json",
        # From current working directory
        Path.cwd() / "tasks" / "schema" / "task.schema.json",
        # Relative to izumi root (if running from anywhere in the repo)
        Path(__file__).resolve().parent,
    ]

    # Walk up from current file to find the schema
    current = Path(__file__).resolve().parent
    for _ in range(10):  # Max 10 levels up
        schema_path = current / "tasks" / "schema" / "task.schema.json"
        if schema_path.exists():
            with open(schema_path) as f:
                return json.load(f)
        current = current.parent

    return {}  # Return empty if schema not found


def generate_dev_docks_task(
    name: str,
    title: str,
    difficulty: str,
    role: str,
    repo_url: Optional[str],
    ref: Optional[str],
) -> dict:
    """Generate a dev-docks format task.yaml."""
    task = {
        "slug": name,
        "title": title or f"Implement {name.replace('__', ' ').replace('-', ' ').title()}",
        "repo_url": repo_url or f"https://github.com/example/{name.split('__')[0]}",
        "ref": ref or "main",
        "agent_role": role,
        "difficulty": difficulty,
        "skills": ["python"],  # Default, user should update
        "categories": ["feature"],  # Default, user should update
        "instruction": """\
# Task: {title}

## Objective
Describe what the agent should accomplish.

## Requirements
1. First requirement
2. Second requirement
3. Third requirement

## Acceptance Criteria
- [ ] All tests pass
- [ ] Code follows project conventions
- [ ] Documentation updated if needed
""".format(title=title or name),
        "success_checks": [
            {
                "name": "tests_pass",
                "command": "pytest tests/",
                "timeout_seconds": 300,
            }
        ],
        "rubric": {
            "correctness": 0.4,
            "code_quality": 0.3,
            "test_coverage": 0.2,
            "documentation": 0.1,
        },
        "x": {
            "dev_docks": {
                "reference_dependencies": [],
                "source": "manual",
                "annotator": "human",
                "estimated_time_minutes": 30,
            }
        },
    }
    return task


def generate_swebench_task(
    name: str,
    title: str,
    difficulty: str,
    role: str,
    repo_url: Optional[str],
    ref: Optional[str],
) -> dict:
    """Generate a SWE-bench compatible task.yaml."""
    repo = name.split("__")[0] if "__" in name else "example"
    task = {
        "slug": name,
        "title": title or f"Fix issue in {repo}",
        "repo_url": repo_url or f"https://github.com/{repo.replace('-', '/')}/{repo}",
        "agent_role": role,
        "difficulty": difficulty,
        "instruction": """\
# Issue Description

Describe the bug or feature request here.

## Steps to Reproduce
1. Step one
2. Step two
3. Expected vs actual behavior

## Solution Hints
- Look at relevant file(s)
- Consider edge cases
""",
        "swebench": {
            "instance_id": name,
            "base_commit": ref or "main",
            "test_patch": "",
            "fail_to_pass": [],
            "pass_to_pass": [],
        },
    }
    return task


def generate_harbor_task(
    name: str,
    title: str,
    difficulty: str,
    role: str,
) -> dict:
    """Generate a Harbor-compatible task.toml structure."""
    import tomli_w

    task = {
        "task": {
            "name": name,
            "title": title or f"Implement {name.replace('_', ' ').title()}",
            "difficulty": difficulty,
        },
        "agent": {
            "role": role,
        },
        "reward": {
            "type": "binary",
            "aggregation": "mean",
        },
    }
    return task


def generate_nova_task(
    name: str,
    title: str,
    difficulty: str,
    role: str,
    repo_url: Optional[str],
) -> dict:
    """Generate a full Nova schema task.yaml."""
    repo = name.split("__")[0] if "__" in name else name.split(".")[0] if "." in name else "example"
    task_name = name.split("__")[1] if "__" in name else name

    task = {
        "id": f"nova.{repo}.{task_name}.v1",
        "title": title or f"Implement {task_name.replace('-', ' ').title()}",
        "repo": repo,
        "repo_url": repo_url or f"https://github.com/example/{repo}",
        "agent_role": role,
        "categories": ["coding"],
        "difficulty": difficulty,
        "estimated_duration_minutes": 30,
        "skills": ["python"],
        "description": f"Task to {task_name.replace('-', ' ').replace('_', ' ')}.",
        "instruction": """\
# Instructions

Describe the task in detail here.

## Requirements
1. First requirement
2. Second requirement

## Hints
- Hint one
- Hint two
""",
        "environment": {
            "docker_image": "us-west2-docker.pkg.dev/izumi-479101/izumi-repo/docks-python:latest",
            "workdir": "/workspace",
        },
        "success_checks": [
            {
                "name": "tests_pass",
                "command": "pytest tests/",
                "timeout_seconds": 300,
            }
        ],
        "hints": [],
        "evaluation_notes": "Human review guidance here.",
        "tags": [],
        "version": "1.0.0",
    }
    return task


def generate_minimal_task(
    name: str,
    title: str,
    difficulty: str,
    role: str,
) -> dict:
    """Generate a minimal task.yaml."""
    task = {
        "slug": name,
        "title": title or f"Task: {name}",
        "difficulty": difficulty,
        "agent_role": role,
        "instruction": "Describe the task here.",
    }
    return task


@app.command("init")
def init_task(
    name: str = typer.Argument(..., help="Task name (e.g., 'django__fix-auth-bug')"),
    template: str = typer.Option(
        "dev-docks",
        "--template",
        "-t",
        help=f"Template format: {', '.join(VALID_TEMPLATES)}",
    ),
    difficulty: str = typer.Option(
        "medium",
        "--difficulty",
        "-d",
        help=f"Task difficulty: {', '.join(VALID_DIFFICULTIES)}",
    ),
    role: str = typer.Option(
        "coding",
        "--role",
        "-r",
        help=f"Agent role: {', '.join(VALID_ROLES)}",
    ),
    title: Optional[str] = typer.Option(
        None,
        "--title",
        help="Task title (auto-generated if not provided)",
    ),
    repo_url: Optional[str] = typer.Option(
        None,
        "--repo-url",
        "-u",
        help="Repository URL",
    ),
    ref: Optional[str] = typer.Option(
        None,
        "--ref",
        help="Git ref (branch, tag, or commit)",
    ),
    output_dir: Path = typer.Option(
        Path("."),
        "--output",
        "-o",
        help="Output directory",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing files",
    ),
):
    """
    Initialize a new task with scaffolding.

    Creates task configuration files from a template. Available templates:

    - dev-docks: Full format with rubric and x namespace extensions (default)
    - swebench: SWE-bench compatible format with instance_id
    - harbor: Harbor framework format (task.toml + instruction.md)
    - minimal: Bare minimum fields only
    - nova: Full Nova registry format with all required fields

    Examples:
        docks tasks init "django__fix-csrf-bug"
        docks tasks init "myrepo__add-feature" --template swebench -d hard
        docks tasks init "calcom__rate-limit" -t dev-docks --repo-url https://github.com/calcom/cal.com
    """
    # Validate inputs
    if template not in VALID_TEMPLATES:
        print_error(f"Invalid template '{template}'. Must be one of: {', '.join(VALID_TEMPLATES)}")
        raise typer.Exit(1)

    if difficulty not in VALID_DIFFICULTIES:
        print_error(f"Invalid difficulty '{difficulty}'. Must be one of: {', '.join(VALID_DIFFICULTIES)}")
        raise typer.Exit(1)

    if role not in VALID_ROLES:
        print_error(f"Invalid role '{role}'. Must be one of: {', '.join(VALID_ROLES)}")
        raise typer.Exit(1)

    # Create task directory
    task_dir = output_dir / name
    if task_dir.exists() and not force:
        print_error(f"Directory already exists: {task_dir}")
        console.print("[dim]Use --force to overwrite[/dim]")
        raise typer.Exit(1)

    task_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold]Creating task:[/bold] {name}")
    console.print(f"  Template:   {template}")
    console.print(f"  Difficulty: {difficulty}")
    console.print(f"  Role:       {role}")
    console.print()

    files_created = []

    # Generate task based on template
    if template == "dev-docks":
        task = generate_dev_docks_task(name, title, difficulty, role, repo_url, ref)
        task_file = task_dir / "task.yaml"
        with open(task_file, "w") as f:
            yaml.dump(task, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        files_created.append("task.yaml")

        # Also create instruction.md for easier editing
        instruction_file = task_dir / "instruction.md"
        with open(instruction_file, "w") as f:
            f.write(task["instruction"])
        files_created.append("instruction.md")

        # Create tests directory with template
        tests_dir = task_dir / "tests"
        tests_dir.mkdir(exist_ok=True)
        test_file = tests_dir / "test.sh"
        with open(test_file, "w") as f:
            f.write("""\
#!/bin/bash
# Test script for task validation
# Exit 0 = pass, non-zero = fail

set -e

echo "Running tests..."
# Add your test commands here
# pytest tests/
# npm test
# go test ./...

echo "Tests passed!"
exit 0
""")
        test_file.chmod(0o755)
        files_created.append("tests/test.sh")

    elif template == "swebench":
        task = generate_swebench_task(name, title, difficulty, role, repo_url, ref)
        task_file = task_dir / "task.yaml"
        with open(task_file, "w") as f:
            yaml.dump(task, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        files_created.append("task.yaml")

    elif template == "harbor":
        try:
            import tomli_w
        except ImportError:
            print_error("tomli_w package required for Harbor template")
            console.print("[dim]Install with: pip install tomli-w[/dim]")
            raise typer.Exit(1)

        task = generate_harbor_task(name, title, difficulty, role)
        task_file = task_dir / "task.toml"
        with open(task_file, "wb") as f:
            tomli_w.dump(task, f)
        files_created.append("task.toml")

        # Create instruction.md
        instruction_file = task_dir / "instruction.md"
        with open(instruction_file, "w") as f:
            f.write(f"""\
# {task['task']['title']}

## Objective

Describe what the agent should accomplish.

## Requirements

1. First requirement
2. Second requirement
3. Third requirement

## Hints

- Hint one
- Hint two
""")
        files_created.append("instruction.md")

        # Create environment directory
        env_dir = task_dir / "environment"
        env_dir.mkdir(exist_ok=True)
        dockerfile = env_dir / "Dockerfile"
        with open(dockerfile, "w") as f:
            f.write("""\
FROM python:3.11-slim

WORKDIR /workspace

# Copy requirements if present
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copy source code
COPY . .

CMD ["bash"]
""")
        files_created.append("environment/Dockerfile")

        # Create tests directory
        tests_dir = task_dir / "tests"
        tests_dir.mkdir(exist_ok=True)
        test_file = tests_dir / "run.sh"
        with open(test_file, "w") as f:
            f.write("""\
#!/bin/bash
# Harbor reward script - outputs to /logs/verifier/reward.txt
set -e

mkdir -p /logs/verifier

# Run tests and capture result
if pytest tests/ 2>&1; then
    echo "1.0" > /logs/verifier/reward.txt
else
    echo "0.0" > /logs/verifier/reward.txt
fi
""")
        test_file.chmod(0o755)
        files_created.append("tests/run.sh")

    elif template == "minimal":
        task = generate_minimal_task(name, title, difficulty, role)
        task_file = task_dir / "task.yaml"
        with open(task_file, "w") as f:
            yaml.dump(task, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        files_created.append("task.yaml")

    elif template == "nova":
        task = generate_nova_task(name, title, difficulty, role, repo_url)
        task_file = task_dir / "task.yaml"
        with open(task_file, "w") as f:
            yaml.dump(task, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        files_created.append("task.yaml")

        # Create instruction.md
        instruction_file = task_dir / "instruction.md"
        with open(instruction_file, "w") as f:
            f.write(task["instruction"])
        files_created.append("instruction.md")

    # Print summary
    console.print("[green]Files created:[/green]")
    for f in files_created:
        console.print(f"  {task_dir / f}")

    console.print()
    print_success(f"Task scaffolded: {task_dir}")
    console.print()
    console.print("[dim]Next steps:[/dim]")
    console.print(f"  1. Edit {task_dir / 'task.yaml'} with your task details")
    if (task_dir / "instruction.md").exists():
        console.print(f"  2. Edit {task_dir / 'instruction.md'} with detailed instructions")
    console.print(f"  3. Run: docks tasks validate {task_dir}")


@app.command("validate")
def validate_task(
    path: Path = typer.Argument(..., help="Path to task directory or task.yaml file"),
    strict: bool = typer.Option(
        False,
        "--strict",
        "-s",
        help="Strict mode: validate against full Nova schema",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed validation output",
    ),
):
    """
    Validate a task against the schema.

    Validates task.yaml files for correct structure and required fields.
    Use --strict to validate against the full Nova registry schema.

    Examples:
        docks tasks validate ./myrepo__fix-bug/
        docks tasks validate ./myrepo__fix-bug/task.yaml --strict
    """
    # Determine file to validate
    if path.is_dir():
        yaml_file = path / "task.yaml"
        toml_file = path / "task.toml"
        if yaml_file.exists():
            task_file = yaml_file
        elif toml_file.exists():
            task_file = toml_file
        else:
            print_error(f"No task.yaml or task.toml found in {path}")
            raise typer.Exit(1)
    else:
        task_file = path

    if not task_file.exists():
        print_error(f"File not found: {task_file}")
        raise typer.Exit(1)

    console.print(f"[bold]Validating:[/bold] {task_file}")
    console.print()

    # Load task
    try:
        if task_file.suffix == ".toml":
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib
            with open(task_file, "rb") as f:
                task_data = tomllib.load(f)
            is_toml = True
        else:
            with open(task_file) as f:
                task_data = yaml.safe_load(f)
            is_toml = False
    except Exception as e:
        print_error(f"Failed to parse file: {e}")
        raise typer.Exit(1)

    errors = []
    warnings = []

    # Basic validation (all formats)
    if is_toml:
        # Harbor/TOML format validation
        if "task" not in task_data:
            errors.append("Missing 'task' section")
        else:
            if "name" not in task_data["task"]:
                errors.append("Missing task.name")
            if "title" not in task_data["task"]:
                warnings.append("Missing task.title")
    else:
        # YAML format validation
        # Check for either slug (dev-docks) or id (nova)
        has_slug = "slug" in task_data
        has_id = "id" in task_data

        if not has_slug and not has_id:
            errors.append("Missing 'slug' or 'id' field")

        # Required fields for all YAML formats
        if "instruction" not in task_data:
            errors.append("Missing 'instruction' field")

        # Check difficulty if present
        if "difficulty" in task_data:
            if task_data["difficulty"] not in VALID_DIFFICULTIES:
                errors.append(f"Invalid difficulty '{task_data['difficulty']}'. Must be: {', '.join(VALID_DIFFICULTIES)}")
        else:
            warnings.append("Missing 'difficulty' field")

        # Check agent_role if present
        if "agent_role" in task_data:
            if task_data["agent_role"] not in VALID_ROLES:
                errors.append(f"Invalid agent_role '{task_data['agent_role']}'. Must be: {', '.join(VALID_ROLES)}")
        else:
            warnings.append("Missing 'agent_role' field")

        # Strict mode: validate against Nova schema
        if strict:
            try:
                from jsonschema import Draft7Validator
                schema = load_schema()
                if schema:
                    validator = Draft7Validator(schema)
                    for error in validator.iter_errors(task_data):
                        path_str = ".".join(str(p) for p in error.path) if error.path else "root"
                        errors.append(f"{path_str}: {error.message}")
                else:
                    warnings.append("Could not load Nova schema for strict validation")
            except ImportError:
                warnings.append("jsonschema not installed - skipping strict validation")

        # Nova ID format validation
        if has_id:
            task_id = task_data["id"]
            parts = task_id.split(".")
            if len(parts) < 4:
                errors.append("Task ID must have format: nova.{repo}.{task_name}.v{version}")
            elif parts[0] != "nova":
                errors.append("Task ID must start with 'nova.'")
            elif not parts[-1].startswith("v"):
                errors.append("Version in ID must start with 'v' (e.g., v1, v2)")

    # Print results
    if errors:
        console.print("[red]Validation failed:[/red]")
        for error in errors:
            console.print(f"  [red]✗[/red] {error}")
        if warnings:
            console.print()
            console.print("[yellow]Warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  [yellow]![/yellow] {warning}")
        raise typer.Exit(1)
    else:
        print_success("Task is valid!")
        if warnings:
            console.print()
            console.print("[yellow]Warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  [yellow]![/yellow] {warning}")

        if verbose:
            console.print()
            console.print("[dim]Task details:[/dim]")
            if is_toml:
                console.print(f"  Name:       {task_data.get('task', {}).get('name')}")
                console.print(f"  Title:      {task_data.get('task', {}).get('title')}")
                console.print(f"  Difficulty: {task_data.get('task', {}).get('difficulty')}")
            else:
                console.print(f"  Slug/ID:    {task_data.get('slug') or task_data.get('id')}")
                console.print(f"  Title:      {task_data.get('title')}")
                console.print(f"  Role:       {task_data.get('agent_role')}")
                console.print(f"  Difficulty: {task_data.get('difficulty')}")
                if task_data.get("categories"):
                    console.print(f"  Categories: {', '.join(task_data.get('categories', []))}")


def load_task_config(path: Path) -> dict:
    """Load task configuration from YAML or TOML file."""
    task_yaml = path / "task.yaml"
    task_toml = path / "task.toml"

    if task_yaml.exists():
        with open(task_yaml) as f:
            return yaml.safe_load(f)
    elif task_toml.exists():
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        with open(task_toml, "rb") as f:
            return tomllib.load(f)
    else:
        raise FileNotFoundError(f"No task.yaml or task.toml found in {path}")


def get_sandbox_image(task_data: dict) -> str:
    """Get the Docker image for sandbox from task config."""
    # Try environment.docker_image first
    if "environment" in task_data and "docker_image" in task_data["environment"]:
        return task_data["environment"]["docker_image"]

    # Default to a Python base image
    return "us-west2-docker.pkg.dev/izumi-479101/izumi-repo/docks-python:latest"


def run_sandbox_test(
    task_path: Path,
    task_data: dict,
    image: str,
    timeout_minutes: int = 30,
) -> dict:
    """
    Run task tests in a cloud sandbox.

    Returns dict with:
        - sandbox_id: UUID of the sandbox
        - success: bool indicating overall success
        - checks: list of check results
        - duration_seconds: total duration
    """
    import time
    import httpx

    from ..config import load_config, get_headers
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    if not settings.tenant_id:
        raise ValueError("Tenant ID not configured. Run: docks auth login")
    if not settings.token:
        raise ValueError("Token not configured. Run: docks auth login")

    api_url = settings.api_url
    tenant_id = settings.tenant_id
    headers = get_headers(settings)

    task_name = task_data.get("slug") or task_data.get("id", task_path.name)
    sandbox_id = None
    start_time = time.time()

    try:
        # Step 1: Create sandbox
        console.print("Creating sandbox...", end=" ")
        create_payload = {
            "name": f"task-test-{task_name[:30]}",
            "mode": "ephemeral",
            "image": image,
            "machine_type": "e2-medium",
            "timeout_minutes": timeout_minutes,
            "environment": task_data.get("environment", {}).get("env_vars", {}),
            "startup_script": None,
        }

        with httpx.Client(headers=headers, timeout=60.0) as http:
            resp = http.post(
                f"{api_url}/tenants/{tenant_id}/sandboxes",
                json=create_payload,
            )
            if resp.status_code == 403:
                error_detail = resp.json().get("detail", "")
                if "not enabled" in error_detail:
                    console.print("[red]failed[/red]")
                    raise ValueError(
                        "Sandbox feature is not enabled for your tenant. "
                        "Contact support to enable sandbox testing."
                    )
                raise ValueError(f"Access denied: {error_detail}")
            resp.raise_for_status()
            sandbox = resp.json()
            sandbox_id = sandbox["id"]

        console.print(f"[green]created[/green] ({sandbox_id[:8]})")

        # Step 2: Wait for sandbox to be running
        console.print("Waiting for sandbox...", end=" ")
        max_wait = 180  # 3 minutes max
        poll_interval = 5
        waited = 0

        with httpx.Client(headers=headers, timeout=30.0) as http:
            while waited < max_wait:
                resp = http.get(f"{api_url}/tenants/{tenant_id}/sandboxes/{sandbox_id}")
                resp.raise_for_status()
                sandbox = resp.json()
                status = sandbox["status"]

                if status == "running":
                    console.print("[green]running[/green]")
                    break
                elif status == "failed":
                    console.print("[red]failed[/red]")
                    raise ValueError(f"Sandbox failed: {sandbox.get('status_reason', 'unknown')}")
                else:
                    time.sleep(poll_interval)
                    waited += poll_interval
            else:
                console.print("[red]timeout[/red]")
                raise ValueError("Sandbox did not start within 3 minutes")

        # Step 3: Execute success_checks
        success_checks = task_data.get("success_checks", [])
        if not success_checks:
            console.print("[yellow]No success_checks defined in task[/yellow]")
            # Try tests/test.sh if exists
            test_script = task_path / "tests" / "test.sh"
            if test_script.exists():
                success_checks = [{
                    "name": "test.sh",
                    "command": "/workspace/tests/test.sh",
                    "timeout_seconds": 300,
                }]
                console.print("[dim]Using tests/test.sh[/dim]")

        check_results = []

        console.print()
        console.print("[bold]Running tests:[/bold]")

        with httpx.Client(headers=headers, timeout=600.0) as http:
            for check in success_checks:
                check_name = check.get("name", "unnamed")
                command = check.get("command", "exit 0")
                timeout_secs = check.get("timeout_seconds", 300)

                console.print(f"  {check_name}...", end=" ")

                exec_payload = {
                    "command": command,
                    "timeout_seconds": timeout_secs,
                    "container": "main",
                }

                try:
                    resp = http.post(
                        f"{api_url}/tenants/{tenant_id}/sandboxes/{sandbox_id}/exec",
                        json=exec_payload,
                    )
                    resp.raise_for_status()
                    result = resp.json()

                    exit_code = result.get("exit_code", -1)
                    passed = exit_code == 0

                    check_results.append({
                        "name": check_name,
                        "passed": passed,
                        "exit_code": exit_code,
                        "stdout": result.get("stdout", ""),
                        "stderr": result.get("stderr", ""),
                        "duration_ms": result.get("duration_ms", 0),
                    })

                    if passed:
                        console.print("[green]PASSED[/green]")
                    else:
                        console.print(f"[red]FAILED[/red] (exit {exit_code})")

                except httpx.HTTPStatusError as e:
                    check_results.append({
                        "name": check_name,
                        "passed": False,
                        "exit_code": -1,
                        "error": str(e),
                    })
                    console.print(f"[red]ERROR[/red] ({e})")

        # Calculate overall success
        overall_success = all(r.get("passed", False) for r in check_results)
        duration = time.time() - start_time

        return {
            "sandbox_id": sandbox_id,
            "success": overall_success,
            "checks": check_results,
            "duration_seconds": int(duration),
        }

    finally:
        # Step 4: Cleanup sandbox
        if sandbox_id:
            console.print()
            console.print("Cleaning up sandbox...", end=" ")
            try:
                with httpx.Client(headers=headers, timeout=30.0) as http:
                    resp = http.post(f"{api_url}/tenants/{tenant_id}/sandboxes/{sandbox_id}/stop")
                    if resp.status_code in (200, 202):
                        console.print("[green]done[/green]")
                    else:
                        console.print(f"[yellow]warning[/yellow] ({resp.status_code})")
            except Exception as e:
                console.print(f"[yellow]warning[/yellow] ({e})")


@app.command("test")
def test_task(
    path: Path = typer.Argument(..., help="Path to task directory"),
    agent: str = typer.Option(
        "claude-code",
        "--agent",
        "-a",
        help="Agent to use for testing (not yet implemented)",
    ),
    model: str = typer.Option(
        "claude-sonnet-4-20250514",
        "--model",
        "-m",
        help="Model to use (not yet implemented)",
    ),
    image: Optional[str] = typer.Option(
        None,
        "--image",
        "-i",
        help="Docker image to use (overrides task config)",
    ),
    timeout: int = typer.Option(
        30,
        "--timeout",
        "-T",
        help="Sandbox timeout in minutes",
    ),
    sandbox: bool = typer.Option(
        False,
        "--sandbox",
        "-s",
        help="Run in cloud sandbox (requires auth)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Show what would be done without executing",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed output including stdout/stderr",
    ),
):
    """
    Test a task in a sandbox environment.

    Runs the task's success_checks in a cloud sandbox to verify the task
    is properly configured and tests can execute.

    Note: Agent execution is not yet implemented. Currently only runs
    the success_checks to validate the task environment.

    Examples:
        docks tasks test ./myrepo__fix-bug/ --dry-run
        docks tasks test ./myrepo__fix-bug/ --sandbox
        docks tasks test ./myrepo__fix-bug/ -s --image python:3.11
    """
    if not path.is_dir():
        print_error(f"Not a directory: {path}")
        raise typer.Exit(1)

    # Load task config
    try:
        task_data = load_task_config(path)
    except FileNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to load task config: {e}")
        raise typer.Exit(1)

    task_name = task_data.get("slug") or task_data.get("id", path.name)

    # Determine image
    sandbox_image = image or get_sandbox_image(task_data)

    console.print(f"[bold]Testing task:[/bold] {task_name}")
    console.print(f"  Image:   {sandbox_image}")
    console.print(f"  Timeout: {timeout} minutes")
    console.print(f"  Mode:    {'sandbox' if sandbox else 'local'}")
    console.print()

    if dry_run:
        console.print("[yellow]Dry run - would execute:[/yellow]")
        console.print(f"  1. Create cloud sandbox with image: {sandbox_image}")
        console.print(f"  2. Wait for sandbox to be running")

        success_checks = task_data.get("success_checks", [])
        if success_checks:
            console.print(f"  3. Execute {len(success_checks)} success_checks:")
            for check in success_checks:
                console.print(f"     - {check.get('name')}: {check.get('command')}")
        else:
            console.print(f"  3. No success_checks defined (would look for tests/test.sh)")

        console.print(f"  4. Report results")
        console.print(f"  5. Cleanup sandbox")
        console.print()
        console.print("[dim]Note: Agent execution (--agent) not yet implemented[/dim]")
        return

    if not sandbox:
        print_error("Local testing not yet implemented")
        console.print("[dim]Use --sandbox flag for cloud sandbox testing[/dim]")
        console.print("[dim]Example: docks tasks test ./task-dir/ --sandbox[/dim]")
        raise typer.Exit(1)

    # Run sandbox test
    try:
        result = run_sandbox_test(
            task_path=path,
            task_data=task_data,
            image=sandbox_image,
            timeout_minutes=timeout,
        )
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Sandbox test failed: {e}")
        raise typer.Exit(1)

    # Print summary
    console.print()
    console.print("[bold]Summary:[/bold]")
    console.print(f"  Duration: {result['duration_seconds']}s")

    passed = sum(1 for c in result["checks"] if c.get("passed", False))
    total = len(result["checks"])
    console.print(f"  Tests:    {passed}/{total} passed")

    if verbose and result["checks"]:
        console.print()
        console.print("[bold]Check Details:[/bold]")
        for check in result["checks"]:
            status = "[green]PASSED[/green]" if check.get("passed") else "[red]FAILED[/red]"
            console.print(f"  {check['name']}: {status}")
            if check.get("stdout"):
                console.print(f"    stdout: {check['stdout'][:200]}...")
            if check.get("stderr"):
                console.print(f"    stderr: {check['stderr'][:200]}...")

    console.print()
    if result["success"]:
        print_success("All tests passed!")
    else:
        print_error("Some tests failed")
        raise typer.Exit(1)


@app.command("list-templates")
def list_templates():
    """
    List available task templates.

    Shows all template formats that can be used with 'docks tasks init'.
    """
    console.print("[bold]Available Templates[/bold]")
    console.print()

    templates = [
        ("dev-docks", "Full format with rubric and x namespace (default)", "task.yaml + instruction.md + tests/"),
        ("swebench", "SWE-bench compatible format", "task.yaml with swebench section"),
        ("harbor", "Harbor framework format", "task.toml + instruction.md + environment/ + tests/"),
        ("minimal", "Bare minimum fields only", "task.yaml (minimal)"),
        ("nova", "Full Nova registry format", "task.yaml (all required fields)"),
    ]

    for name, desc, files in templates:
        console.print(f"  [green]{name:12}[/green] - {desc}")
        console.print(f"                Creates: {files}")
        console.print()

    console.print("[dim]Use with: docks tasks init <name> --template <template>[/dim]")


def update_manifest(dataset_path: Path, task_slug: str, task_data: dict) -> bool:
    """
    Update the manifest.yaml file in a dataset to include a new task.

    Returns True if manifest was updated, False if task already exists.
    """
    manifest_path = dataset_path / "manifest.yaml"

    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f) or {}
    else:
        # Create new manifest
        dataset_name = dataset_path.name
        manifest = {
            "name": dataset_name,
            "version": "1.0.0",
            "description": f"Evaluation tasks for {dataset_name}",
            "tasks": [],
        }

    # Check if task already exists
    tasks = manifest.get("tasks", [])
    if task_slug in tasks:
        return False

    # Add task to manifest
    tasks.append(task_slug)
    manifest["tasks"] = sorted(tasks)

    # Update repo_url if available in task
    if "repo_url" in task_data and "repo_url" not in manifest:
        manifest["repo_url"] = task_data["repo_url"]
    if "ref" in task_data and "ref" not in manifest:
        manifest["ref"] = task_data["ref"]

    # Write updated manifest
    with open(manifest_path, "w") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return True


@app.command("push")
def push_task(
    path: Path = typer.Argument(..., help="Path to task directory"),
    dataset: str = typer.Option(
        ...,
        "--dataset",
        "-d",
        help="Dataset name (e.g., 'dev-docks-appsmith', 'swebench-lite')",
    ),
    bucket: str = typer.Option(
        "gs://izumi-harbor-datasets",
        "--bucket",
        "-b",
        help="GCS bucket URL",
    ),
    skip_validate: bool = typer.Option(
        False,
        "--skip-validate",
        help="Skip validation before pushing",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Show what would be uploaded without executing",
    ),
    update_manifest: bool = typer.Option(
        True,
        "--update-manifest/--no-update-manifest",
        help="Update dataset manifest.yaml with new task",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing task in GCS",
    ),
):
    """
    Push a task to GCS dataset bucket.

    Uploads all task files (task.yaml, instruction.md, tests/, etc.) to the
    specified dataset in GCS. Optionally updates the dataset manifest.

    Examples:
        docks tasks push ./myrepo__fix-bug/ --dataset dev-docks-appsmith
        docks tasks push ./myrepo__fix-bug/ -d swebench-lite --dry-run
        docks tasks push ./myrepo__fix-bug/ -d dev-docks-supabase --force
    """
    import subprocess

    if not path.is_dir():
        print_error(f"Not a directory: {path}")
        raise typer.Exit(1)

    # Load task config
    try:
        task_data = load_task_config(path)
    except FileNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to load task config: {e}")
        raise typer.Exit(1)

    task_slug = task_data.get("slug") or task_data.get("id", path.name)
    # Normalize task slug (use directory name if no slug in config)
    if task_slug == path.name and "__" not in task_slug:
        # Use the directory name as slug
        task_slug = path.name

    console.print(f"[bold]Pushing task:[/bold] {task_slug}")
    console.print(f"  Dataset:  {dataset}")
    console.print(f"  Bucket:   {bucket}")
    console.print()

    # Validate first (unless skipped)
    if not skip_validate:
        console.print("[bold]Validating...[/bold]")
        try:
            task_yaml = path / "task.yaml"
            task_toml = path / "task.toml"

            if task_yaml.exists():
                with open(task_yaml) as f:
                    validate_data = yaml.safe_load(f)
            elif task_toml.exists():
                try:
                    import tomllib
                except ImportError:
                    import tomli as tomllib
                with open(task_toml, "rb") as f:
                    validate_data = tomllib.load(f)
            else:
                print_error("No task.yaml or task.toml found")
                raise typer.Exit(1)

            # Basic validation
            errors = []
            if "slug" not in validate_data and "id" not in validate_data:
                if "task" in validate_data and "name" in validate_data["task"]:
                    pass  # TOML format is OK
                else:
                    errors.append("Missing 'slug' or 'id' field")

            if errors:
                for err in errors:
                    console.print(f"  [red]✗[/red] {err}")
                print_error("Validation failed")
                raise typer.Exit(1)

            console.print("  [green]✓[/green] Task is valid")
            console.print()

        except typer.Exit:
            raise
        except Exception as e:
            print_error(f"Validation error: {e}")
            raise typer.Exit(1)

    # Construct GCS paths
    gcs_task_path = f"{bucket}/{dataset}/{task_slug}/"

    # Check if task already exists
    if not force:
        console.print("Checking for existing task...", end=" ")
        result = subprocess.run(
            ["gsutil", "ls", gcs_task_path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            console.print("[yellow]exists[/yellow]")
            print_error(f"Task already exists at {gcs_task_path}")
            console.print("[dim]Use --force to overwrite[/dim]")
            raise typer.Exit(1)
        console.print("[green]ok[/green]")

    # List files to upload
    files_to_upload = []
    for item in path.rglob("*"):
        if item.is_file():
            # Skip hidden files and common ignore patterns
            rel_path = item.relative_to(path)
            if any(part.startswith(".") for part in rel_path.parts):
                continue
            if "__pycache__" in str(rel_path):
                continue
            files_to_upload.append(rel_path)

    console.print(f"[bold]Files to upload ({len(files_to_upload)}):[/bold]")
    for f in files_to_upload:
        console.print(f"  {f}")
    console.print()

    if dry_run:
        console.print("[yellow]Dry run - would execute:[/yellow]")
        console.print(f"  gsutil -m rsync -r {path}/ {gcs_task_path}")
        if update_manifest:
            console.print(f"  Update manifest: {bucket}/{dataset}/manifest.yaml")
        console.print()
        print_info("Use without --dry-run to execute")
        return

    # Upload files
    console.print("[bold]Uploading to GCS...[/bold]")
    result = subprocess.run(
        ["gsutil", "-m", "rsync", "-r", "-x", r"^\.|__pycache__", str(path) + "/", gcs_task_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print_error(f"gsutil upload failed: {result.stderr}")
        raise typer.Exit(1)

    console.print(f"  [green]✓[/green] Uploaded to {gcs_task_path}")

    # Update manifest if requested
    if update_manifest:
        console.print()
        console.print("[bold]Updating manifest...[/bold]")

        # Download current manifest
        manifest_gcs = f"{bucket}/{dataset}/manifest.yaml"
        manifest_local = Path(f"/tmp/manifest_{dataset}.yaml")

        # Try to download existing manifest
        result = subprocess.run(
            ["gsutil", "cp", manifest_gcs, str(manifest_local)],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # Load existing manifest
            with open(manifest_local) as f:
                manifest = yaml.safe_load(f) or {}
        else:
            # Create new manifest
            manifest = {
                "name": dataset,
                "version": "1.0.0",
                "description": f"Evaluation tasks for {dataset}",
                "tasks": [],
            }

        # Update manifest
        tasks = manifest.get("tasks", [])
        if task_slug not in tasks:
            tasks.append(task_slug)
            manifest["tasks"] = sorted(tasks)

            # Update repo_url if in task
            if "repo_url" in task_data and "repo_url" not in manifest:
                manifest["repo_url"] = task_data["repo_url"]
            if "ref" in task_data and "ref" not in manifest:
                manifest["ref"] = task_data["ref"]

            # Write and upload
            with open(manifest_local, "w") as f:
                yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

            result = subprocess.run(
                ["gsutil", "cp", str(manifest_local), manifest_gcs],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                console.print(f"  [yellow]![/yellow] Failed to update manifest: {result.stderr}")
            else:
                console.print(f"  [green]✓[/green] Added {task_slug} to manifest")
        else:
            console.print(f"  [dim]Task already in manifest[/dim]")

    console.print()
    print_success(f"Task pushed: {gcs_task_path}")
    console.print()
    console.print("[dim]View with:[/dim]")
    console.print(f"  gsutil ls {gcs_task_path}")


@app.command("pull")
def pull_task(
    task: str = typer.Argument(..., help="Task slug (e.g., 'appsmith__app-deployment')"),
    dataset: str = typer.Option(
        ...,
        "--dataset",
        "-d",
        help="Dataset name (e.g., 'dev-docks-appsmith')",
    ),
    bucket: str = typer.Option(
        "gs://izumi-harbor-datasets",
        "--bucket",
        "-b",
        help="GCS bucket URL",
    ),
    output_dir: Path = typer.Option(
        Path("."),
        "--output",
        "-o",
        help="Output directory",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing local files",
    ),
):
    """
    Pull a task from GCS to local filesystem.

    Downloads task files from the specified dataset in GCS.

    Examples:
        docks tasks pull appsmith__app-deployment --dataset dev-docks-appsmith
        docks tasks pull django__fix-auth -d swebench-lite -o ./tasks/
    """
    import subprocess

    gcs_task_path = f"{bucket}/{dataset}/{task}/"
    local_path = output_dir / task

    console.print(f"[bold]Pulling task:[/bold] {task}")
    console.print(f"  From:   {gcs_task_path}")
    console.print(f"  To:     {local_path}")
    console.print()

    # Check if task exists in GCS
    result = subprocess.run(
        ["gsutil", "ls", gcs_task_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print_error(f"Task not found: {gcs_task_path}")
        raise typer.Exit(1)

    # Check if local path exists
    if local_path.exists() and not force:
        print_error(f"Local path already exists: {local_path}")
        console.print("[dim]Use --force to overwrite[/dim]")
        raise typer.Exit(1)

    # Create local directory
    local_path.mkdir(parents=True, exist_ok=True)

    # Download files
    console.print("[bold]Downloading...[/bold]")
    result = subprocess.run(
        ["gsutil", "-m", "rsync", "-r", gcs_task_path, str(local_path) + "/"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print_error(f"gsutil download failed: {result.stderr}")
        raise typer.Exit(1)

    # List downloaded files
    files = list(local_path.rglob("*"))
    file_count = len([f for f in files if f.is_file()])

    console.print(f"  [green]✓[/green] Downloaded {file_count} files")
    console.print()
    print_success(f"Task pulled to: {local_path}")


@app.command("list")
def list_tasks(
    dataset: str = typer.Argument(..., help="Dataset name"),
    bucket: str = typer.Option(
        "gs://izumi-harbor-datasets",
        "--bucket",
        "-b",
        help="GCS bucket URL",
    ),
):
    """
    List tasks in a dataset.

    Shows all tasks available in the specified GCS dataset.

    Examples:
        docks tasks list dev-docks-appsmith
        docks tasks list swebench-lite
    """
    import subprocess

    gcs_path = f"{bucket}/{dataset}/"

    console.print(f"[bold]Tasks in {dataset}:[/bold]")
    console.print()

    # Try to read manifest first
    manifest_path = f"{bucket}/{dataset}/manifest.yaml"
    result = subprocess.run(
        ["gsutil", "cat", manifest_path],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        try:
            manifest = yaml.safe_load(result.stdout)
            tasks = manifest.get("tasks", [])
            if tasks:
                for task in sorted(tasks):
                    console.print(f"  {task}")
                console.print()
                console.print(f"[dim]Total: {len(tasks)} tasks[/dim]")
                return
        except Exception:
            pass

    # Fall back to listing directories
    result = subprocess.run(
        ["gsutil", "ls", gcs_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print_error(f"Dataset not found: {gcs_path}")
        raise typer.Exit(1)

    lines = result.stdout.strip().split("\n")
    tasks = []
    for line in lines:
        # Extract task name from path like gs://bucket/dataset/task/
        if line.endswith("/"):
            parts = line.rstrip("/").split("/")
            task_name = parts[-1]
            if task_name and not task_name.startswith("."):
                tasks.append(task_name)

    # Filter out manifest.yaml and other non-task items
    tasks = [t for t in tasks if not t.endswith(".yaml") and not t.endswith(".json")]

    if not tasks:
        print_info(f"No tasks found in {dataset}")
        return

    for task in sorted(tasks):
        console.print(f"  {task}")

    console.print()
    console.print(f"[dim]Total: {len(tasks)} tasks[/dim]")
