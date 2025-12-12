"""Tests for HTTP client."""

import pytest
from unittest.mock import MagicMock, patch
import httpx

from src.docks.client import (
    DocksAPIError,
    SyncDocksClient,
    _should_retry,
    DEFAULT_MAX_RETRIES,
    RETRYABLE_STATUS_CODES,
)
from src.docks.config import Settings


class TestDocksAPIError:
    """Tests for DocksAPIError."""

    def test_basic_error(self):
        """Test error with message only."""
        error = DocksAPIError("Something went wrong")
        assert str(error) == "Something went wrong"

    def test_error_with_status_code(self):
        """Test error with status code."""
        error = DocksAPIError("Failed", status_code=404)
        assert "404" in str(error)

    def test_error_with_url(self):
        """Test error with request URL."""
        error = DocksAPIError("Failed", request_url="https://api.example.com/test")
        assert "api.example.com" in str(error)

    def test_error_with_response_body(self):
        """Test error with response body."""
        error = DocksAPIError("Failed", response_body='{"error": "not found"}')
        assert "not found" in str(error)

    def test_error_truncates_long_body(self):
        """Test that long response bodies are truncated."""
        long_body = "x" * 1000
        error = DocksAPIError("Failed", response_body=long_body)
        error_str = str(error)
        assert "..." in error_str
        assert len(error_str) < 600


class TestShouldRetry:
    """Tests for retry logic."""

    def test_retryable_status_codes(self):
        """Test that specific status codes trigger retry."""
        for code in RETRYABLE_STATUS_CODES:
            assert _should_retry(code) is True

    def test_non_retryable_status_codes(self):
        """Test that other status codes don't trigger retry."""
        for code in [200, 201, 400, 401, 403, 404, 405]:
            assert _should_retry(code) is False


class TestSyncDocksClient:
    """Tests for SyncDocksClient."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings(
            api_url="https://api.example.com",
            tenant_id="test-tenant",
            token="test-token",
        )

    def test_client_initialization(self, settings):
        """Test client initializes correctly."""
        client = SyncDocksClient(settings)
        assert client.base_url == "https://api.example.com"
        assert client.tenant_id == "test-tenant"
        assert client.max_retries == DEFAULT_MAX_RETRIES

    def test_url_with_tenant(self, settings):
        """Test URL building with tenant prefix."""
        client = SyncDocksClient(settings)
        url = client._url("/runs")
        assert url == "/tenants/test-tenant/runs"

    def test_url_without_tenant(self, settings):
        """Test URL building without tenant."""
        settings.tenant_id = None
        client = SyncDocksClient(settings)
        url = client._url("/health")
        assert url == "/health"

    @patch("src.docks.client.httpx.Client")
    def test_get_request(self, mock_client_cls, settings):
        """Test GET request."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "run-1"}]
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.request.return_value = mock_response
        mock_client_cls.return_value = mock_client

        client = SyncDocksClient(settings)
        result = client.list_runs()

        assert result == [{"id": "run-1"}]

    @patch("src.docks.client.httpx.Client")
    def test_raises_error_on_failure(self, mock_client_cls, settings):
        """Test that errors are raised for failed requests."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.request.return_value = mock_response
        mock_client_cls.return_value = mock_client

        client = SyncDocksClient(settings, max_retries=1)
        with pytest.raises(DocksAPIError) as exc_info:
            client.get("/runs/nonexistent")

        assert exc_info.value.status_code == 404
