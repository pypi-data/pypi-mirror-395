"""HTTP client for Docks API."""

import time
from typing import Any, Optional

import httpx

from .config import Settings, get_headers
from .logging import get_logger

logger = get_logger("client")

# Retry configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0  # seconds
DEFAULT_RETRY_BACKOFF = 2.0  # exponential backoff multiplier
RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


class DocksAPIError(Exception):
    """API error with full details for debugging."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
        request_url: Optional[str] = None,
    ):
        self.status_code = status_code
        self.response_body = response_body
        self.request_url = request_url
        super().__init__(message)

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.request_url:
            parts.append(f"URL: {self.request_url}")
        if self.response_body:
            # Truncate long response bodies
            body = self.response_body[:500]
            if len(self.response_body) > 500:
                body += "..."
            parts.append(f"Response: {body}")
        return " | ".join(parts)


def _should_retry(status_code: int) -> bool:
    """Check if request should be retried based on status code."""
    return status_code in RETRYABLE_STATUS_CODES


class DocksClient:
    """Async HTTP client for Docks API."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = settings.api_url.rstrip("/")
        self.tenant_id = settings.tenant_id
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "DocksClient":
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=get_headers(self.settings),
            timeout=30.0,
        )
        return self

    async def __aexit__(self, *args) -> None:
        if self._client:
            await self._client.aclose()

    def _url(self, path: str) -> str:
        """Build URL with tenant prefix."""
        if self.tenant_id:
            return f"/tenants/{self.tenant_id}{path}"
        return path

    async def get(self, path: str, **kwargs) -> httpx.Response:
        """GET request."""
        return await self._client.get(self._url(path), **kwargs)

    async def post(self, path: str, json: Any = None, **kwargs) -> httpx.Response:
        """POST request."""
        return await self._client.post(self._url(path), json=json, **kwargs)

    async def delete(self, path: str, **kwargs) -> httpx.Response:
        """DELETE request."""
        return await self._client.delete(self._url(path), **kwargs)

    # High-level API methods

    async def list_runs(self, limit: int = 20, offset: int = 0) -> list[dict]:
        """List runs for tenant."""
        resp = await self.get("/runs", params={"limit": limit, "offset": offset})
        resp.raise_for_status()
        return resp.json()

    async def get_run(self, run_id: str) -> dict:
        """Get run by ID."""
        resp = await self.get(f"/runs/{run_id}")
        resp.raise_for_status()
        return resp.json()

    async def create_run(
        self, template_id: str, provider: str, params: Optional[dict] = None
    ) -> dict:
        """Create a new run."""
        payload = {
            "template_id": template_id,
            "provider": provider,
            "params": params or {},
        }
        resp = await self.post("/runs", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def stop_run(self, run_id: str) -> dict:
        """Stop a run."""
        resp = await self.post(f"/runs/{run_id}/stop")
        resp.raise_for_status()
        return resp.json()

    async def list_datasets(self) -> list[dict]:
        """List datasets for tenant."""
        resp = await self.get("/datasets")
        resp.raise_for_status()
        return resp.json()

    async def get_dataset(self, dataset_id: str) -> dict:
        """Get dataset by ID."""
        resp = await self.get(f"/datasets/{dataset_id}")
        resp.raise_for_status()
        return resp.json()

    async def list_tasks(self, dataset_id: str) -> list[dict]:
        """List tasks in a dataset."""
        resp = await self.get(f"/datasets/{dataset_id}/tasks")
        resp.raise_for_status()
        return resp.json()

    async def seed_dataset(self, manifest: str, replace: bool = False) -> dict:
        """Seed dataset from manifest."""
        payload = {"manifest": manifest, "replace": replace}
        resp = await self.post("/datasets/seed", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def list_templates(self, limit: int = 50) -> list[dict]:
        """List templates for tenant."""
        resp = await self.get("/templates", params={"limit": limit})
        resp.raise_for_status()
        return resp.json()


class SyncDocksClient:
    """Synchronous HTTP client with retry logic for Docks API."""

    def __init__(
        self,
        settings: Settings,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
    ):
        self.settings = settings
        self.base_url = settings.api_url.rstrip("/")
        self.tenant_id = settings.tenant_id
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff

    def _url(self, path: str) -> str:
        """Build URL with tenant prefix."""
        if self.tenant_id:
            return f"/tenants/{self.tenant_id}{path}"
        return path

    def _request(
        self,
        method: str,
        path: str,
        retry: bool = True,
        **kwargs,
    ) -> httpx.Response:
        """Make a synchronous request with retry logic.

        Args:
            method: HTTP method
            path: API path
            retry: Whether to retry on transient errors
            **kwargs: Additional httpx request arguments

        Returns:
            httpx.Response

        Raises:
            DocksAPIError: On API errors with full debugging info
        """
        url = f"{self.base_url}{self._url(path)}"
        last_error: Optional[Exception] = None
        delay = self.retry_delay

        max_attempts = self.max_retries if retry else 1

        for attempt in range(max_attempts):
            try:
                logger.debug(f"Request: {method} {url} (attempt {attempt + 1}/{max_attempts})")

                with httpx.Client(
                    headers=get_headers(self.settings),
                    timeout=30.0,
                ) as client:
                    resp = client.request(method, url, **kwargs)

                # Check for retryable errors
                if retry and _should_retry(resp.status_code) and attempt < max_attempts - 1:
                    logger.warning(
                        f"Retryable error {resp.status_code} from {url}, "
                        f"retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)
                    delay *= self.retry_backoff
                    continue

                # Raise detailed error for non-success responses
                if resp.status_code >= 400:
                    raise DocksAPIError(
                        message=f"API request failed: {method} {path}",
                        status_code=resp.status_code,
                        response_body=resp.text,
                        request_url=url,
                    )

                logger.debug(f"Response: {resp.status_code}")
                return resp

            except httpx.ConnectError as e:
                last_error = e
                if attempt < max_attempts - 1:
                    logger.warning(f"Connection error: {e}, retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    delay *= self.retry_backoff
                    continue
                raise DocksAPIError(
                    message=f"Connection failed: {e}",
                    request_url=url,
                )

            except httpx.TimeoutException as e:
                last_error = e
                if attempt < max_attempts - 1:
                    logger.warning(f"Request timeout: {e}, retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    delay *= self.retry_backoff
                    continue
                raise DocksAPIError(
                    message=f"Request timeout: {e}",
                    request_url=url,
                )

            except DocksAPIError:
                raise

            except Exception as e:
                raise DocksAPIError(
                    message=f"Unexpected error: {e}",
                    request_url=url,
                )

        # Should not reach here, but just in case
        raise DocksAPIError(
            message=f"Max retries exceeded: {last_error}",
            request_url=url,
        )

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> httpx.Response:
        return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs) -> httpx.Response:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self._request("DELETE", path, **kwargs)

    def list_runs(self, limit: int = 20) -> list[dict]:
        resp = self.get("/runs", params={"limit": limit})
        return resp.json()

    def get_run(self, run_id: str) -> dict:
        resp = self.get(f"/runs/{run_id}")
        return resp.json()

    def list_datasets(self) -> list[dict]:
        resp = self.get("/datasets")
        return resp.json()

    def list_templates(self) -> list[dict]:
        resp = self.get("/templates")
        return resp.json()

    # Harbor API methods
    def list_harbor_runs(self, limit: int = 20) -> list[dict]:
        """List Harbor runs."""
        resp = self.get("/harbor/runs", params={"limit": limit})
        return resp.json()

    def get_harbor_run(self, run_id: str) -> dict:
        """Get Harbor run details."""
        resp = self.get(f"/harbor/runs/{run_id}")
        return resp.json()

    def list_harbor_trials(self, run_id: str) -> list[dict]:
        """List trials for a Harbor run."""
        resp = self.get(f"/harbor/runs/{run_id}/trials")
        return resp.json()

    def get_harbor_trial(self, run_id: str, trial_id: str) -> dict:
        """Get trial details including artifact URIs."""
        resp = self.get(f"/harbor/runs/{run_id}/trials/{trial_id}")
        return resp.json()

    def create_harbor_run(
        self,
        name: str,
        dataset_uri: Optional[str] = None,
        task_slugs: Optional[list[str]] = None,
        agent_variants: Optional[list[dict]] = None,
        max_concurrent: int = 32,
        attempts_per_task: int = 1,
    ) -> dict:
        """Create a new Harbor run."""
        payload = {
            "name": name,
            "max_concurrent": max_concurrent,
            "attempts_per_task": attempts_per_task,
        }
        if dataset_uri:
            payload["dataset_uri"] = dataset_uri
        if task_slugs:
            payload["task_slugs"] = task_slugs
        if agent_variants:
            payload["agent_variants"] = agent_variants

        resp = self.post("/harbor/runs", json=payload)
        return resp.json()

    def start_harbor_run(self, run_id: str) -> dict:
        """Start a queued Harbor run."""
        resp = self.post(f"/harbor/runs/{run_id}/start")
        return resp.json()

    def cancel_harbor_run(self, run_id: str) -> dict:
        """Cancel a running Harbor run."""
        resp = self.post(f"/harbor/runs/{run_id}/cancel")
        return resp.json()
