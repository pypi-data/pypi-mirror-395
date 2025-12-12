"""Tests for output formatting module."""

import pytest
from datetime import datetime, timezone, timedelta

from src.docks.output import (
    format_time_ago,
    status_color,
)


class TestFormatTimeAgo:
    """Tests for format_time_ago function."""

    def test_none_input(self):
        """Test with None input."""
        assert format_time_ago(None) == "-"

    def test_just_now(self):
        """Test time within last minute."""
        now = datetime.now(timezone.utc)
        result = format_time_ago(now.isoformat())
        assert result == "just now"

    def test_minutes_ago(self):
        """Test time a few minutes ago."""
        past = datetime.now(timezone.utc) - timedelta(minutes=5)
        result = format_time_ago(past.isoformat())
        assert "m ago" in result

    def test_hours_ago(self):
        """Test time a few hours ago."""
        past = datetime.now(timezone.utc) - timedelta(hours=3)
        result = format_time_ago(past.isoformat())
        assert "h ago" in result

    def test_days_ago(self):
        """Test time a few days ago."""
        past = datetime.now(timezone.utc) - timedelta(days=5)
        result = format_time_ago(past.isoformat())
        assert "d ago" in result


class TestStatusColor:
    """Tests for status_color function."""

    def test_ready_status(self):
        """Test ready status is green."""
        assert status_color("ready") == "green"
        assert status_color("completed") == "green"
        assert status_color("passed") == "green"

    def test_running_status(self):
        """Test running status is blue."""
        assert status_color("running") == "blue"
        assert status_color("provisioning") == "blue"

    def test_pending_status(self):
        """Test pending status is yellow."""
        assert status_color("pending") == "yellow"
        assert status_color("queued") == "yellow"

    def test_failed_status(self):
        """Test failed status is red."""
        assert status_color("failed") == "red"
        assert status_color("error") == "red"

    def test_unknown_status(self):
        """Test unknown status defaults to white."""
        assert status_color("unknown") == "white"
        assert status_color("custom") == "white"

    def test_case_insensitive(self):
        """Test status matching is case insensitive."""
        assert status_color("READY") == "green"
        assert status_color("Ready") == "green"
        assert status_color("FAILED") == "red"
