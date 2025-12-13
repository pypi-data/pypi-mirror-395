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

"""Logging utilities for Pristy support tool."""

import logging
import sys
from typing import List


# Global logger instance
_logger = None


def setup_logging(debug: bool = False):
    """Setup logging configuration."""
    global _logger

    level = logging.DEBUG if debug else logging.INFO

    # Create logger
    _logger = logging.getLogger("pristy_support")
    _logger.setLevel(level)

    # Remove existing handlers
    _logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    # Create formatter
    if debug:
        formatter = logging.Formatter("%(levelname)s [%(name)s] %(message)s")
    else:
        formatter = logging.Formatter("%(message)s")

    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    return _logger


def get_logger():
    """Get the logger instance."""
    global _logger
    if _logger is None:
        _logger = setup_logging(debug=False)
    return _logger


def log_command(cmd: List[str], description: str = None):
    """Log a command that will be executed."""
    logger = get_logger()
    if description:
        logger.debug(f"🔧 {description}")
    logger.debug(f"   $ {' '.join(cmd)}")


def log_command_result(returncode: int, stdout: str = None, stderr: str = None):
    """Log the result of a command execution."""
    logger = get_logger()
    if returncode == 0:
        logger.debug(f"   ✓ Command succeeded (exit code: 0)")
    else:
        # Red color for error messages
        logger.debug(f"   \033[91m✗ Command failed (exit code: {returncode})\033[0m")
        if stderr:
            logger.debug(f"   \033[91mstderr: {stderr[:200]}\033[0m")


def log_docker_exec(container: str, cmd: List[str]):
    """Log a docker exec command."""
    logger = get_logger()
    logger.debug(f"🐳 Executing in container '{container}':")
    logger.debug(f"   $ {' '.join(cmd)}")


def log_file_read(file_path: str):
    """Log a file read operation."""
    logger = get_logger()
    logger.debug(f"📄 Reading file: {file_path}")


def log_file_write(file_path: str):
    """Log a file write operation."""
    logger = get_logger()
    logger.debug(f"📝 Writing file: {file_path}")


def log_info(message: str):
    """Log an informational message."""
    logger = get_logger()
    logger.debug(f"ℹ️  {message}")
