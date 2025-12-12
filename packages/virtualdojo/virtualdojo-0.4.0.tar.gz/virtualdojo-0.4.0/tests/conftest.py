"""Pytest configuration and fixtures."""

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / "virtualdojo"
    config_dir.mkdir()
    return config_dir
