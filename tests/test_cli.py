"""Tests for CLI options and flags."""

from click.testing import CliRunner
from cryptx.cli import cli


def test_cli_version_long():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_cli_version_short():
    runner = CliRunner()
    result = runner.invoke(cli, ["-v"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_cli_help_dash_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["-help"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Usage: cryptx" in result.output
    assert "-v, --version" in result.output
    assert "-h, -help, --help" in result.output


def test_cli_help_short():
    runner = CliRunner()
    result = runner.invoke(cli, ["-h"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Usage: cryptx" in result.output


def test_subcommand_dash_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["calc", "-help"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Multi-base calculator" in result.output
