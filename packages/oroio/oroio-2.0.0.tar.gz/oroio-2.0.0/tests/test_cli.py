"""Tests for CLI commands"""

import pytest
from click.testing import CliRunner
from oroio.cli import cli


def test_cli_help():
    """Test CLI help command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'oroio' in result.output
    assert 'Factory Droid' in result.output


def test_version_command():
    """Test version command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['version'])
    assert result.exit_code == 0
    assert 'version' in result.output.lower()


def test_config_show_command():
    """Test config show command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['config', 'show'])
    assert result.exit_code == 0
    assert 'Configuration' in result.output or 'Server' in result.output


def test_config_set_server_command():
    """Test config set-server command"""
    runner = CliRunner()
    test_url = "https://test.example.com"
    result = runner.invoke(cli, ['config', 'set-server', test_url])
    assert result.exit_code == 0
    assert test_url in result.output


def test_list_command_unauthenticated():
    """Test list command without authentication"""
    runner = CliRunner()
    result = runner.invoke(cli, ['list'])
    # Should fail or prompt for authentication
    assert 'Not authenticated' in result.output or 'login' in result.output.lower()
