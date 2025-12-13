"""Prebaked image commands."""

import subprocess
from pathlib import Path
from typing import Optional

import typer

from ..config import load_config
from ..output import console, print_images_table, print_error, print_success, print_info

app = typer.Typer()


@app.command("list")
def list_images(
    repo: Optional[str] = typer.Option(None, "--repo", "-r", help="Filter by repo name"),
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status (prebaked/raw)"
    ),
):
    """List prebaked images in GCS."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))
    bucket = settings.gcs_bucket.rstrip("/")

    try:
        # List images from GCS
        result = subprocess.run(
            ["gsutil", "ls", "-l", f"{bucket}/swebench-images/"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print_error(f"gsutil error: {result.stderr}")
            raise typer.Exit(1)

        # Parse output
        images = []
        for line in result.stdout.strip().split("\n"):
            if ".tar.gz" in line:
                parts = line.split()
                if len(parts) >= 3:
                    size_bytes = int(parts[0])
                    size_mb = size_bytes / 1024 / 1024
                    path = parts[-1]
                    instance_id = path.split("/")[-1].replace(".tar.gz", "")

                    # Determine status based on size
                    img_status = "prebaked" if size_mb > 1100 else "raw"

                    # Apply filters
                    if repo and repo.lower() not in instance_id.lower():
                        continue
                    if status and status != img_status:
                        continue

                    images.append(
                        {
                            "instance_id": instance_id,
                            "size": f"{size_mb:.1f} MB",
                            "status": img_status,
                            "modified": parts[1] if len(parts) > 1 else "",
                        }
                    )

        if not images:
            console.print("[dim]No images found[/dim]")
            return

        print_images_table(images)
        console.print(f"\n[dim]Total: {len(images)} images[/dim]")

    except FileNotFoundError:
        print_error("gsutil not found. Install Google Cloud SDK.")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to list images: {e}")
        raise typer.Exit(1)


@app.command("prebake")
def prebake_image(
    instance_id: Optional[str] = typer.Argument(None, help="Instance ID to prebake"),
    repo: Optional[str] = typer.Option(
        None, "--repo", "-r", help="Prebake all images for repo"
    ),
    all_images: bool = typer.Option(False, "--all", help="Prebake all missing images"),
    parallel: int = typer.Option(20, "--parallel", "-j", help="Max parallel builds"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done"),
    estimate: bool = typer.Option(False, "--estimate", help="Show cost estimate only"),
):
    """
    Build prebaked images via Cloud Build.

    Examples:
        docks images prebake pallets__flask-4045
        docks images prebake --repo flask --parallel 10
        docks images prebake --all --estimate
    """
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    # Find the deploy script
    script_paths = [
        Path(__file__).parent.parent.parent.parent.parent.parent
        / "docks"
        / "swebench-adapter"
        / "deploy_cloudbuild_batch.sh",
        Path.cwd() / "docks" / "swebench-adapter" / "deploy_cloudbuild_batch.sh",
    ]

    script_path = None
    for p in script_paths:
        if p.exists():
            script_path = p
            break

    if estimate or all_images or repo:
        if not script_path:
            print_error("deploy_cloudbuild_batch.sh not found")
            raise typer.Exit(1)

        # Build command
        cmd = [str(script_path)]
        if estimate:
            cmd.append("--estimate")
        elif all_images:
            cmd.append("--prebake-all")
            if dry_run:
                cmd.append("--dry-run")
        elif repo:
            cmd.append(f"--prebake-repo={repo}")
            if dry_run:
                cmd.append("--dry-run")

        # Set environment
        env = {
            "MAX_CONCURRENT": str(parallel),
            "IZUMI_PROJECT": settings.gcp_project,
            "IZUMI_GCS_BUCKET": settings.gcs_bucket,
        }

        try:
            import os

            full_env = os.environ.copy()
            full_env.update(env)

            result = subprocess.run(cmd, env=full_env)
            raise typer.Exit(result.returncode)

        except Exception as e:
            print_error(f"Failed to run script: {e}")
            raise typer.Exit(1)

    elif instance_id:
        # Single image prebake via Cloud Build
        print_info(f"Submitting Cloud Build for {instance_id}...")

        try:
            cmd = [
                "gcloud",
                "builds",
                "submit",
                "--no-source",
                f"--config={script_path.parent / 'cloudbuild_batch.yaml'}"
                if script_path
                else "--config=cloudbuild_batch.yaml",
                f"--substitutions=_INSTANCE_ID={instance_id}",
                f"--project={settings.gcp_project}",
                f"--region={settings.gcp_region}",
            ]

            if dry_run:
                console.print(f"[dim]Would run: {' '.join(cmd)}[/dim]")
                return

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print_success(f"Build submitted for {instance_id}")
                console.print("[dim]Monitor with: docks images status --ongoing[/dim]")
            else:
                print_error(f"Build failed: {result.stderr}")
                raise typer.Exit(1)

        except FileNotFoundError:
            print_error("gcloud not found. Install Google Cloud SDK.")
            raise typer.Exit(1)

    else:
        print_error("Specify instance_id, --repo, or --all")
        raise typer.Exit(1)


@app.command("status")
def build_status(
    build_id: Optional[str] = typer.Argument(None, help="Build ID to check"),
    ongoing: bool = typer.Option(False, "--ongoing", help="Show only ongoing builds"),
    limit: int = typer.Option(10, "--limit", "-n", help="Number of builds to show"),
):
    """Check Cloud Build status."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    try:
        if build_id:
            # Get specific build
            cmd = [
                "gcloud",
                "builds",
                "describe",
                build_id,
                f"--project={settings.gcp_project}",
            ]
        else:
            # List builds
            cmd = [
                "gcloud",
                "builds",
                "list",
                f"--project={settings.gcp_project}",
                f"--limit={limit}",
                '--format=table(id,status,createTime,duration,images)',
            ]
            if ongoing:
                cmd.append("--ongoing")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            console.print(result.stdout)
        else:
            print_error(f"Failed: {result.stderr}")
            raise typer.Exit(1)

    except FileNotFoundError:
        print_error("gcloud not found. Install Google Cloud SDK.")
        raise typer.Exit(1)


@app.command("validate")
def validate_image(
    instance_id: str = typer.Argument(..., help="Instance ID to validate"),
):
    """Validate that a prebaked image has all prerequisites."""
    image_name = f"swebench-{instance_id}:latest"

    console.print(f"[cyan]Validating {image_name}...[/cyan]\n")

    checks = [
        ("Node.js", ["node", "--version"]),
        ("Claude CLI", ["which", "claude"]),
        ("google-cloud-storage", ["python", "-c", "import google.cloud.storage; print('OK')"]),
        ("/adapter/", ["ls", "/adapter/"]),
    ]

    all_passed = True

    for name, cmd in checks:
        try:
            result = subprocess.run(
                ["docker", "run", "--rm", image_name] + cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                output = result.stdout.strip().split("\n")[0]
                console.print(f"  [green]OK[/green] {name}: {output}")
            else:
                console.print(f"  [red]FAIL[/red] {name}: {result.stderr.strip()}")
                all_passed = False

        except subprocess.TimeoutExpired:
            console.print(f"  [red]FAIL[/red] {name}: timeout")
            all_passed = False
        except Exception as e:
            console.print(f"  [red]FAIL[/red] {name}: {e}")
            all_passed = False

    console.print()
    if all_passed:
        print_success("Image validated successfully")
    else:
        print_error("Image validation failed")
        raise typer.Exit(1)


@app.command("estimate")
def estimate_cost():
    """Show cost estimate for prebaking all images."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))

    # Find and run the deploy script with --estimate
    script_paths = [
        Path(__file__).parent.parent.parent.parent.parent.parent
        / "docks"
        / "swebench-adapter"
        / "deploy_cloudbuild_batch.sh",
        Path.cwd() / "docks" / "swebench-adapter" / "deploy_cloudbuild_batch.sh",
    ]

    script_path = None
    for p in script_paths:
        if p.exists():
            script_path = p
            break

    if not script_path:
        # Fallback to hardcoded estimate
        console.print("""
[cyan]SWE-bench Cloud Build Cost Estimate[/cyan]

Configuration:
  Total instances:           300
  Concurrent builds:         20

Cloud Build Cost (E2_HIGHCPU_8 @ $0.016/min):
  Per image:                 5 min x $0.016 = $0.08
  Total (300 images):        $24

Network Egress:
  Upload (~1.2GB/image):     360GB x $0.12 = $43

Storage (monthly):
  Base images:               ~300GB @ $0.02/GB = $6/mo
  Prebaked images:           ~345GB @ $0.02/GB = $7/mo

==============================================
TOTAL ONE-TIME COST:         ~$67
MONTHLY STORAGE:             ~$13/month
==============================================
""")
        return

    import os

    env = os.environ.copy()
    env["IZUMI_PROJECT"] = settings.gcp_project
    env["IZUMI_GCS_BUCKET"] = settings.gcs_bucket

    subprocess.run([str(script_path), "--estimate"], env=env)
