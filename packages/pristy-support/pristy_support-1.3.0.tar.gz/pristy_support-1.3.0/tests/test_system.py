# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for system module."""

import pytest
from unittest.mock import patch, MagicMock
from pristy_support.modules import system


def test_format_size_human_bytes():
    """Test formatting bytes."""
    assert system._format_size_human(100) == "100B"
    assert system._format_size_human(512) == "512B"


def test_format_size_human_kilobytes():
    """Test formatting kilobytes."""
    assert system._format_size_human(1024) == "1.0K"
    assert system._format_size_human(2048) == "2.0K"
    assert system._format_size_human(1536) == "1.5K"


def test_format_size_human_megabytes():
    """Test formatting megabytes."""
    assert system._format_size_human(1024 * 1024) == "1.0M"
    assert system._format_size_human(1024 * 1024 * 10) == "10.0M"


def test_format_size_human_gigabytes():
    """Test formatting gigabytes."""
    assert system._format_size_human(1024 * 1024 * 1024) == "1.0G"
    assert system._format_size_human(1024 * 1024 * 1024 * 100) == "100.0G"


def test_format_size_human_terabytes():
    """Test formatting terabytes."""
    assert system._format_size_human(1024 * 1024 * 1024 * 1024) == "1.0T"


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.os.path.exists")
@patch("pristy_support.modules.system.permissions.detect_permissions")
@patch("pristy_support.modules.system.subprocess.run")
def test_get_directory_sizes_success(
    mock_subprocess, mock_perms, mock_exists, mock_config
):
    """Test get_directory_sizes with successful du command."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["/test/path"]

    # Mock path exists
    mock_exists.return_value = True

    # Mock permissions (no sudo)
    mock_perms.return_value = {"sudo_available": False, "is_root": False}

    # Mock subprocess result
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "1073741824    /test/path\n"
    mock_subprocess.return_value = mock_result

    results = system.get_directory_sizes()

    assert len(results) == 1
    assert results[0]["path"] == "/test/path"
    assert results[0]["size_human"] == "1.0G"
    assert results[0]["size_bytes"] == 1073741824
    assert results[0]["status"] == "ok"


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.os.path.exists")
def test_get_directory_sizes_not_found(mock_exists, mock_config):
    """Test get_directory_sizes with non-existent directory."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["/nonexistent/path"]

    # Mock path doesn't exist
    mock_exists.return_value = False

    results = system.get_directory_sizes()

    assert len(results) == 1
    assert results[0]["path"] == "/nonexistent/path"
    assert results[0]["size_human"] == "N/A"
    assert results[0]["size_bytes"] == 0
    assert results[0]["status"] == "not_found"


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.os.path.exists")
@patch("pristy_support.modules.system.permissions.detect_permissions")
@patch("pristy_support.modules.system.subprocess.run")
def test_get_directory_sizes_permission_denied(
    mock_subprocess, mock_perms, mock_exists, mock_config
):
    """Test get_directory_sizes with permission denied."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["/test/path"]

    # Mock path exists
    mock_exists.return_value = True

    # Mock permissions (no sudo)
    mock_perms.return_value = {"sudo_available": False, "is_root": False}

    # Mock subprocess result (permission denied)
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_subprocess.return_value = mock_result

    results = system.get_directory_sizes()

    assert len(results) == 1
    assert results[0]["path"] == "/test/path"
    assert results[0]["size_human"] == "N/A"
    assert results[0]["status"] == "permission_denied"


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.os.path.exists")
@patch("pristy_support.modules.system.permissions.detect_permissions")
@patch("pristy_support.modules.system.subprocess.run")
def test_get_directory_sizes_with_sudo(
    mock_subprocess, mock_perms, mock_exists, mock_config
):
    """Test get_directory_sizes with sudo."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["/test/path"]

    # Mock path exists
    mock_exists.return_value = True

    # Mock permissions (sudo available, not root)
    mock_perms.return_value = {"has_sudo": True, "is_root": False}

    # Mock subprocess result
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "1048576    /test/path\n"
    mock_subprocess.return_value = mock_result

    results = system.get_directory_sizes()

    # Verify sudo was used in command
    mock_subprocess.assert_called_once()
    call_args = mock_subprocess.call_args
    assert call_args[0][0] == ["sudo", "-n", "du", "-sb", "/test/path"]

    assert len(results) == 1
    assert results[0]["status"] == "ok"


# Tests for get_disk_partitions


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.permissions.detect_permissions")
@patch("pristy_support.modules.system.subprocess.run")
def test_get_disk_partitions_success(mock_subprocess, mock_perms, mock_config):
    """Test get_disk_partitions with successful execution."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["ext4", "xfs"]

    # Mock permissions (no sudo)
    mock_perms.return_value = {"has_sudo": False, "is_root": False}

    # Mock subprocess result with JSON output
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = """{
        "filesystems": [
            {
                "source": "/dev/sda1",
                "fstype": "xfs",
                "size": "200G",
                "used": "127.2G",
                "avail": "72.8G",
                "use%": "64%",
                "target": "/"
            },
            {
                "source": "/dev/sdb1",
                "fstype": "ext4",
                "size": "500G",
                "used": "450G",
                "avail": "50G",
                "use%": "90%",
                "target": "/data"
            }
        ]
    }"""
    mock_subprocess.return_value = mock_result

    results = system.get_disk_partitions()

    # Verify findmnt was called correctly
    mock_subprocess.assert_called_once()
    call_args = mock_subprocess.call_args
    assert call_args[0][0] == [
        "findmnt",
        "--uniq",
        "-o",
        "SOURCE,FSTYPE,SIZE,USED,AVAIL,USE%,TARGET",
        "--types",
        "ext4,xfs",
        "-J",
    ]

    # Verify results
    assert len(results) == 2

    # First partition (64% usage -> OK)
    assert results[0]["source"] == "/dev/sda1"
    assert results[0]["fstype"] == "xfs"
    assert results[0]["size"] == "200G"
    assert results[0]["used"] == "127.2G"
    assert results[0]["avail"] == "72.8G"
    assert results[0]["use_percent"] == "64%"
    assert results[0]["target"] == "/"
    assert results[0]["status"] == "OK"

    # Second partition (90% usage -> WARNING)
    assert results[1]["source"] == "/dev/sdb1"
    assert results[1]["status"] == "WARNING"


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.permissions.detect_permissions")
@patch("pristy_support.modules.system.subprocess.run")
def test_get_disk_partitions_critical_status(mock_subprocess, mock_perms, mock_config):
    """Test get_disk_partitions with critical disk usage."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["ext4"]

    # Mock permissions
    mock_perms.return_value = {"has_sudo": False, "is_root": False}

    # Mock subprocess result with 96% usage
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = """{
        "filesystems": [
            {
                "source": "/dev/sda1",
                "fstype": "ext4",
                "size": "100G",
                "used": "96G",
                "avail": "4G",
                "use%": "96%",
                "target": "/"
            }
        ]
    }"""
    mock_subprocess.return_value = mock_result

    results = system.get_disk_partitions()

    assert len(results) == 1
    assert results[0]["status"] == "CRITICAL"
    assert results[0]["use_percent"] == "96%"


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.permissions.detect_permissions")
@patch("pristy_support.modules.system.subprocess.run")
def test_get_disk_partitions_with_sudo(mock_subprocess, mock_perms, mock_config):
    """Test get_disk_partitions with sudo."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["ext4"]

    # Mock permissions (sudo available, not root)
    mock_perms.return_value = {"has_sudo": True, "is_root": False}

    # Mock subprocess result
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = '{"filesystems": []}'
    mock_subprocess.return_value = mock_result

    system.get_disk_partitions()

    # Verify sudo was used in command
    mock_subprocess.assert_called_once()
    call_args = mock_subprocess.call_args
    assert call_args[0][0][0:2] == ["sudo", "-n"]


@patch("pristy_support.modules.system.config_manager.get_config")
@patch("pristy_support.modules.system.permissions.detect_permissions")
@patch("pristy_support.modules.system.subprocess.run")
def test_get_disk_partitions_command_failure(mock_subprocess, mock_perms, mock_config):
    """Test get_disk_partitions when findmnt fails."""
    # Mock configuration
    mock_config.return_value.get.return_value = ["ext4"]

    # Mock permissions
    mock_perms.return_value = {"has_sudo": False, "is_root": False}

    # Mock subprocess result with failure
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "findmnt: command not found"
    mock_subprocess.return_value = mock_result

    results = system.get_disk_partitions()

    assert len(results) == 0
