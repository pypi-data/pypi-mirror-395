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

"""Configuration review module for Pristy support tool."""

import os
import json
from typing import Dict, List, Optional
from ..utils import logger as log_utils, permissions
from .. import config_manager


def read_properties_file(
    file_path: str, use_sudo: bool = False
) -> Optional[Dict[str, str]]:
    """Read Java properties file and return as dictionary."""
    if not os.path.exists(file_path):
        return None

    try:
        log_utils.log_file_read(file_path)
        properties = {}

        if use_sudo:
            # Try reading with sudo
            import subprocess

            cmd = ["sudo", "cat", file_path]
            log_utils.log_command(cmd, f"Reading file with sudo: {file_path}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            log_utils.log_command_result(result.returncode)

            if result.returncode != 0:
                return None

            content = result.stdout
            for line in content.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    properties[key.strip()] = value.strip()
        else:
            # Normal read
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith("#"):
                        continue
                    # Parse key=value
                    if "=" in line:
                        key, value = line.split("=", 1)
                        properties[key.strip()] = value.strip()

        return properties
    except (PermissionError, UnicodeDecodeError):
        return None
    except Exception:
        return None


def read_json_config(file_path: str, use_sudo: bool = False) -> Optional[Dict]:
    """Read JSON configuration file."""
    if not os.path.exists(file_path):
        return None

    try:
        log_utils.log_file_read(file_path)

        if use_sudo:
            # Try reading with sudo
            import subprocess

            cmd = ["sudo", "cat", file_path]
            log_utils.log_command(cmd, f"Reading file with sudo: {file_path}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            log_utils.log_command_result(result.returncode)

            if result.returncode != 0:
                return None

            return json.loads(result.stdout)
        else:
            # Normal read
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

    except (PermissionError, json.JSONDecodeError):
        return None
    except Exception:
        return None


def find_config_file(paths: List[str]) -> Optional[str]:
    """Find first existing config file from list of paths."""
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def analyze_alfresco_config() -> Dict[str, any]:
    """Analyze Alfresco global properties configuration."""
    cfg = config_manager.get_config()
    paths = cfg.get("config_paths.alfresco_global_properties", [])
    config_path = find_config_file(paths)

    if not config_path:
        return {
            "status": "ERROR",
            "error": "alfresco-global.properties not found",
            "file_path": None,
        }

    properties = read_properties_file(config_path)

    # If failed to read, try with sudo if available
    if properties is None:
        perms = permissions.detect_permissions()
        if perms.get("has_sudo", False):
            properties = read_properties_file(config_path, use_sudo=True)

    if properties is None:
        return {
            "status": "ERROR",
            "error": "Failed to read alfresco-global.properties (permission denied)",
            "file_path": config_path,
        }

    # Extract key parameters
    key_params = {}
    missing_params = []
    alfresco_key_params = cfg.get("config_paths.alfresco_key_params", [])

    for param in alfresco_key_params:
        if param in properties:
            key_params[param] = properties[param]
        else:
            missing_params.append(param)

    # Check for potential issues
    issues = []
    warnings = []

    # Check server mode
    server_mode = properties.get("system.serverMode", "UNKNOWN")
    if server_mode == "UNKNOWN":
        warnings.append("system.serverMode not defined")
    elif server_mode not in ["PRODUCTION", "TEST"]:
        warnings.append(f"Unusual system.serverMode: {server_mode}")

    # Check database pool
    db_pool_max = properties.get("db.pool.max")
    if db_pool_max:
        try:
            pool_max = int(db_pool_max)
            if pool_max < 40:
                warnings.append(
                    f"db.pool.max ({pool_max}) is quite low, recommended: 90"
                )
            elif pool_max > 200:
                warnings.append(f"db.pool.max ({pool_max}) is very high")
        except ValueError:
            issues.append(f"Invalid db.pool.max value: {db_pool_max}")

    # Determine status
    status = "OK"
    if issues:
        status = "ERROR"
    elif warnings:
        status = "WARNING"

    return {
        "status": status,
        "file_path": config_path,
        "key_parameters": key_params,
        "missing_parameters": missing_params,
        "total_parameters": len(properties),
        "issues": issues,
        "warnings": warnings,
    }


def analyze_pristy_app_config(app_name: str) -> Dict[str, any]:
    """Analyze Pristy Vue.js application configuration."""
    cfg = config_manager.get_config()
    pristy_apps = cfg.get("config_paths.pristy_apps", {})

    if app_name not in pristy_apps:
        return {
            "status": "ERROR",
            "error": f"Unknown app: {app_name}",
        }

    config_path = find_config_file(pristy_apps[app_name])

    if not config_path:
        return {
            "status": "ERROR",
            "error": f"{app_name} env-config.json not found",
            "file_path": None,
        }

    config = read_json_config(config_path)

    # If failed to read, try with sudo if available
    if config is None:
        perms = permissions.detect_permissions()
        if perms.get("has_sudo", False):
            config = read_json_config(config_path, use_sudo=True)

    if config is None:
        return {
            "status": "ERROR",
            "error": f"Failed to read {app_name} config (permission denied)",
            "file_path": config_path,
        }

    # Extract key parameters
    key_params = {}
    missing_params = []
    pristy_key_params_config = cfg.get("config_paths.pristy_key_params", {})
    app_key_params = pristy_key_params_config.get(app_name, [])

    for param in app_key_params:
        if param in config:
            key_params[param] = config[param]
        else:
            missing_params.append(param)

    # Check key parameters and generate warnings
    warnings = []

    # Check Alfresco host
    alfresco_host = config.get("ALFRESCO_HOST", "")
    if not alfresco_host:
        warnings.append("ALFRESCO_HOST not defined")
    elif "localhost" in alfresco_host or "127.0.0.1" in alfresco_host:
        warnings.append("ALFRESCO_HOST uses localhost (may not work in production)")

    # Check authentication
    auth = config.get("AUTH", "")
    if auth and auth not in ["basic", "oauth", "oidc", "saml"]:
        warnings.append(f"Unusual AUTH value: {auth}")

    # Determine status
    status = "OK"
    if warnings:
        status = "WARNING"

    return {
        "status": status,
        "app_name": app_name,
        "file_path": config_path,
        "key_parameters": key_params,
        "missing_parameters": missing_params,
        "total_parameters": len(config),
        "warnings": warnings,
    }


def analyze_all_pristy_configs() -> Dict[str, Dict[str, any]]:
    """Analyze all Pristy application configurations."""
    cfg = config_manager.get_config()
    pristy_apps = cfg.get("config_paths.pristy_apps", {})
    results = {}

    for app_name in pristy_apps.keys():
        results[app_name] = analyze_pristy_app_config(app_name)

    return results


def run_config_audit() -> Dict[str, any]:
    """Run complete configuration audit."""
    cfg = config_manager.get_config()
    pristy_apps = cfg.get("config_paths.pristy_apps", {})

    alfresco_config = analyze_alfresco_config()
    pristy_configs = analyze_all_pristy_configs()

    # Determine overall status
    all_statuses = [alfresco_config["status"]] + [
        config["status"] for config in pristy_configs.values()
    ]

    overall_status = "OK"
    if "ERROR" in all_statuses:
        overall_status = "ERROR"
    elif "WARNING" in all_statuses:
        overall_status = "WARNING"

    # Count found configs
    found_configs = sum(
        1
        for config in pristy_configs.values()
        if config["status"] != "ERROR" or "not found" not in config.get("error", "")
    )
    if alfresco_config["status"] != "ERROR":
        found_configs += 1

    return {
        "status": overall_status,
        "alfresco": alfresco_config,
        "pristy_apps": pristy_configs,
        "summary": {
            "total_apps_checked": len(pristy_apps) + 1,  # +1 for Alfresco
            "configs_found": found_configs,
        },
    }
