# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner
from pristy_support.cli import main


def test_cli_version():
    """Test that --version flag works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_help():
    """Test that --help flag works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Pristy Support" in result.output


def test_audit_help():
    """Test that audit --help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["audit", "--help"])
    assert result.exit_code == 0
    assert "audit" in result.output.lower()


def test_system_check_help():
    """Test that system-check --help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["system-check", "--help"])
    assert result.exit_code == 0


def test_logs_check_help():
    """Test that logs-check --help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["logs-check", "--help"])
    assert result.exit_code == 0


def test_database_check_help():
    """Test that database-check --help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["database-check", "--help"])
    assert result.exit_code == 0


def test_config_check_help():
    """Test that config-check --help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["config-check", "--help"])
    assert result.exit_code == 0
