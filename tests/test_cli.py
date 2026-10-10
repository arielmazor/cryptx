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


def test_cli_decode_auto():
    runner = CliRunner()
    result = runner.invoke(cli, ["decode", "QXJpZWwgTWF6b3I="], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Ariel Mazor" in result.output


def test_cli_direct_ciphers():
    runner = CliRunner()
    result = runner.invoke(cli, ["rot13", "Hello"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Uryyb" in result.output


def test_cli_crack_rainbow():
    runner = CliRunner()
    result = runner.invoke(cli, ["crack", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "CRACKED" in result.output
    assert "'password'" in result.output


def test_cli_crack_unseen_gives_hashcat():
    runner = CliRunner()
    result = runner.invoke(cli, ["crack", "1111111111111111111111111111111111111111111111111111111111111111"], prog_name="cryptx")
    assert result.exit_code == 0
    assert "hashcat -m 1400" in result.output


def test_cli_analyze_shows_detected_type():
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "QXJpZWwgTWF6b3I="], prog_name="cryptx")
    assert result.exit_code == 0
    assert "Detected Types" in result.output
    assert "Base64" in result.output

