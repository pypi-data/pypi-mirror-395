"""Docks API client with consolidated error handling.

This module provides a simplified API client that:
- Maps all HTTP errors to a single APIError exception
- Provides user-friendly error display via display() method
- Enforces server invariants (e.g., create must return id)
- Supports debug mode for verbose HTTP logging

Commands should only import DocksAPI and APIError from this module.
"""

from typing import Any, Optional

import httpx
import typer

from .config import Settings, load_config


class APIError(Exception):
    """
    Single exception type for all API failures.

    Raised for:
    - HTTP errors (non-2xx responses)
    - Connection/timeout failures
    - Invalid JSON responses
    - Server invariant violations (e.g., missing id in create response)

    Attributes:
        message: Human-readable error description
        status_code: HTTP status code if applicable
        detail: Structured error response from API
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        detail: Optional[dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(message)

    def display(self) -> None:
        """Print user-friendly error to stderr.

        Formats the error for CLI output, extracting structured details
        like missing_tasks and hints from the API response.
        """
        # Main error message
        if self.status_code:
            typer.echo(f"Error ({self.status_code}): {self.message}", err=True)
        else:
            typer.echo(f"Error: {self.message}", err=True)

        # Show missing tasks if present (common validation error)
        missing = self.detail.get("missing_tasks")
        if missing:
            if isinstance(missing, list):
                typer.echo(f"  Missing tasks: {', '.join(missing)}", err=True)
            else:
                typer.echo(f"  Missing tasks: {missing}", err=True)

        # Show hint if provided
        hint = self.detail.get("hint")
        if hint:
            typer.echo(f"  Hint: {hint}", err=True)

        # Show additional context for specific status codes
        if self.status_code == 401:
            typer.echo("  Run: docks auth login", err=True)
        elif self.status_code == 403:
            typer.echo("  Check that your token has access to this tenant/resource.", err=True)
        elif self.status_code == 404:
            typer.echo("  Use 'docks runs eval-list' to see available runs.", err=True)
        elif self.status_code and self.status_code >= 500:
            typer.echo("  This is a server-side issue. Try again later.", err=True)


class DocksAPI:
    """
    Docks API client with consolidated error handling.

    All HTTP details and error mapping are consolidated here.
    Commands import only DocksAPI and APIError.

    Example:
        api = DocksAPI.from_config()
        try:
            run = api.create_harbor_run({"name": "test"})
        except APIError as e:
            e.display()
            raise typer.Exit(1)
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        tenant_id: str,
        timeout: float = 30.0,
        debug: bool = False,
    ):
        """
        Construct client from config/env.

        Args:
            base_url: API base URL (from DOCKS_BASE_URL or config)
            token: Bearer token (from DOCKS_API_TOKEN or config)
            tenant_id: Tenant UUID (from config)
            timeout: Request timeout in seconds (default 30s)
            debug: Enable verbose HTTP logging (request/response details)
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.tenant_id = tenant_id
        self.timeout = timeout
        self.debug = debug

        if debug:
            import logging
            logging.basicConfig(level=logging.DEBUG)
            # Enable httpx debug logging
            logging.getLogger("httpx").setLevel(logging.DEBUG)
            logging.getLogger("httpcore").setLevel(logging.DEBUG)

    @classmethod
    def from_config(cls, profile: str = "default", debug: bool = False) -> "DocksAPI":
        """Create DocksAPI from config file.

        Args:
            profile: Config profile name (default: "default")
            debug: Enable verbose HTTP logging

        Returns:
            Configured DocksAPI instance

        Raises:
            APIError: If required config is missing
        """
        settings = load_config(profile)
        if not settings.tenant_id:
            raise APIError("Tenant ID not configured. Run: docks auth login")
        if not settings.token:
            raise APIError("Token not configured. Run: docks auth login")
        return cls(
            base_url=settings.api_url,
            token=settings.token,
            tenant_id=settings.tenant_id,
            debug=debug,
        )

    def _url(self, path: str) -> str:
        """Build full URL with tenant prefix."""
        return f"{self.base_url}/tenants/{self.tenant_id}{path}"

    def _headers(self) -> dict:
        """Build request headers."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _parse_error(self, response: httpx.Response) -> dict:
        """Extract structured error from API response.

        Returns:
            Dict with 'message' and any additional error details
        """
        try:
            body = response.json()
            detail = body.get("detail", {})
            if isinstance(detail, dict):
                # Ensure we have a message field
                if "message" not in detail:
                    detail["message"] = str(detail) or f"HTTP {response.status_code}"
                return detail
            # detail is a string
            return {"message": str(detail)}
        except Exception:
            text = response.text[:200] if response.text else "No response body"
            return {"message": text}

    def _request_json(self, method: str, path: str, **kwargs) -> dict:
        """
        Internal helper that all domain methods use.

        Behavior:
        1. Sends HTTP request using httpx.Client with base_url, Authorization, timeout
        2. Calls raise_for_status() to enforce 2xx/3xx-only success
        3. On HTTPStatusError, ConnectError, TimeoutException: wraps into APIError
        4. Parses JSON body; if parsing fails, raises APIError ("invalid JSON from API")

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., "/harbor/runs")
            **kwargs: Additional httpx request arguments (json, params, etc.)

        Returns:
            Parsed JSON dict on success

        Raises:
            APIError: On any failure
        """
        url = self._url(path)

        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.request(
                    method,
                    url,
                    headers=self._headers(),
                    **kwargs,
                )
                resp.raise_for_status()

        except httpx.HTTPStatusError as e:
            detail = self._parse_error(e.response)
            raise APIError(
                message=detail.get("message", f"HTTP {e.response.status_code}"),
                status_code=e.response.status_code,
                detail=detail,
            )

        except httpx.ConnectError:
            raise APIError(
                message="Unable to reach API server",
                detail={"hint": "Check your network connection and API URL setting."},
            )

        except httpx.TimeoutException:
            raise APIError(
                message="Request timed out",
                detail={"hint": "The server may be overloaded. Try again later."},
            )

        # Parse JSON
        try:
            return resp.json()
        except Exception:
            raise APIError(
                message="Invalid JSON from API",
                status_code=resp.status_code,
            )

    def _request_json_list(self, method: str, path: str, **kwargs) -> list:
        """Like _request_json but expects a list response."""
        result = self._request_json(method, path, **kwargs)
        if not isinstance(result, list):
            # Some endpoints return {"items": [...]}
            if isinstance(result, dict) and "items" in result:
                return result["items"]
            return [result] if result else []
        return result

    # --- Harbor/Evaluation Run Methods ---

    def create_harbor_run(self, payload: dict) -> dict:
        """
        Create a Harbor evaluation run.

        Args:
            payload: Run configuration dict with keys:
                - name: Run name (required)
                - dataset_uri: GCS URI to dataset (optional)
                - task_slugs: List of task slugs to run (optional)
                - agent_variants: Agent configuration list (optional)
                - max_concurrent: Max parallel trials (default 32)
                - attempts_per_task: Retries per task (default 1)

        Returns:
            Created run dict with id, status, etc.

        Raises:
            APIError: On HTTP error or missing id in response
        """
        data = self._request_json("POST", "/harbor/runs", json=payload)

        # Invariant: create must return an id
        if "id" not in data:
            raise APIError(
                message="Server returned success but no run ID",
                detail={"hint": "This is a server bug. Contact support."},
            )

        return data

    def start_harbor_run(self, run_id: str) -> dict:
        """Start a queued Harbor run.

        Args:
            run_id: Run UUID

        Returns:
            Updated run dict with status='running'
        """
        return self._request_json("POST", f"/harbor/runs/{run_id}/start")

    def cancel_harbor_run(self, run_id: str) -> dict:
        """Cancel a running Harbor run.

        Args:
            run_id: Run UUID

        Returns:
            Updated run dict with status='cancelled'
        """
        return self._request_json("POST", f"/harbor/runs/{run_id}/cancel")

    def list_harbor_runs(self, limit: int = 20) -> list[dict]:
        """List Harbor runs.

        Args:
            limit: Max runs to return

        Returns:
            List of run dicts
        """
        return self._request_json_list("GET", "/harbor/runs", params={"limit": limit})

    def get_harbor_run(self, run_id: str) -> dict:
        """Get Harbor run details.

        Args:
            run_id: Run UUID

        Returns:
            Run dict with status, trials, etc.
        """
        return self._request_json("GET", f"/harbor/runs/{run_id}")

    def list_harbor_trials(self, run_id: str) -> list[dict]:
        """List trials for a Harbor run.

        Args:
            run_id: Run UUID

        Returns:
            List of trial dicts
        """
        return self._request_json_list("GET", f"/harbor/runs/{run_id}/trials")

    def get_harbor_trial(self, run_id: str, trial_id: str) -> dict:
        """Get trial details including artifact URIs.

        Args:
            run_id: Run UUID
            trial_id: Trial UUID

        Returns:
            Trial dict with logs_uri, trajectory_uri, etc.
        """
        return self._request_json("GET", f"/harbor/runs/{run_id}/trials/{trial_id}")

    # --- Dataset Methods ---

    def list_datasets(self) -> list[dict]:
        """List datasets for tenant."""
        return self._request_json_list("GET", "/datasets")

    def get_dataset(self, dataset_id: str) -> dict:
        """Get dataset details."""
        return self._request_json("GET", f"/datasets/{dataset_id}")

    def list_tasks(self, dataset_id: str) -> list[dict]:
        """List tasks in a dataset."""
        return self._request_json_list("GET", f"/datasets/{dataset_id}/tasks")

    # --- Run Methods (legacy) ---

    def list_runs(self, limit: int = 20) -> list[dict]:
        """List runs for tenant."""
        return self._request_json_list("GET", "/runs", params={"limit": limit})

    def get_run(self, run_id: str) -> dict:
        """Get run by ID."""
        return self._request_json("GET", f"/runs/{run_id}")

    def stop_run(self, run_id: str) -> dict:
        """Stop a run."""
        return self._request_json("POST", f"/runs/{run_id}/stop")

    # --- Template Methods ---

    def list_templates(self, limit: int = 50) -> list[dict]:
        """List templates for tenant."""
        return self._request_json_list("GET", "/templates", params={"limit": limit})

    # --- Sandbox Methods ---

    def create_sandbox(self, task_slug: str, dataset_uri: Optional[str] = None) -> dict:
        """Create a sandbox environment for debugging.

        Args:
            task_slug: Task to run in sandbox
            dataset_uri: Optional dataset URI

        Returns:
            Sandbox dict with id, status, connection info
        """
        payload = {"task_slug": task_slug}
        if dataset_uri:
            payload["dataset_uri"] = dataset_uri

        data = self._request_json("POST", "/sandboxes", json=payload)

        # Invariant: create must return an id
        if "id" not in data:
            raise APIError(
                message="Server returned success but no sandbox ID",
                detail={"hint": "This is a server bug. Contact support."},
            )

        return data

    def list_sandboxes(self) -> list[dict]:
        """List active sandboxes."""
        return self._request_json_list("GET", "/sandboxes")

    def get_sandbox(self, sandbox_id: str) -> dict:
        """Get sandbox details."""
        return self._request_json("GET", f"/sandboxes/{sandbox_id}")

    def delete_sandbox(self, sandbox_id: str) -> dict:
        """Delete a sandbox."""
        return self._request_json("DELETE", f"/sandboxes/{sandbox_id}")

    def create_sandbox_full(self, payload: dict) -> dict:
        """Create a sandbox with full configuration.

        Args:
            payload: Full sandbox configuration dict with keys:
                - name: Sandbox name (required)
                - mode: interactive or ephemeral
                - image: Docker image
                - machine_type: e2-medium, e2-standard-2, etc.
                - timeout_minutes: Timeout in minutes
                - startup_script: Optional startup script
                - environment: Optional env vars

        Returns:
            Sandbox dict with id, status, connection info
        """
        data = self._request_json("POST", "/sandboxes", json=payload)

        # Invariant: create must return an id
        if "id" not in data:
            raise APIError(
                message="Server returned success but no sandbox ID",
                detail={"hint": "This is a server bug. Contact support."},
            )

        return data

    def list_sandboxes_filtered(
        self, limit: int = 20, status: Optional[str] = None
    ) -> list[dict]:
        """List sandboxes with optional filtering.

        Args:
            limit: Max sandboxes to return
            status: Filter by status (running, pending, etc.)

        Returns:
            List of sandbox dicts
        """
        params = {"limit": limit}
        if status:
            params["status"] = status
        return self._request_json_list("GET", "/sandboxes", params=params)

    def stop_sandbox(self, sandbox_id: str) -> dict:
        """Stop a sandbox.

        Args:
            sandbox_id: Sandbox UUID

        Returns:
            Updated sandbox dict
        """
        return self._request_json("POST", f"/sandboxes/{sandbox_id}/stop")

    def exec_in_sandbox(
        self, sandbox_id: str, command: str, timeout_seconds: int = 60
    ) -> dict:
        """Execute a command in a sandbox.

        Args:
            sandbox_id: Sandbox UUID
            command: Command to execute
            timeout_seconds: Command timeout

        Returns:
            Execution result with stdout, stderr, exit_code
        """
        return self._request_json(
            "POST",
            f"/sandboxes/{sandbox_id}/exec",
            json={"command": command, "timeout_seconds": timeout_seconds},
        )

    def extend_sandbox(self, sandbox_id: str, additional_minutes: int) -> dict:
        """Extend sandbox timeout.

        Args:
            sandbox_id: Sandbox UUID
            additional_minutes: Minutes to add

        Returns:
            Updated sandbox dict with new expires_at
        """
        return self._request_json(
            "POST",
            f"/sandboxes/{sandbox_id}/extend",
            json={"additional_minutes": additional_minutes},
        )
