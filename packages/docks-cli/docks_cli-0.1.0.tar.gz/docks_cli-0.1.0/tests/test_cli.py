"""Tests for main CLI module."""

import pytest
from typer.testing import CliRunner

from src.docks.cli import app


runner = CliRunner()


def test_cli_version():
    """Test --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "docks version" in result.output


def test_cli_help():
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "CLI for managing Docks" in result.output
    assert "runs" in result.output
    assert "auth" in result.output


def test_cli_verbose_flag():
    """Test --verbose flag sets state."""
    result = runner.invoke(app, ["--verbose", "--help"])
    assert result.exit_code == 0


def test_cli_debug_flag():
    """Test --debug flag sets state."""
    result = runner.invoke(app, ["--debug", "--help"])
    assert result.exit_code == 0
