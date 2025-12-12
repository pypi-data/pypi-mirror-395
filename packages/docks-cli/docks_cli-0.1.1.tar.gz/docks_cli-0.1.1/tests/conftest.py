"""Pytest fixtures for CLI tests."""

import pytest
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner


@pytest.fixture
def runner():
    """CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_settings():
    """Mock settings with test values."""
    settings = MagicMock()
    settings.api_url = "https://api.example.com"
    settings.tenant_id = "test-tenant-123"
    settings.token = "test-token"
    settings.profile = "default"
    settings.gcp_project = "test-project"
    settings.gcs_bucket = "gs://test-bucket"
    return settings


@pytest.fixture
def mock_client(mock_settings):
    """Mock SyncDocksClient."""
    with patch("src.docks.commands.runs.SyncDocksClient") as mock_cls:
        client = MagicMock()
        mock_cls.return_value = client
        yield client


@pytest.fixture
def mock_load_config(mock_settings):
    """Mock load_config to return test settings."""
    with patch("src.docks.commands.runs.load_config") as mock:
        mock.return_value = mock_settings
        yield mock
