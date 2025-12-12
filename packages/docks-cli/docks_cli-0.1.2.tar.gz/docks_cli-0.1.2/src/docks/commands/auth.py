"""Authentication commands."""

from typing import Optional

import typer

from ..config import load_config, save_config, clear_token, CONFIG_FILE
from ..output import console, print_auth_status, print_success, print_error

app = typer.Typer()


@app.command()
def login(
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Docks API URL"),
    tenant_id: Optional[str] = typer.Option(None, "--tenant", "-t", help="Tenant UUID"),
    token: Optional[str] = typer.Option(None, "--token", help="JWT token"),
    profile: str = typer.Option("default", "--profile", "-p", help="Profile name"),
):
    """
    Save authentication credentials.

    Example:
        docks auth login --tenant 64e7ed28-... --token "Bearer eyJ..."
    """
    if not tenant_id and not token and not api_url:
        # Interactive mode - prompt for values
        console.print("[cyan]Docks CLI Login[/cyan]\n")

        if not api_url:
            api_url = typer.prompt(
                "API URL",
                default="https://api.docks.thecontextlab.ai",
            )
        if not tenant_id:
            tenant_id = typer.prompt("Tenant ID")
        if not token:
            token = typer.prompt("JWT Token", hide_input=True)

    save_config(
        profile=profile,
        api_url=api_url,
        tenant_id=tenant_id,
        token=token,
    )

    print_success(f"Credentials saved to {CONFIG_FILE}")
    print_success(f"Profile: {profile}")


@app.command()
def status():
    """Show current authentication status."""
    from ..cli import state

    settings = load_config(state.get("profile", "default"))
    print_auth_status(settings)


@app.command()
def logout():
    """Clear saved authentication credentials."""
    clear_token()
    print_success("Token cleared")


@app.command()
def token(
    tenant_id: str = typer.Option(..., "--tenant", "-t", help="Tenant UUID"),
    role: str = typer.Option("admin", "--role", "-r", help="Role (admin, operator)"),
    api_url: Optional[str] = typer.Option(None, "--api-url", help="API URL"),
):
    """
    Generate a dev token (requires API access).

    This calls the /dev/token endpoint to mint a JWT for testing.
    Only works in development environments.
    """
    import httpx

    from ..cli import state

    settings = load_config(state.get("profile", "default"))
    url = api_url or settings.api_url

    try:
        resp = httpx.post(
            f"{url}/dev/token",
            json={"tenant_id": tenant_id, "role": role},
            timeout=10.0,
        )
        resp.raise_for_status()
        data = resp.json()
        token_value = data.get("token")

        console.print(f"[green]Token generated:[/green]")
        console.print(f"Bearer {token_value}")

        # Optionally save
        if typer.confirm("\nSave to config?"):
            save_config(
                profile=state.get("profile", "default"),
                api_url=url,
                tenant_id=tenant_id,
                token=token_value,
            )
            print_success("Token saved")

    except httpx.HTTPStatusError as e:
        print_error(f"API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print_error(f"Failed to generate token: {e}")
