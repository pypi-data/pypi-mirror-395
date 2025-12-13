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

"""Docker utilities for Pristy support tool."""

import subprocess
from typing import List, Dict, Optional
from . import logger as log_utils
from .. import config_manager


def docker_is_available() -> bool:
    """Check if Docker is available and accessible."""
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def docker_ps(all_containers: bool = False) -> List[Dict[str, str]]:
    """List Docker containers."""
    try:
        cmd = [
            "docker",
            "ps",
            "--format",
            "{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}|{{.CreatedAt}}",
        ]
        if all_containers:
            cmd.append("-a")

        log_utils.log_command(cmd, "Listing Docker containers")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        log_utils.log_command_result(result.returncode)

        if result.returncode != 0:
            return []

        containers = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 5:
                containers.append(
                    {
                        "id": parts[0],
                        "name": parts[1],
                        "status": parts[2],
                        "image": parts[3],
                        "created": parts[4],
                    }
                )

        return containers
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def docker_inspect(container_name: str) -> Optional[Dict]:
    """Inspect a Docker container to get detailed information."""
    try:
        cmd = ["docker", "inspect", container_name]
        log_utils.log_command(cmd, f"Inspecting container '{container_name}'")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        log_utils.log_command_result(result.returncode)

        if result.returncode != 0:
            return None

        import json

        data = json.loads(result.stdout)
        if data and len(data) > 0:
            return data[0]
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        return None


def docker_exec(
    container_name: str, command: List[str], timeout: int = 30
) -> Optional[str]:
    """Execute a command inside a Docker container."""
    try:
        cmd = ["docker", "exec", "-i", container_name] + command
        log_utils.log_docker_exec(container_name, command)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        log_utils.log_command_result(
            result.returncode,
            result.stdout if result.returncode != 0 else None,
            result.stderr,
        )

        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def get_container_memory_limit(container_name: str) -> Optional[int]:
    """Get memory limit for a Docker container in bytes."""
    inspect_data = docker_inspect(container_name)
    if not inspect_data:
        return None

    try:
        memory = inspect_data.get("HostConfig", {}).get("Memory", 0)
        return memory if memory > 0 else None
    except (KeyError, TypeError):
        return None


def get_pristy_containers() -> List[Dict[str, str]]:
    """Get list of Pristy-related containers."""
    cfg = config_manager.get_config()
    pristy_names = cfg.get("docker.container_patterns", [])

    all_containers = docker_ps(all_containers=True)

    pristy_containers = []
    for container in all_containers:
        if any(name in container["name"] for name in pristy_names):
            pristy_containers.append(container)

    return pristy_containers
