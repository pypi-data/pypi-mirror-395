"""Tests for main CLI."""

from typer.testing import CliRunner

from virtualdojo.cli import app

runner = CliRunner()


def test_help():
    """Test help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "VirtualDojo CLI" in result.stdout


def test_version():
    """Test version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "VirtualDojo CLI version" in result.stdout


def test_auth_help():
    """Test auth subcommand help."""
    result = runner.invoke(app, ["auth", "--help"])
    assert result.exit_code == 0
    assert "login" in result.stdout
    assert "logout" in result.stdout
    assert "whoami" in result.stdout


def test_records_help():
    """Test records subcommand help."""
    result = runner.invoke(app, ["records", "--help"])
    assert result.exit_code == 0
    assert "list" in result.stdout
    assert "get" in result.stdout
    assert "create" in result.stdout
    assert "update" in result.stdout
    assert "delete" in result.stdout


def test_schema_help():
    """Test schema subcommand help."""
    result = runner.invoke(app, ["schema", "--help"])
    assert result.exit_code == 0
    assert "objects" in result.stdout
    assert "describe" in result.stdout
    assert "fields" in result.stdout


def test_config_help():
    """Test config subcommand help."""
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "show" in result.stdout
    assert "profile" in result.stdout
