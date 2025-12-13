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

"""Access logs analysis module for nginx logs."""

import re
import subprocess
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple
from ..utils import permissions, logger as log_utils


def fetch_logs_journalctl(service_name: str, days: int, use_sudo: bool) -> List[str]:
    """Fetch logs from journalctl."""
    cmd = []
    if use_sudo:
        cmd.extend(["sudo", "-n"])
    cmd.extend(
        ["journalctl", "-u", service_name, "--since", f"{days} days ago", "--no-pager"]
    )

    log_utils.log_command(cmd, f"Fetching logs from journalctl ({service_name})")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            log_utils.log_info(f"  Retrieved {len(lines)} log lines from journalctl")
            return lines
        else:
            log_utils.log_info(
                f"  ❌ Failed to fetch journalctl logs (exit code {result.returncode})"
            )
            if result.stderr:
                log_utils.log_info(f"  Error: {result.stderr.strip()}")
            return []
    except Exception as e:
        log_utils.log_info(f"  ❌ Exception fetching journalctl logs: {e}")
        return []


def fetch_logs_docker(container_name: str, days: int, use_sudo: bool) -> List[str]:
    """Fetch logs from docker container."""
    cmd = []
    if use_sudo:
        cmd.extend(["sudo", "-n"])
    cmd.extend(["docker", "logs", container_name, "--since", f"{days}d"])

    log_utils.log_command(cmd, f"Fetching logs from docker ({container_name})")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            log_utils.log_info(f"  Retrieved {len(lines)} log lines from docker")
            return lines
        else:
            log_utils.log_info(
                f"  ❌ Failed to fetch docker logs (exit code {result.returncode})"
            )
            if result.stderr:
                log_utils.log_info(f"  Error: {result.stderr.strip()}")
            return []
    except Exception as e:
        log_utils.log_info(f"  ❌ Exception fetching docker logs: {e}")
        return []


def parse_nginx_log_line(line: str) -> Optional[Dict]:
    """
    Parse nginx combined log format.

    Handles both formats:
    - Direct: 86.246.213.139 - - [21/Nov/2025:14:39:17 +0000] "GET ..." 200 ...
    - Journalctl: Nov 21 14:39:17 hostname docker[PID]: 86.246.213.139 - - [21/Nov/2025:14:39:17 +0000] "GET ..." 200 ...
    """
    # Remove journalctl prefix if present
    # Format: Nov 21 14:39:17 hostname docker[PID]:
    journalctl_prefix_pattern = (
        r"^[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+\S+:\s+"
    )
    line = re.sub(journalctl_prefix_pattern, "", line)

    # Nginx combined log format pattern
    pattern = r'^(?P<ip>[\d\.]+) - (?P<user>\S+) \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) (?P<http_version>[^"]+)" (?P<status>\d+) (?P<size>\d+|-) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'

    match = re.match(pattern, line)
    if not match:
        return None

    try:
        timestamp_str = match.group("timestamp")
        # Parse: 21/Nov/2025:14:39:17 +0000
        timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")

        size = match.group("size")
        size_bytes = int(size) if size != "-" else 0

        return {
            "ip": match.group("ip"),
            "user": match.group("user"),
            "timestamp": timestamp,
            "method": match.group("method"),
            "url": match.group("url"),
            "http_version": match.group("http_version"),
            "status": int(match.group("status")),
            "size": size_bytes,
            "referer": match.group("referer"),
            "user_agent": match.group("user_agent"),
        }
    except (ValueError, AttributeError) as e:
        return None


def detect_os_and_browser(user_agent: str) -> Dict[str, Optional[str]]:
    """Detect OS and browser from user agent string."""
    os_type = None
    browser = None

    # Detect OS
    if "Windows NT" in user_agent:
        os_type = "Windows"
    elif "Macintosh" in user_agent or "Mac OS X" in user_agent:
        os_type = "Mac"
    elif "Android" in user_agent:
        os_type = "Android"
    elif "iPhone" in user_agent or "iPad" in user_agent:
        os_type = "iOS"
    elif "Linux" in user_agent and "Android" not in user_agent:
        os_type = "Linux"
    elif "CrOS" in user_agent:
        os_type = "Chrome OS"
    else:
        os_type = "Unknown"

    # Detect Browser (order matters - check specific ones first)
    if "Edg/" in user_agent or "Edge/" in user_agent:
        browser = "Edge"
    elif "Firefox/" in user_agent:
        browser = "Firefox"
    elif "Chrome/" in user_agent and "Edg/" not in user_agent:
        browser = "Chrome"
    elif "Safari/" in user_agent and "Chrome/" not in user_agent:
        browser = "Safari"
    elif "Opera/" in user_agent or "OPR/" in user_agent:
        browser = "Opera"
    else:
        browser = "Unknown"

    return {"os": os_type, "browser": browser}


def classify_url(method: str, url: str) -> str:
    """Classify URL by type."""
    if "/shared-links/" in url and "/content" in url:
        return "shared-link"
    elif "/renditions/doclib/content" in url:
        return "rendition-doclib"
    elif method == "POST" and "/search/versions/" in url:
        return "search"
    elif re.search(r"/nodes/[^/]+/versions/[^/]+/content", url):
        return "download"
    else:
        return "other"


def extract_site_name(referer: str) -> Optional[str]:
    """
    Extract site name from referer URL.

    Example: https://jeci.pristy.net/espaces-rc/mes-espaces/Commercial/... -> "Commercial"
    """
    if not referer or referer == "-":
        return None

    # Pattern: /mes-espaces/{SITE_NAME}/
    pattern = r"/mes-espaces/([^/]+)/"
    match = re.search(pattern, referer)
    if match:
        return match.group(1)

    return None


def calculate_requests_per_minute(timestamps: List[datetime]) -> Dict:
    """Calculate requests per minute statistics."""
    if not timestamps:
        return {"avg_per_minute": 0, "max_per_minute": 0, "peak_timestamp": None}

    # Group by minute
    minute_counts = Counter()
    for ts in timestamps:
        # Round to minute
        minute_key = ts.replace(second=0, microsecond=0)
        minute_counts[minute_key] += 1

    if not minute_counts:
        return {"avg_per_minute": 0, "max_per_minute": 0, "peak_timestamp": None}

    max_minute, max_count = minute_counts.most_common(1)[0]
    avg_count = sum(minute_counts.values()) / len(minute_counts)

    return {
        "avg_per_minute": round(avg_count, 2),
        "max_per_minute": max_count,
        "peak_timestamp": max_minute.strftime("%Y-%m-%d %H:%M"),
    }


def get_top_ips(log_entries: List[Dict], limit: int = 10) -> List[Dict]:
    """Get top N IPs by request count."""
    ip_counts = Counter(entry["ip"] for entry in log_entries)
    top_ips = []

    for ip, count in ip_counts.most_common(limit):
        top_ips.append({"ip": ip, "requests": count})

    return top_ips


def get_top_sites(log_entries: List[Dict], limit: int = 10) -> List[Dict]:
    """Get top N sites by request count."""
    site_counts = Counter()

    for entry in log_entries:
        site = extract_site_name(entry.get("referer", ""))
        if site:
            site_counts[site] += 1

    top_sites = []
    for site, count in site_counts.most_common(limit):
        top_sites.append({"site": site, "requests": count})

    return top_sites


def analyze_access_logs(config: Dict) -> Optional[Dict]:
    """
    Analyze access logs from journalctl or docker.

    Args:
        config: Configuration dictionary with:
            - source: "journalctl" or "docker"
            - service_name: for journalctl
            - container_name: for docker
            - analysis_days: number of days to analyze
            - ignore_ips: list of IPs to ignore
            - ignore_user_agents: list of user agent patterns to ignore
            - detect_robots: auto-detect robots via robots.txt access

    Returns:
        Dictionary with analysis results or None on error
    """
    source = config.get("source", "journalctl")
    days = config.get("analysis_days", 7)
    ignore_ips = set(config.get("ignore_ips", []))
    ignore_user_agents = config.get("ignore_user_agents", [])
    detect_robots = config.get("detect_robots", True)

    log_utils.log_info(f"Analyzing access logs (source: {source}, days: {days})")

    # Check permissions
    perms = permissions.detect_permissions()
    use_sudo = False

    if source == "journalctl":
        service_name = config.get("service_name", "nginx_pristy")
        use_sudo = perms.get("has_sudo", False) and not perms.get("is_root", False)
        log_lines = fetch_logs_journalctl(service_name, days, use_sudo)
        source_name = service_name
    elif source == "docker":
        container_name = config.get("container_name", "pristy-proxy")
        use_sudo = perms.get("can_use_docker", False) and not perms.get(
            "is_root", False
        )
        log_lines = fetch_logs_docker(container_name, days, use_sudo)
        source_name = container_name
    else:
        log_utils.log_info(f"  ❌ Invalid log source: {source}")
        return None

    if not log_lines:
        log_utils.log_info("  ❌ No log lines retrieved")
        return None

    # Parse log lines
    log_utils.log_info("  Parsing log lines...")
    parsed_entries = []
    parse_errors = 0

    for line in log_lines:
        entry = parse_nginx_log_line(line)
        if entry:
            parsed_entries.append(entry)
        else:
            parse_errors += 1

    log_utils.log_info(
        f"  Parsed {len(parsed_entries)} entries ({parse_errors} errors)"
    )

    if not parsed_entries:
        log_utils.log_info("  ❌ No valid log entries parsed")
        return None

    # Detect robots
    robots_ips = set()
    if detect_robots:
        for entry in parsed_entries:
            if "/robots.txt" in entry["url"]:
                robots_ips.add(entry["ip"])
        log_utils.log_info(f"  Detected {len(robots_ips)} robot IPs via robots.txt")

    # Filter entries
    filtered_entries = []
    for entry in parsed_entries:
        # Skip ignored IPs
        if entry["ip"] in ignore_ips:
            continue

        # Skip robot IPs
        if entry["ip"] in robots_ips:
            continue

        # Skip ignored user agents
        user_agent = entry["user_agent"].lower()
        if any(pattern.lower() in user_agent for pattern in ignore_user_agents):
            continue

        filtered_entries.append(entry)

    log_utils.log_info(f"  Filtered to {len(filtered_entries)} entries")

    if not filtered_entries:
        log_utils.log_info("  ❌ No entries after filtering")
        return None

    # Calculate statistics
    log_utils.log_info("  Calculating statistics...")

    # OS and Browser distribution
    os_counts = Counter()
    browser_counts = Counter()
    for entry in filtered_entries:
        detection = detect_os_and_browser(entry["user_agent"])
        os_counts[detection["os"]] += 1
        browser_counts[detection["browser"]] += 1

    # URL types
    url_type_counts = Counter()
    for entry in filtered_entries:
        url_type = classify_url(entry["method"], entry["url"])
        url_type_counts[url_type] += 1

    # Timestamps for per-minute analysis
    timestamps = [entry["timestamp"] for entry in filtered_entries]
    per_minute_stats = calculate_requests_per_minute(timestamps)

    # Calculate requests per day
    if timestamps:
        time_span = (max(timestamps) - min(timestamps)).total_seconds() / 86400  # days
        requests_per_day = int(len(filtered_entries) / max(time_span, 1))
    else:
        requests_per_day = 0

    # Top IPs and sites
    top_ips = get_top_ips(filtered_entries, limit=10)
    top_sites = get_top_sites(filtered_entries, limit=10)

    log_utils.log_info("  ✓ Analysis complete")

    return {
        "source": source,
        "source_name": source_name,
        "period_days": days,
        "total_requests": len(parsed_entries),
        "filtered_requests": len(filtered_entries),
        "requests_per_day": requests_per_day,
        "peak_requests_per_minute": per_minute_stats["max_per_minute"],
        "avg_requests_per_minute": per_minute_stats["avg_per_minute"],
        "peak_timestamp": per_minute_stats["peak_timestamp"],
        "filtered_ips_count": len(ignore_ips),
        "robots_ips_count": len(robots_ips),
        "os_distribution": dict(os_counts.most_common()),
        "browser_distribution": dict(browser_counts.most_common()),
        "url_types": dict(url_type_counts.most_common()),
        "top_ips": top_ips,
        "top_sites": top_sites if top_sites else None,
    }
