"""Tests for configuration module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.docks.config import Settings, load_config, get_headers


class TestSettings:
    """Tests for Settings class."""

    def test_default_values(self):
        """Test default settings values."""
        settings = Settings()
        assert "izumi-api" in settings.api_url
        assert settings.tenant_id is None
        assert settings.token is None
        assert settings.profile == "default"
        assert settings.gcp_project == "izumi-479101"

    def test_custom_values(self):
        """Test settings with custom values."""
        settings = Settings(
            api_url="https://custom.api.com",
            tenant_id="custom-tenant",
            token="custom-token",
        )
        assert settings.api_url == "https://custom.api.com"
        assert settings.tenant_id == "custom-tenant"
        assert settings.token == "custom-token"


class TestGetHeaders:
    """Tests for get_headers function."""

    def test_headers_without_token(self):
        """Test headers without auth token."""
        settings = Settings(token=None)
        headers = get_headers(settings)
        assert "Content-Type" in headers
        assert "Authorization" not in headers

    def test_headers_with_bearer_token(self):
        """Test headers with Bearer token."""
        settings = Settings(token="Bearer test-token")
        headers = get_headers(settings)
        assert headers["Authorization"] == "Bearer test-token"

    def test_headers_with_raw_token(self):
        """Test headers with raw token (auto-adds Bearer)."""
        settings = Settings(token="raw-token")
        headers = get_headers(settings)
        assert headers["Authorization"] == "Bearer raw-token"
