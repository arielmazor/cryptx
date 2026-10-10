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


def test_cli_help_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["help"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Usage: cryptx" in result.output


def test_cli_help_subcommand():
    runner = CliRunner()
    result = runner.invoke(cli, ["help", "encode"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Usage: cryptx encode" in result.output


def test_cli_subcommand_help():
    runner = CliRunner()
    for cmd in ["encode", "decode", "crypto", "calc", "hash", "pack", "unpack", "analyze"]:
        result = runner.invoke(cli, [cmd, "help"], prog_name="cryptx")
        assert result.exit_code == 0
        assert f"Usage: cryptx {cmd}" in result.output


def test_cli_subcommand_flags():
    runner = CliRunner()
    for flag in ["-h", "--help", "-help"]:
        result = runner.invoke(cli, ["calc", flag], prog_name="cryptx")
        assert result.exit_code == 0
        assert "Multi-base calculator" in result.output
