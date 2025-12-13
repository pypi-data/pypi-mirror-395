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

"""System checks module for Pristy support tool."""

import os
import subprocess
import psutil
import socket
import platform
import json
from typing import List, Dict, Optional, Tuple
from ..utils import docker_utils, permissions, logger as log_utils
from .. import config_manager
from . import access_logs


def get_system_info() -> Dict[str, str]:
    """Get basic system information."""
    log_utils.log_info("Collecting system information (hostname, OS)")

    try:
        hostname = socket.gethostname()
        log_utils.log_info(f"  Hostname: {hostname}")
    except Exception:
        hostname = "Unknown"

    try:
        os_type = platform.system()
        os_release = platform.release()
        os_version = platform.version()

        # Try to get more detailed info from /etc/os-release
        dist_name = "Unknown"
        dist_version = "Unknown"
        try:
            log_utils.log_file_read("/etc/os-release")
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        dist_name = line.split("=", 1)[1].strip().strip('"')
                    elif line.startswith("VERSION=") and dist_version == "Unknown":
                        dist_version = line.split("=", 1)[1].strip().strip('"')
        except (FileNotFoundError, PermissionError):
            pass

        if dist_name == "Unknown":
            dist_name = f"{os_type} {os_release}"

    except Exception:
        os_type = "Unknown"
        dist_name = "Unknown"
        dist_version = "Unknown"

    return {
        "hostname": hostname,
        "os_type": os_type,
        "os_distribution": dist_name,
        "os_version": dist_version,
    }


def get_cpu_info() -> Dict[str, any]:
    """Get CPU information."""
    log_utils.log_info("Collecting CPU information")

    cpu_count = os.cpu_count() or 1
    log_utils.log_info(f"  CPU count: {cpu_count} cores")

    # Try to get CPU model
    cpu_model = "Unknown"
    try:
        log_utils.log_file_read("/proc/cpuinfo")
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("model name"):
                    cpu_model = line.split(":", 1)[1].strip()
                    break
    except (FileNotFoundError, PermissionError):
        pass

    return {
        "count": cpu_count,
        "model": cpu_model,
    }


def get_memory_info() -> Dict[str, any]:
    """Get memory information."""
    log_utils.log_info("Collecting memory information (RAM and Swap)")

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    log_utils.log_info(
        f"  RAM: {round(mem.total / (1024**3), 2)}GB total, {round(mem.percent, 1)}% used"
    )
    log_utils.log_info(
        f"  Swap: {round(swap.total / (1024**3), 2)}GB total, {round(swap.percent, 1)}% used"
    )

    return {
        "total_gb": round(mem.total / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "free_gb": round(mem.available / (1024**3), 2),
        "percent_used": round(mem.percent, 1),
        "swap_total_gb": round(swap.total / (1024**3), 2),
        "swap_used_gb": round(swap.used / (1024**3), 2),
        "swap_percent_used": round(swap.percent, 1),
    }


def get_network_interfaces() -> List[Dict[str, str]]:
    """Get network interfaces and their IP addresses (excluding virtual interfaces)."""
    log_utils.log_info("Collecting network interfaces (excluding virtual interfaces)")

    interfaces = []

    # Get network interfaces using psutil
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()

    # List of interface prefixes to exclude (virtual interfaces)
    exclude_prefixes = ["docker", "veth", "br-", "virbr", "vmnet", "vbox", "lo"]

    for interface_name, addrs in net_if_addrs.items():
        # Skip loopback and virtual interfaces
        if interface_name == "lo" or any(
            interface_name.startswith(prefix) for prefix in exclude_prefixes
        ):
            continue

        # Get interface status
        is_up = net_if_stats.get(interface_name, None)
        if is_up and not is_up.isup:
            continue  # Skip interfaces that are down

        # Extract IPv4 and IPv6 addresses
        ipv4_addresses = []
        ipv6_addresses = []

        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4_addresses.append(addr.address)
            elif addr.family == socket.AF_INET6:
                # Skip link-local IPv6 addresses
                if not addr.address.startswith("fe80:"):
                    ipv6_addresses.append(addr.address)

        if ipv4_addresses or ipv6_addresses:
            ipv4_str = ", ".join(ipv4_addresses) if ipv4_addresses else "N/A"
            log_utils.log_info(f"  Found interface: {interface_name} ({ipv4_str})")
            interfaces.append(
                {
                    "name": interface_name,
                    "ipv4": ipv4_str,
                    "ipv6": ", ".join(ipv6_addresses) if ipv6_addresses else "N/A",
                }
            )

    return interfaces


def get_docker_info() -> Dict[str, any]:
    """Get Docker version and configuration."""
    log_utils.log_info("Collecting Docker information")

    if not docker_utils.docker_is_available():
        log_utils.log_info("  Docker not available")
        return {
            "available": False,
            "version": "N/A",
        }

    # Get Docker version
    version = "Unknown"
    try:
        cmd = ["docker", "version", "--format", "{{.Server.Version}}"]
        log_utils.log_command(cmd, "Getting Docker version")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Read daemon.json
    daemon_config = {}
    daemon_config_path = "/etc/docker/daemon.json"
    try:
        log_utils.log_file_read(daemon_config_path)
        with open(daemon_config_path, "r") as f:
            daemon_config = json.load(f)
        log_utils.log_info(
            f"  Found {len(daemon_config)} daemon configuration parameters"
        )
    except FileNotFoundError:
        log_utils.log_info(f"  Daemon config not found: {daemon_config_path}")
    except (PermissionError, json.JSONDecodeError) as e:
        log_utils.log_info(f"  Could not read daemon config: {e}")

    return {
        "available": True,
        "version": version,
        "daemon_config": daemon_config,
        "daemon_config_path": daemon_config_path if daemon_config else None,
    }


def get_docker_networks() -> List[Dict[str, any]]:
    """Get Docker networks and their IP ranges."""
    log_utils.log_info("Collecting Docker networks")

    if not docker_utils.docker_is_available():
        return []

    networks = []

    try:
        cmd = ["docker", "network", "ls", "--format", "{{.Name}}"]
        log_utils.log_command(cmd, "Listing Docker networks")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return []

        network_names = result.stdout.strip().split("\n")

        for network_name in network_names:
            if not network_name:
                continue

            # Get network details
            cmd_inspect = ["docker", "network", "inspect", network_name]
            log_utils.log_command(cmd_inspect, f"Inspecting network '{network_name}'")
            result_inspect = subprocess.run(
                cmd_inspect,
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result_inspect.returncode == 0:
                try:
                    network_data = json.loads(result_inspect.stdout)
                    if network_data and len(network_data) > 0:
                        net = network_data[0]

                        # Extract IPAM config
                        subnets = []
                        gateways = []
                        if (
                            "IPAM" in net
                            and "Config" in net["IPAM"]
                            and net["IPAM"]["Config"] is not None
                        ):
                            for config in net["IPAM"]["Config"]:
                                if config and "Subnet" in config:
                                    subnets.append(config["Subnet"])
                                if config and "Gateway" in config:
                                    gateways.append(config["Gateway"])

                        subnet_str = ", ".join(subnets) if subnets else "N/A"
                        log_utils.log_info(
                            f"  Found network: {network_name} ({subnet_str})"
                        )
                        networks.append(
                            {
                                "name": network_name,
                                "driver": net.get("Driver", "Unknown"),
                                "scope": net.get("Scope", "Unknown"),
                                "subnets": subnets,
                                "gateways": gateways,
                            }
                        )
                except json.JSONDecodeError:
                    pass

    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return networks


def check_systemd_services(perms: dict) -> List[Dict[str, str]]:
    """Check status of Pristy systemd services."""
    if not perms["can_use_systemctl"]:
        return []

    cfg = config_manager.get_config()
    services = cfg.get("system.services", [])
    services_status = []
    cmd_prefix = perms["command_prefix"]

    for service in services:
        try:
            # Check if service exists
            cmd = cmd_prefix + ["systemctl", "list-unit-files", f"{service}.service"]
            log_utils.log_command(cmd, f"Checking if service '{service}' exists")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5,
            )

            if service not in result.stdout:
                continue  # Service not installed

            # Check if service is enabled
            cmd_enabled = cmd_prefix + ["systemctl", "is-enabled", service]
            log_utils.log_command(cmd_enabled, f"Checking if '{service}' is enabled")
            result_enabled = subprocess.run(
                cmd_enabled,
                capture_output=True,
                text=True,
                timeout=5,
            )
            is_enabled = result_enabled.returncode == 0

            # Check if service is active
            cmd_active = cmd_prefix + ["systemctl", "is-active", service]
            log_utils.log_command(cmd_active, f"Checking if '{service}' is active")
            result_active = subprocess.run(
                cmd_active,
                capture_output=True,
                text=True,
                timeout=5,
            )
            is_active = result_active.returncode == 0

            services_status.append(
                {
                    "name": service,
                    "enabled": "Yes" if is_enabled else "No",
                    "active": "Active" if is_active else "Inactive",
                    "status": "OK" if (is_enabled and is_active) else "WARNING",
                }
            )

        except subprocess.TimeoutExpired:
            services_status.append(
                {
                    "name": service,
                    "enabled": "Unknown",
                    "active": "Unknown",
                    "status": "ERROR",
                }
            )

    return services_status


def check_docker_containers() -> List[Dict[str, str]]:
    """Check status of Docker containers."""
    if not docker_utils.docker_is_available():
        return []

    containers = docker_utils.get_pristy_containers()
    results = []

    for container in containers:
        is_running = "Up" in container["status"]
        results.append(
            {
                "name": container["name"],
                "status": container["status"],
                "image": container["image"],
                "created": container.get("created", "N/A"),
                "state": "Running" if is_running else "Stopped",
                "health": "OK" if is_running else "WARNING",
            }
        )

    return results


def check_memory_limits() -> Dict[str, any]:
    """Check memory configuration and limits."""
    cfg = config_manager.get_config()
    min_ram = cfg.get("system.memory.min_ram_gb", 8)
    min_swap = cfg.get("system.memory.min_swap_gb", 2)

    # Get total system memory
    mem = psutil.virtual_memory()
    total_ram_gb = mem.total / (1024**3)
    available_ram_gb = mem.available / (1024**3)

    # Get swap information
    swap = psutil.swap_memory()
    total_swap_gb = swap.total / (1024**3)

    # Check Docker container memory limits
    containers = docker_utils.get_pristy_containers()
    container_limits = []
    total_limit_bytes = 0

    for container in containers:
        limit = docker_utils.get_container_memory_limit(container["name"])
        if limit:
            limit_gb = limit / (1024**3)
            container_limits.append(
                {
                    "name": container["name"],
                    "limit_gb": round(limit_gb, 2),
                    "limit_bytes": limit,
                }
            )
            total_limit_bytes += limit

    total_limit_gb = total_limit_bytes / (1024**3) if total_limit_bytes > 0 else 0

    # Determine status
    status = "OK"
    issues = []

    if total_ram_gb < min_ram:
        status = "WARNING"
        issues.append(
            f"Total RAM ({total_ram_gb:.1f}GB) is below minimum ({min_ram}GB)"
        )

    if total_swap_gb < min_swap:
        status = "WARNING"
        issues.append(f"Swap ({total_swap_gb:.1f}GB) is below minimum ({min_swap}GB)")

    if total_limit_bytes > 0 and total_limit_gb > total_ram_gb * 0.9:
        status = "ERROR"
        issues.append(
            f"Sum of container limits ({total_limit_gb:.1f}GB) exceeds 90% of total RAM ({total_ram_gb:.1f}GB)"
        )

    return {
        "total_ram_gb": round(total_ram_gb, 2),
        "available_ram_gb": round(available_ram_gb, 2),
        "total_swap_gb": round(total_swap_gb, 2),
        "container_limits": container_limits,
        "total_limit_gb": round(total_limit_gb, 2),
        "status": status,
        "issues": issues,
    }


def check_swap() -> Dict[str, any]:
    """Check swap configuration."""
    cfg = config_manager.get_config()
    min_swap = cfg.get("system.memory.min_swap_gb", 2)

    swap = psutil.swap_memory()
    total_swap_gb = swap.total / (1024**3)
    used_swap_gb = swap.used / (1024**3)
    percent_used = swap.percent

    status = "OK"
    issues = []

    if total_swap_gb == 0:
        status = "ERROR"
        issues.append("No swap configured")
    elif total_swap_gb < min_swap:
        status = "WARNING"
        issues.append(
            f"Swap size ({total_swap_gb:.1f}GB) is below minimum ({min_swap}GB)"
        )
    elif percent_used > 80:
        status = "WARNING"
        issues.append(f"Swap usage is high ({percent_used:.1f}%)")

    return {
        "total_gb": round(total_swap_gb, 2),
        "used_gb": round(used_swap_gb, 2),
        "percent_used": round(percent_used, 1),
        "status": status,
        "issues": issues,
    }


def check_firewall(perms: dict) -> Dict[str, str]:
    """Check firewall status."""
    cmd_prefix = perms["command_prefix"]

    # Try firewalld first (Red Hat / CentOS / Fedora)
    try:
        cmd = cmd_prefix + ["firewall-cmd", "--state"]
        log_utils.log_command(cmd, "Checking firewalld status")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return {
                "type": "firewalld",
                "status": "Active"
                if "running" in result.stdout.lower()
                else "Inactive",
                "health": "OK",
            }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Try ufw (Ubuntu / Debian)
    try:
        cmd = cmd_prefix + ["ufw", "status"]
        log_utils.log_command(cmd, "Checking ufw status")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            status = "Active" if "active" in result.stdout.lower() else "Inactive"
            return {
                "type": "ufw",
                "status": status,
                "health": "OK" if status == "Active" else "WARNING",
            }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Try iptables
    try:
        cmd = cmd_prefix + ["iptables", "-L", "-n"]
        log_utils.log_command(cmd, "Checking iptables rules")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # Check if there are any rules
            lines = result.stdout.strip().split("\n")
            has_rules = len(lines) > 8  # More than just headers
            return {
                "type": "iptables",
                "status": "Active" if has_rules else "No rules",
                "health": "WARNING" if not has_rules else "OK",
            }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return {
        "type": "None",
        "status": "Not detected",
        "health": "WARNING",
    }


def check_disk_space() -> List[Dict[str, any]]:
    """Check disk space on all relevant partitions."""
    cfg = config_manager.get_config()
    disk_thresholds = cfg.get("system.disk_thresholds", {})
    results = []

    # Get all mounted partitions
    partitions = psutil.disk_partitions()

    # Check each threshold path
    for path, min_free_percent in disk_thresholds.items():
        if not os.path.exists(path):
            continue

        try:
            usage = psutil.disk_usage(path)
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            percent_used = usage.percent
            percent_free = 100 - percent_used

            status = "OK"
            issues = []

            if percent_free < min_free_percent:
                status = "WARNING"
                issues.append(
                    f"Free space ({percent_free:.1f}%) is below threshold ({min_free_percent}%)"
                )

            if percent_free < 5:
                status = "CRITICAL"

            results.append(
                {
                    "path": path,
                    "total_gb": round(total_gb, 2),
                    "used_gb": round(used_gb, 2),
                    "free_gb": round(free_gb, 2),
                    "percent_used": round(percent_used, 1),
                    "percent_free": round(percent_free, 1),
                    "threshold": min_free_percent,
                    "status": status,
                    "issues": issues,
                }
            )

        except (PermissionError, FileNotFoundError):
            results.append(
                {
                    "path": path,
                    "status": "ERROR",
                    "issues": ["Unable to access path"],
                }
            )

    return results


def get_disk_partitions() -> List[Dict[str, any]]:
    """Get disk partition information using findmnt."""
    from ..utils import permissions, logger as log_utils
    import subprocess
    import json

    cfg = config_manager.get_config()
    filesystem_types = cfg.get("system.filesystem_types", ["ext4", "xfs"])
    results = []

    log_utils.log_info(
        f"Collecting disk partition information for types: {', '.join(filesystem_types)}"
    )

    # Check if sudo is available
    perms = permissions.detect_permissions()
    use_sudo = perms.get("has_sudo", False) and not perms.get("is_root", False)

    try:
        # Build findmnt command
        cmd = []
        if use_sudo:
            cmd.extend(["sudo", "-n"])
        cmd.extend(
            [
                "findmnt",
                "--uniq",
                "-o",
                "SOURCE,FSTYPE,SIZE,USED,AVAIL,USE%,TARGET",
                "--types",
                ",".join(filesystem_types),
                "-J",
            ]
        )

        # Execute findmnt command
        log_utils.log_command(cmd, "Getting disk partition information")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0 and result.stdout.strip():
            # Parse JSON output
            data = json.loads(result.stdout)
            filesystems = data.get("filesystems", [])

            log_utils.log_info(f"Found {len(filesystems)} partitions")

            for fs in filesystems:
                source = fs.get("source", "N/A")
                fstype = fs.get("fstype", "N/A")
                size = fs.get("size", "N/A")
                used = fs.get("used", "N/A")
                avail = fs.get("avail", "N/A")
                use_percent_str = fs.get("use%", "0%")
                target = fs.get("target", "N/A")

                # Parse use percentage to determine status
                try:
                    use_percent = float(use_percent_str.rstrip("%"))
                    if use_percent >= 95:
                        status = "CRITICAL"
                    elif use_percent >= 80:
                        status = "WARNING"
                    else:
                        status = "OK"
                except (ValueError, AttributeError):
                    use_percent = 0
                    status = "UNKNOWN"

                log_utils.log_info(
                    f"  {target} ({source}): {used}/{size} ({use_percent_str}) - {status}"
                )

                results.append(
                    {
                        "source": source,
                        "fstype": fstype,
                        "size": size,
                        "used": used,
                        "avail": avail,
                        "use_percent": use_percent_str,
                        "target": target,
                        "status": status,
                    }
                )

        else:
            log_utils.log_info(
                f"  ❌ Failed to execute findmnt (exit code {result.returncode})"
            )
            if result.stderr:
                log_utils.log_info(f"  Error: {result.stderr.strip()}")

    except json.JSONDecodeError as e:
        log_utils.log_info(f"  ❌ Failed to parse findmnt JSON output: {e}")
    except Exception as e:
        log_utils.log_info(f"  ❌ Unexpected error collecting disk partition info: {e}")

    return results


def get_directory_sizes() -> List[Dict[str, any]]:
    """Get size of key directories using du command."""
    from ..utils import permissions, logger as log_utils
    import subprocess

    cfg = config_manager.get_config()
    directory_paths = cfg.get("system.directory_paths", [])
    results = []

    log_utils.log_info(f"Collecting directory sizes for {len(directory_paths)} paths")

    perms = permissions.detect_permissions()
    use_sudo = perms.get("has_sudo", False) and not perms.get("is_root", False)

    for path in directory_paths:
        if not os.path.exists(path):
            log_utils.log_info(f"  ⚠️  Directory not found: {path}")
            results.append(
                {
                    "path": path,
                    "size_human": "N/A",
                    "size_bytes": 0,
                    "status": "not_found",
                }
            )
            continue

        try:
            # Build du command
            cmd = []
            if use_sudo:
                cmd.extend(["sudo", "-n"])
            cmd.extend(["du", "-sb", path])

            # Execute du command
            log_utils.log_command(cmd, f"Getting size of {path}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)

            if result.returncode == 0 and result.stdout.strip():
                # Parse output: "123456789    /path"
                parts = result.stdout.strip().split(None, 1)
                if parts:
                    size_bytes = int(parts[0])
                    size_human = _format_size_human(size_bytes)

                    log_utils.log_info(f"  ✓ {path}: {size_human}")
                    results.append(
                        {
                            "path": path,
                            "size_human": size_human,
                            "size_bytes": size_bytes,
                            "status": "ok",
                        }
                    )
                else:
                    log_utils.log_info(f"  ❌ {path}: Unable to parse du output")
                    results.append(
                        {
                            "path": path,
                            "size_human": "N/A",
                            "size_bytes": 0,
                            "status": "error",
                        }
                    )
            else:
                # Permission denied or other error
                log_utils.log_info(
                    f"  ❌ {path}: Permission denied or error (exit code {result.returncode})"
                )
                results.append(
                    {
                        "path": path,
                        "size_human": "N/A",
                        "size_bytes": 0,
                        "status": "permission_denied",
                    }
                )

        except subprocess.TimeoutExpired:
            log_utils.log_info(f"  ⏱️  {path}: Timeout (>30s)")
            results.append(
                {
                    "path": path,
                    "size_human": "N/A",
                    "size_bytes": 0,
                    "status": "timeout",
                }
            )
        except Exception as e:
            log_utils.log_info(f"  ❌ {path}: Error - {e}")
            results.append(
                {
                    "path": path,
                    "size_human": "N/A",
                    "size_bytes": 0,
                    "status": "error",
                }
            )

    return results


def _format_size_human(size_bytes: int) -> str:
    """Convert bytes to human-readable format (like du -sh)."""
    for unit in ["B", "K", "M", "G", "T"]:
        if size_bytes < 1024.0:
            if unit == "B":
                return f"{int(size_bytes)}{unit}"
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}P"


def check_system_load() -> Dict[str, any]:
    """Check system load."""
    load_avg = os.getloadavg()
    cpu_count = os.cpu_count() or 1

    load_1min = load_avg[0]
    load_5min = load_avg[1]
    load_15min = load_avg[2]

    # Load at 15 minutes should not exceed CPU count
    status = "OK"
    issues = []

    if load_15min > cpu_count:
        status = "WARNING"
        issues.append(
            f"15-minute load ({load_15min:.2f}) exceeds CPU count ({cpu_count})"
        )

    if load_15min > cpu_count * 1.5:
        status = "CRITICAL"

    return {
        "load_1min": round(load_1min, 2),
        "load_5min": round(load_5min, 2),
        "load_15min": round(load_15min, 2),
        "cpu_count": cpu_count,
        "status": status,
        "issues": issues,
    }


def run_system_audit(perms: Optional[dict] = None) -> Dict[str, any]:
    """Run complete system audit."""
    if perms is None:
        perms = permissions.detect_permissions()

    cfg = config_manager.get_config()

    return {
        "system_info": get_system_info(),
        "cpu_info": get_cpu_info(),
        "memory_info": get_memory_info(),
        "network_interfaces": get_network_interfaces(),
        "docker_info": get_docker_info(),
        "docker_networks": get_docker_networks(),
        "permissions": perms,
        "systemd_services": check_systemd_services(perms),
        "docker_containers": check_docker_containers(),
        "memory_limits": check_memory_limits(),
        "swap": check_swap(),
        "firewall": check_firewall(perms),
        "disk_space": get_disk_partitions(),
        "directory_sizes": get_directory_sizes(),
        "system_load": check_system_load(),
        "access_logs": (
            access_logs.analyze_access_logs(cfg.get("access_logs", {}))
            if cfg.get("access_logs.enabled", True)
            else None
        ),
    }
