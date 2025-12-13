# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pristy Support is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pristy Support.  If not, see <https://www.gnu.org/licenses/>.

"""Permission detection utilities."""

import os
import subprocess
from typing import Tuple
from . import logger as log_utils


def is_root() -> bool:
    """Check if running as root user."""
    return os.geteuid() == 0


def has_sudo() -> bool:
    """Check if user has sudo privileges."""
    try:
        cmd = ["sudo", "-n", "true"]
        log_utils.log_command(cmd, "Checking sudo privileges")
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=2,
        )
        log_utils.log_command_result(result.returncode)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def can_use_systemctl() -> bool:
    """Check if systemctl commands are available."""
    try:
        cmd = ["systemctl", "--version"]
        log_utils.log_command(cmd, "Checking systemctl availability")
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=2,
        )
        log_utils.log_command_result(result.returncode)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def can_use_journalctl() -> bool:
    """Check if journalctl is available and accessible."""
    try:
        # Try without sudo first
        cmd = ["journalctl", "-n", "0"]
        log_utils.log_command(cmd, "Checking journalctl availability")
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=2,
        )
        log_utils.log_command_result(result.returncode)
        if result.returncode == 0:
            return True

        # Try with sudo if available
        if has_sudo():
            cmd = ["sudo", "journalctl", "-n", "0"]
            log_utils.log_command(cmd, "Checking journalctl with sudo")
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=2,
            )
            log_utils.log_command_result(result.returncode)
            return result.returncode == 0

        return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def can_use_docker() -> bool:
    """Check if Docker commands are available."""
    try:
        cmd = ["docker", "ps"]
        log_utils.log_command(cmd, "Checking Docker availability")
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=5,
        )
        log_utils.log_command_result(result.returncode)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_command_prefix() -> list:
    """Get command prefix (empty list or ['sudo']) based on permissions."""
    if is_root():
        return []
    elif has_sudo():
        return ["sudo"]
    else:
        return []


def detect_permissions() -> dict:
    """Detect available permissions and capabilities."""
    return {
        "is_root": is_root(),
        "has_sudo": has_sudo(),
        "can_use_systemctl": can_use_systemctl(),
        "can_use_journalctl": can_use_journalctl(),
        "can_use_docker": can_use_docker(),
        "command_prefix": get_command_prefix(),
    }


def format_permissions_report(perms: dict) -> str:
    """Format permissions detection results as a readable string."""
    lines = [
        "Permission Detection:",
        f"  Root user: {'Yes' if perms['is_root'] else 'No'}",
        f"  Sudo available: {'Yes' if perms['has_sudo'] else 'No'}",
        f"  Systemctl: {'Available' if perms['can_use_systemctl'] else 'Not available'}",
        f"  Journalctl: {'Available' if perms['can_use_journalctl'] else 'Not available'}",
        f"  Docker: {'Available' if perms['can_use_docker'] else 'Not available'}",
    ]
    return "\n".join(lines)
