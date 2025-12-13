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

"""Log analysis module for Pristy support tool."""

import re
import subprocess
from typing import List, Dict, Optional
from collections import Counter
from ..utils import permissions, logger as log_utils
from .. import config_manager


def get_severity_patterns() -> Dict[str, re.Pattern]:
    """Get severity patterns from configuration."""
    cfg = config_manager.get_config()
    keywords = cfg.get(
        "logs.severity_keywords",
        {
            "critical": ["CRITICAL", "FATAL"],
            "error": ["ERROR"],
            "warning": ["WARN", "WARNING"],
        },
    )

    return {
        "CRITICAL": re.compile(
            r"\b(" + "|".join(keywords.get("critical", [])) + r")\b", re.IGNORECASE
        ),
        "ERROR": re.compile(
            r"\b(" + "|".join(keywords.get("error", [])) + r")\b", re.IGNORECASE
        ),
        "WARNING": re.compile(
            r"\b(" + "|".join(keywords.get("warning", [])) + r")\b", re.IGNORECASE
        ),
    }


def get_journalctl_logs(
    service: str, since: str = "7d", cmd_prefix: Optional[List[str]] = None
) -> Optional[str]:
    """Get logs from journalctl for a specific service."""
    if cmd_prefix is None:
        cmd_prefix = []

    # Add '-' prefix if not already present
    since_value = since if since.startswith("-") else f"-{since}"

    try:
        cmd = cmd_prefix + [
            "journalctl",
            "-eu",
            service,
            "--since",
            since_value,
            "--no-pager",
        ]

        log_utils.log_command(cmd, f"Retrieving logs for service '{service}'")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        log_utils.log_command_result(result.returncode)

        if result.returncode == 0:
            return result.stdout
        else:
            return None

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def analyze_log_content(log_content: str) -> Dict[str, any]:
    """Analyze log content and count severities."""
    if not log_content:
        return {
            "total_lines": 0,
            "critical_count": 0,
            "error_count": 0,
            "warning_count": 0,
            "samples": {},
        }

    cfg = config_manager.get_config()
    max_samples = cfg.get("logs.max_samples_per_severity", 10)
    severity_patterns = get_severity_patterns()
    lines = log_content.strip().split("\n")
    total_lines = len(lines)

    severity_counts = {
        "CRITICAL": 0,
        "ERROR": 0,
        "WARNING": 0,
    }

    severity_samples = {
        "CRITICAL": [],
        "ERROR": [],
        "WARNING": [],
    }

    # Analyze each line
    for line in lines:
        for severity, pattern in severity_patterns.items():
            if pattern.search(line):
                severity_counts[severity] += 1
                # Keep only last N samples per severity (most recent)
                if len(severity_samples[severity]) < max_samples:
                    severity_samples[severity].append(
                        line[:500]
                    )  # Truncate very long lines
                break  # Count each line only once (highest severity)

    return {
        "total_lines": total_lines,
        "critical_count": severity_counts["CRITICAL"],
        "error_count": severity_counts["ERROR"],
        "warning_count": severity_counts["WARNING"],
        "samples": severity_samples,
    }


def extract_error_patterns(
    log_content: str, max_patterns: int = 10
) -> List[Dict[str, any]]:
    """Extract and count common error patterns from logs."""
    if not log_content:
        return []

    severity_patterns = get_severity_patterns()
    error_messages = []
    lines = log_content.strip().split("\n")

    for line in lines:
        # Look for lines with ERROR or WARN
        if severity_patterns["ERROR"].search(line) or severity_patterns[
            "WARNING"
        ].search(line):
            # Try to extract the meaningful part (after timestamp and log level)
            # This is a simple heuristic
            parts = line.split("]", 1)
            if len(parts) > 1:
                message = parts[1].strip()
            else:
                message = line

            # Truncate and normalize
            message = message[:150]
            error_messages.append(message)

    # Count occurrences
    counter = Counter(error_messages)
    most_common = counter.most_common(max_patterns)

    return [
        {
            "message": msg,
            "count": count,
        }
        for msg, count in most_common
    ]


def analyze_service_logs(
    service: str, since: str = "7d", perms: Optional[dict] = None
) -> Dict[str, any]:
    """Analyze logs for a specific service."""
    if perms is None:
        perms = permissions.detect_permissions()

    if not perms["can_use_journalctl"]:
        return {
            "service": service,
            "status": "ERROR",
            "error": "journalctl not available",
        }

    log_content = get_journalctl_logs(service, since, perms["command_prefix"])

    if log_content is None:
        return {
            "service": service,
            "status": "ERROR",
            "error": "Failed to retrieve logs (service may not exist)",
        }

    analysis = analyze_log_content(log_content)
    patterns = extract_error_patterns(log_content)

    # Determine status based on severity counts
    status = "OK"
    if analysis["critical_count"] > 0:
        status = "CRITICAL"
    elif analysis["error_count"] > 10:  # More than 10 errors is concerning
        status = "WARNING"
    elif analysis["warning_count"] > 50:  # Many warnings
        status = "WARNING"

    return {
        "service": service,
        "since": since,
        "status": status,
        "total_lines": analysis["total_lines"],
        "critical_count": analysis["critical_count"],
        "error_count": analysis["error_count"],
        "warning_count": analysis["warning_count"],
        "samples": analysis["samples"],
        "common_patterns": patterns,
    }


def get_service_log_counts(
    since: str = "7d", cmd_prefix: Optional[List[str]] = None
) -> Dict[str, any]:
    """Count log lines per systemd service using journalctl.

    This function queries journalctl for all service units and counts the number
    of log lines per service. This is useful for identifying services that generate
    the most log volume.

    Args:
        since: Time period to analyze (e.g., "7d", "24h", "30d")
        cmd_prefix: Command prefix (e.g., ["sudo"]) for elevated permissions

    Returns:
        Dict containing:
            - status: "OK", "WARNING", or "ERROR"
            - total_lines: Total number of log lines processed
            - services: List of dicts with "name" and "count" sorted by count desc
            - error: Error message if status is "ERROR"
    """
    if cmd_prefix is None:
        cmd_prefix = []

    # Add '-' prefix if not already present
    since_value = since if since.startswith("-") else f"-{since}"

    try:
        cmd = cmd_prefix + [
            "journalctl",
            "--since",
            since_value,
            "--output=cat",
            "--output-fields=_SYSTEMD_UNIT",
            "--no-pager",
        ]

        log_utils.log_command(cmd, "Counting log lines per service")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes timeout for large time ranges
        )
        log_utils.log_command_result(result.returncode)

        if result.returncode != 0:
            return {
                "status": "ERROR",
                "error": f"journalctl failed: {result.stderr}",
                "services": [],
                "total_lines": 0,
            }

        # Parse output and count services
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        service_counter = Counter()

        for line in lines:
            line = line.strip()
            # Filter for .service entries only
            if line.endswith(".service"):
                service_counter[line] += 1

        # Sort by count descending
        sorted_services = [
            {"name": name, "count": count}
            for name, count in service_counter.most_common()
        ]

        total_lines = sum(s["count"] for s in sorted_services)

        return {
            "status": "OK",
            "total_lines": total_lines,
            "services": sorted_services,
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "ERROR",
            "error": "Command timed out after 5 minutes",
            "services": [],
            "total_lines": 0,
        }
    except FileNotFoundError:
        return {
            "status": "ERROR",
            "error": "journalctl not found",
            "services": [],
            "total_lines": 0,
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "services": [],
            "total_lines": 0,
        }


def run_logs_audit(since: str = "7d", perms: Optional[dict] = None) -> Dict[str, any]:
    """Run logs analysis for all Pristy services."""
    if perms is None:
        perms = permissions.detect_permissions()

    if not perms["can_use_journalctl"]:
        return {
            "status": "ERROR",
            "error": "journalctl not available or accessible",
            "services": [],
        }

    cfg = config_manager.get_config()
    services = cfg.get("logs.services", [])
    results = []

    for service in services:
        analysis = analyze_service_logs(service, since, perms)
        results.append(analysis)

    # Compute overall status
    overall_status = "OK"
    critical_count = sum(1 for r in results if r.get("status") == "CRITICAL")
    warning_count = sum(1 for r in results if r.get("status") == "WARNING")

    if critical_count > 0:
        overall_status = "CRITICAL"
    elif warning_count > 0:
        overall_status = "WARNING"

    # Get service log line counts
    service_log_counts = get_service_log_counts(since, perms["command_prefix"])

    return {
        "status": overall_status,
        "since": since,
        "services": results,
        "summary": {
            "total_services": len(results),
            "services_with_critical": critical_count,
            "services_with_warnings": warning_count,
        },
        "service_log_counts": service_log_counts,
    }
