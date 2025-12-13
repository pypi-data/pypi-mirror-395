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

"""Markdown exporter for Pristy support tool."""

import re
from datetime import datetime, timezone
from typing import Dict
from tabulate import tabulate

try:
    from dateutil import parser as dateutil_parser

    HAS_DATEUTIL = True
except ImportError:
    HAS_DATEUTIL = False


def format_status_badge(status: str) -> str:
    """Format status as a markdown badge."""
    badges = {
        "OK": "✅ OK",
        "WARNING": "⚠️ WARNING",
        "ERROR": "❌ ERROR",
        "CRITICAL": "🔴 CRITICAL",
    }
    return badges.get(status, status)


def format_time_ago(created_str: str) -> str:
    """Format time elapsed since container creation."""
    if not created_str or created_str == "N/A":
        return ""

    if not HAS_DATEUTIL:
        return ""

    try:
        # Clean up the date string (remove timezone abbreviations like CEST, UTC, etc.)
        # Docker returns format like "2025-09-29 09:55:14 +0200 CEST"
        # We keep only the part before the timezone abbreviation
        cleaned_str = re.sub(r"\s+[A-Z]{3,4}$", "", created_str.strip())

        # Parse the date string
        created_date = dateutil_parser.parse(cleaned_str)

        # Make sure both dates are timezone aware
        now = datetime.now(timezone.utc)
        if created_date.tzinfo is None:
            created_date = created_date.replace(tzinfo=timezone.utc)
        else:
            created_date = created_date.astimezone(timezone.utc)

        # Calculate difference
        delta = now - created_date
        total_seconds = delta.total_seconds()

        if total_seconds < 3600:  # Less than 1 hour
            minutes = int(total_seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif total_seconds < 86400:  # Less than 1 day
            hours = int(total_seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif total_seconds < 2592000:  # Less than 30 days
            days = int(total_seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif total_seconds < 31536000:  # Less than 1 year
            months = int(total_seconds / 2592000)
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = int(total_seconds / 31536000)
            return f"{years} year{'s' if years != 1 else ''} ago"
    except Exception:
        return ""


def export_system_section(data: Dict) -> str:
    """Export system checks as markdown."""
    lines = ["## System Checks\n"]

    # System info
    system_info = data.get("system_info", {})
    if system_info:
        lines.append("### System Information")
        lines.append(f"- **Hostname**: {system_info.get('hostname', 'N/A')}")
        lines.append(
            f"- **Operating System**: {system_info.get('os_distribution', 'N/A')}"
        )
        lines.append("")

    # CPU info
    cpu_info = data.get("cpu_info", {})
    if cpu_info:
        lines.append("### CPU Information")
        lines.append(f"- **Count**: {cpu_info.get('count', 'N/A')} cores")
        lines.append(f"- **Model**: {cpu_info.get('model', 'N/A')}")
        lines.append("")

    # Memory info
    memory_info = data.get("memory_info", {})
    if memory_info:
        lines.append("### Memory Information")
        lines.append(f"- **Total RAM**: {memory_info.get('total_gb', 'N/A')}GB")
        lines.append(
            f"- **Used RAM**: {memory_info.get('used_gb', 'N/A')}GB ({memory_info.get('percent_used', 'N/A')}%)"
        )
        lines.append(f"- **Free RAM**: {memory_info.get('free_gb', 'N/A')}GB")
        if memory_info.get("swap_total_gb", 0) > 0:
            lines.append(
                f"- **Total Swap**: {memory_info.get('swap_total_gb', 'N/A')}GB"
            )
            lines.append(
                f"- **Used Swap**: {memory_info.get('swap_used_gb', 'N/A')}GB ({memory_info.get('swap_percent_used', 'N/A')}%)"
            )
        lines.append("")

    # Network interfaces
    network_interfaces = data.get("network_interfaces", [])
    if network_interfaces:
        lines.append("### Network Interfaces")
        table_data = [
            [iface["name"], iface["ipv4"], iface["ipv6"]]
            for iface in network_interfaces
        ]
        lines.append(
            tabulate(
                table_data, headers=["Interface", "IPv4", "IPv6"], tablefmt="github"
            )
        )
        lines.append("")

    # Permissions
    perms = data.get("permissions", {})
    lines.append("### Permissions")
    lines.append(f"- **Root user**: {'Yes' if perms.get('is_root') else 'No'}")
    lines.append(f"- **Sudo available**: {'Yes' if perms.get('has_sudo') else 'No'}")
    lines.append(
        f"- **Docker**: {'Available' if perms.get('can_use_docker') else 'Not available'}"
    )
    lines.append("")

    # Systemd services
    services = data.get("systemd_services", [])
    if services:
        lines.append("### Systemd Services")
        table_data = [
            [s["name"], s["enabled"], s["active"], format_status_badge(s["status"])]
            for s in services
        ]
        lines.append(
            tabulate(
                table_data,
                headers=["Service", "Enabled", "Active", "Status"],
                tablefmt="github",
            )
        )
        lines.append("")

    # Docker info
    docker_info = data.get("docker_info", {})
    if docker_info and docker_info.get("available"):
        lines.append("### Docker Information")
        lines.append(f"- **Version**: {docker_info.get('version', 'N/A')}")

        daemon_config = docker_info.get("daemon_config", {})
        if daemon_config:
            lines.append(
                f"- **Daemon Config File**: `{docker_info.get('daemon_config_path', 'N/A')}`"
            )
            lines.append("\n**Daemon Configuration:**")
            for key, value in daemon_config.items():
                lines.append(f"- `{key}`: `{value}`")
        lines.append("")

    # Docker networks
    docker_networks = data.get("docker_networks", [])
    if docker_networks:
        lines.append("### Docker Networks")
        table_data = []
        for net in docker_networks:
            subnets = ", ".join(net["subnets"]) if net["subnets"] else "N/A"
            gateways = ", ".join(net["gateways"]) if net["gateways"] else "N/A"
            table_data.append(
                [net["name"], net["driver"], net["scope"], subnets, gateways]
            )
        lines.append(
            tabulate(
                table_data,
                headers=["Network", "Driver", "Scope", "Subnets", "Gateways"],
                tablefmt="github",
            )
        )
        lines.append("")

    # Docker containers
    containers = data.get("docker_containers", [])
    if containers:
        lines.append("### Docker Containers")
        table_data = []
        for c in containers:
            created = c.get("created", "N/A")
            time_ago = format_time_ago(created)
            created_display = f"{created} ({time_ago})" if time_ago else created
            table_data.append(
                [
                    c["name"],
                    c["image"],
                    created_display,
                    c["state"],
                    format_status_badge(c["health"]),
                ]
            )
        lines.append(
            tabulate(
                table_data,
                headers=["Container", "Image", "Created", "State", "Health"],
                tablefmt="github",
            )
        )
        lines.append("")

    # Memory and swap
    mem = data.get("memory_limits", {})
    if mem:
        lines.append("### Memory Configuration")
        lines.append(f"- **Total RAM**: {mem.get('total_ram_gb')}GB")
        lines.append(f"- **Available RAM**: {mem.get('available_ram_gb')}GB")
        lines.append(f"- **Total Swap**: {mem.get('total_swap_gb')}GB")
        lines.append(f"- **Container limits sum**: {mem.get('total_limit_gb')}GB")
        lines.append(f"- **Status**: {format_status_badge(mem.get('status'))}")
        if mem.get("issues"):
            lines.append("\n**Issues:**")
            for issue in mem["issues"]:
                lines.append(f"- {issue}")
        lines.append("")

    # Disk space
    disks = data.get("disk_space", [])
    if disks:
        lines.append("### Disk Space")
        table_data = []
        for d in disks:
            table_data.append(
                [
                    d.get("source", "N/A"),
                    d.get("fstype", "N/A"),
                    d.get("target", "N/A"),
                    d.get("size", "N/A"),
                    d.get("used", "N/A"),
                    d.get("avail", "N/A"),
                    d.get("use_percent", "N/A"),
                    format_status_badge(d.get("status", "UNKNOWN")),
                ]
            )
        lines.append(
            tabulate(
                table_data,
                headers=[
                    "Device",
                    "FS Type",
                    "Mount Point",
                    "Size",
                    "Used",
                    "Avail",
                    "Use%",
                    "Status",
                ],
                tablefmt="github",
            )
        )
        lines.append("")

    # Directory sizes
    directories = data.get("directory_sizes", [])
    if directories:
        lines.append("### Directory Sizes")
        table_data = []
        for d in directories:
            status = d.get("status", "unknown")
            status_badge = (
                "✅ OK"
                if status == "ok"
                else "⚠️ N/A"
                if status == "not_found"
                else "❌ ERROR"
            )
            table_data.append(
                [
                    d["path"],
                    d.get("size_human", "N/A"),
                    status_badge,
                ]
            )
        lines.append(
            tabulate(table_data, headers=["Path", "Size", "Status"], tablefmt="github")
        )
        lines.append("")

    # System load
    load = data.get("system_load", {})
    if load:
        lines.append("### System Load")
        lines.append(f"- **1 min**: {load.get('load_1min')}")
        lines.append(f"- **5 min**: {load.get('load_5min')}")
        lines.append(f"- **15 min**: {load.get('load_15min')}")
        lines.append(f"- **CPU count**: {load.get('cpu_count')}")
        lines.append(f"- **Status**: {format_status_badge(load.get('status'))}")
        if load.get("issues"):
            for issue in load["issues"]:
                lines.append(f"- ⚠️ {issue}")
        lines.append("")

    # Firewall
    firewall = data.get("firewall", {})
    if firewall:
        lines.append("### Firewall")
        lines.append(f"- **Type**: {firewall.get('type', 'N/A')}")
        lines.append(f"- **Status**: {firewall.get('status', 'N/A')}")
        lines.append(
            f"- **Health**: {format_status_badge(firewall.get('health', 'UNKNOWN'))}"
        )
        lines.append("")

    # Access Logs Analysis
    access_logs = data.get("access_logs")
    if access_logs:
        lines.append("### Access Logs Analysis")
        lines.append(
            f"- **Source**: {access_logs.get('source')} ({access_logs.get('source_name')})"
        )
        lines.append(f"- **Period**: {access_logs.get('period_days')} days")
        lines.append(f"- **Total requests**: {access_logs.get('total_requests'):,}")
        lines.append(
            f"- **Filtered requests**: {access_logs.get('filtered_requests'):,}"
        )
        lines.append(f"- **Avg requests/day**: {access_logs.get('requests_per_day'):,}")
        lines.append(
            f"- **Avg requests/minute**: {access_logs.get('avg_requests_per_minute')}"
        )
        lines.append(
            f"- **Peak requests/minute**: {access_logs.get('peak_requests_per_minute')}"
        )
        if access_logs.get("peak_timestamp"):
            lines.append(f"- **Peak time**: {access_logs.get('peak_timestamp')}")
        lines.append(f"- **Filtered IPs**: {access_logs.get('filtered_ips_count')}")
        lines.append(f"- **Detected robots**: {access_logs.get('robots_ips_count')}")
        lines.append("")

        # OS Distribution
        os_dist = access_logs.get("os_distribution", {})
        if os_dist:
            lines.append("#### Operating Systems")
            table_data = [[os_name, count] for os_name, count in os_dist.items()]
            lines.append(
                tabulate(table_data, headers=["OS", "Requests"], tablefmt="github")
            )
            lines.append("")

        # Browser Distribution
        browser_dist = access_logs.get("browser_distribution", {})
        if browser_dist:
            lines.append("#### Browsers")
            table_data = [[browser, count] for browser, count in browser_dist.items()]
            lines.append(
                tabulate(table_data, headers=["Browser", "Requests"], tablefmt="github")
            )
            lines.append("")

        # URL Types
        url_types = access_logs.get("url_types", {})
        if url_types:
            lines.append("#### Request Types")
            table_data = [[url_type, count] for url_type, count in url_types.items()]
            lines.append(
                tabulate(table_data, headers=["Type", "Requests"], tablefmt="github")
            )
            lines.append("")

        # Top IPs
        top_ips = access_logs.get("top_ips", [])
        if top_ips:
            lines.append("#### Top 10 IP Addresses")
            table_data = [[ip["ip"], ip["requests"]] for ip in top_ips]
            lines.append(
                tabulate(
                    table_data, headers=["IP Address", "Requests"], tablefmt="github"
                )
            )
            lines.append("")

        # Top Sites
        top_sites = access_logs.get("top_sites")
        if top_sites:
            lines.append("#### Top Sites")
            table_data = [[site["site"], site["requests"]] for site in top_sites]
            lines.append(
                tabulate(table_data, headers=["Site", "Requests"], tablefmt="github")
            )
            lines.append("")

    return "\n".join(lines)


def export_logs_section(data: Dict) -> str:
    """Export logs analysis as markdown."""
    lines = ["## Logs Analysis\n"]

    status = data.get("status", "UNKNOWN")
    since = data.get("since", "N/A")
    summary = data.get("summary", {})

    lines.append(f"**Status**: {format_status_badge(status)}")
    lines.append(f"**Period**: Last {since}")
    lines.append(
        f"**Services with critical errors**: {summary.get('services_with_critical', 0)}"
    )
    lines.append(
        f"**Services with warnings**: {summary.get('services_with_warnings', 0)}"
    )
    lines.append("")

    services = data.get("services", [])
    if services:
        lines.append("### Service Log Summary")
        table_data = []
        for service in services:
            if service.get("error"):
                continue  # Skip services we couldn't query
            table_data.append(
                [
                    service["service"],
                    service.get("critical_count", 0),
                    service.get("error_count", 0),
                    service.get("warning_count", 0),
                    format_status_badge(service.get("status", "UNKNOWN")),
                ]
            )

        if table_data:
            lines.append(
                tabulate(
                    table_data,
                    headers=["Service", "Critical", "Errors", "Warnings", "Status"],
                    tablefmt="github",
                )
            )
        lines.append("")

    # Log samples for services with issues
    services_with_issues = [
        s
        for s in services
        if not s.get("error")
        and (
            s.get("critical_count", 0) > 0
            or s.get("error_count", 0) > 0
            or s.get("warning_count", 0) > 0
        )
    ]

    if services_with_issues:
        lines.append("### Log Samples\n")
        for service in services_with_issues:
            service_name = service.get("service", "Unknown")
            samples = service.get("samples", {})

            # Show critical samples
            critical_samples = samples.get("CRITICAL", [])
            if critical_samples:
                lines.append(f"#### {service_name} - Critical")
                lines.append("```")
                for sample in critical_samples[:10]:  # Limit to 10
                    lines.append(sample)
                lines.append("```\n")

            # Show error samples
            error_samples = samples.get("ERROR", [])
            if error_samples:
                lines.append(f"#### {service_name} - Errors")
                lines.append("```")
                for sample in error_samples[:10]:  # Limit to 10
                    lines.append(sample)
                lines.append("```\n")

            # Show warning samples (only if no critical/errors, or limited)
            warning_samples = samples.get("WARNING", [])
            if warning_samples and not critical_samples and not error_samples:
                lines.append(f"#### {service_name} - Warnings")
                lines.append("```")
                for sample in warning_samples[:10]:  # Limit to 10
                    lines.append(sample)
                lines.append("```\n")

    # Service log line counts
    service_log_counts = data.get("service_log_counts", {})
    if service_log_counts and service_log_counts.get("services"):
        lines.append("### Service Log Line Counts\n")
        total_lines = service_log_counts.get("total_lines", 0)
        lines.append(f"**Total log lines**: {total_lines:,}")
        lines.append("")

        table_data = []
        for svc in service_log_counts["services"]:
            table_data.append([svc["name"], f"{svc['count']:,}"])

        if table_data:
            lines.append(
                tabulate(
                    table_data,
                    headers=["Service", "Log Lines"],
                    tablefmt="github",
                )
            )
        lines.append("")

    return "\n".join(lines)


def export_database_section(data: Dict) -> str:
    """Export database statistics as markdown."""
    lines = ["## Database Statistics\n"]

    status = data.get("status", "UNKNOWN")
    lines.append(f"**Status**: {format_status_badge(status)}")
    lines.append("")

    if data.get("error"):
        lines.append(f"❌ **Error**: {data['error']}")
        return "\n".join(lines)

    stats = data.get("statistics", {})
    if stats:
        lines.append("### Node Statistics")
        nodes = stats.get("nodes")
        lines.append(
            f"- **Nodes**: {nodes:,}" if nodes is not None else "- **Nodes**: N/A"
        )
        properties = stats.get("properties")
        lines.append(
            f"- **Properties**: {properties:,}"
            if properties is not None
            else "- **Properties**: N/A"
        )
        aspects = stats.get("aspects")
        lines.append(
            f"- **Aspects**: {aspects:,}"
            if aspects is not None
            else "- **Aspects**: N/A"
        )
        content_urls = stats.get("content_urls")
        lines.append(
            f"- **Content URLs**: {content_urls:,}"
            if content_urls is not None
            else "- **Content URLs**: N/A"
        )
        content_data = stats.get("content_data")
        lines.append(
            f"- **Content Data**: {content_data:,}"
            if content_data is not None
            else "- **Content Data**: N/A"
        )
        lines.append("")

        lines.append("### User Statistics")
        users = stats.get("users")
        lines.append(
            f"- **Total Users**: {users:,}"
            if users is not None
            else "- **Total Users**: N/A"
        )

        internal_users = stats.get("internal_users")
        if internal_users is not None:
            lines.append(f"- **Internal users** (with password): {internal_users:,}")
        external_users = stats.get("external_users")
        if external_users is not None:
            lines.append(f"- **External users** (SSO/LDAP): {external_users:,}")
        lines.append("")

        # List of internal users
        internal_users_list = stats.get("internal_users_list", [])
        if internal_users_list:
            lines.append(f"**Internal users list ({len(internal_users_list)}):**")
            for user in internal_users_list[:10]:
                lines.append(f"- `{user}`")
            if len(internal_users_list) > 10:
                lines.append(f"- ... and {len(internal_users_list) - 10} more")
            lines.append("")

        lines.append("### Group and Site Statistics")
        groups = stats.get("groups")
        lines.append(
            f"- **Groups** (non-site): {groups:,}"
            if groups is not None
            else "- **Groups** (non-site): N/A"
        )
        sites_count = stats.get("sites_count")
        lines.append(
            f"- **Sites**: {sites_count:,}"
            if sites_count is not None
            else "- **Sites**: N/A"
        )
        lines.append("")

        # List of groups
        groups_list = stats.get("groups_list", [])
        if groups_list:
            lines.append("**Groups list:**")
            for group in groups_list:
                lines.append(f"- `{group}`")
            lines.append("")

        # List of sites
        sites = stats.get("sites", [])
        if sites:
            lines.append("**Sites list:**")
            for site in sites:
                lines.append(f"- `{site}`")
            lines.append("")

    db_size = data.get("database_size")
    if db_size:
        lines.append("### Storage Statistics")
        lines.append(f"- **Database Size**: {db_size}")
        lines.append("")

    ratios = data.get("ratios", {})
    if ratios:
        lines.append("### Ratios")
        lines.append(
            f"- **Properties per node**: {ratios.get('properties_per_node', 'N/A')}"
        )
        lines.append(f"- **Aspects per node**: {ratios.get('aspects_per_node', 'N/A')}")
        lines.append("")

    table_sizes = data.get("table_sizes", {})
    if table_sizes:
        lines.append("### Table Sizes")
        table_data = [[table, size] for table, size in table_sizes.items()]
        lines.append(tabulate(table_data, headers=["Table", "Size"], tablefmt="github"))
        lines.append("")

    # Nodes by store
    nodes_by_store = data.get("nodes_by_store", {})
    if nodes_by_store:
        lines.append("### Nodes by Store")
        table_data = [[store, f"{count:,}"] for store, count in nodes_by_store.items()]
        lines.append(
            tabulate(table_data, headers=["Store", "Node Count"], tablefmt="github")
        )
        lines.append("")

    # Top 10 node types
    nodes_by_type = data.get("nodes_by_type_top10", [])
    if nodes_by_type:
        lines.append("### Top 10 Node Types")
        table_data = [
            [idx, item["type"], f"{item['count']:,}"]
            for idx, item in enumerate(nodes_by_type, 1)
        ]
        lines.append(
            tabulate(
                table_data, headers=["Rank", "Node Type", "Count"], tablefmt="github"
            )
        )
        lines.append("")

    return "\n".join(lines)


def export_solr_section(data: Dict) -> str:
    """Export Solr statistics as markdown."""
    lines = ["## Solr Statistics\n"]

    status = data.get("status", "UNKNOWN")
    lines.append(f"**Status**: {format_status_badge(status)}")
    lines.append("")

    if data.get("error"):
        lines.append(f"❌ **Error**: {data['error']}")
        return "\n".join(lines)

    solr_ip = data.get("solr_ip")
    if solr_ip:
        lines.append(f"**Solr IP**: {solr_ip}")
        lines.append("")

    # Core statistics
    cores = data.get("cores", {})
    for core_name in ["alfresco", "archive"]:
        if core_name not in cores:
            continue

        core_data = cores[core_name]
        lines.append(f"### {core_name.upper()} Core")
        lines.append("")

        # Index statistics
        lines.append("**Index Statistics:**")
        nodes = core_data.get("nodes_in_index")
        lines.append(
            f"- **Nodes in index**: {nodes:,}"
            if nodes is not None
            else "- **Nodes in index**: N/A"
        )
        txs = core_data.get("transactions_in_index")
        lines.append(
            f"- **Transactions in index**: {txs:,}"
            if txs is not None
            else "- **Transactions in index**: N/A"
        )
        acls = core_data.get("acls_in_index")
        lines.append(
            f"- **ACLs in index**: {acls:,}"
            if acls is not None
            else "- **ACLs in index**: N/A"
        )
        unindexed = core_data.get("unindexed_nodes")
        lines.append(
            f"- **Unindexed nodes**: {unindexed:,}"
            if unindexed is not None
            else "- **Unindexed nodes**: N/A"
        )
        errors = core_data.get("error_nodes")
        lines.append(
            f"- **Error nodes**: {errors:,}"
            if errors is not None
            else "- **Error nodes**: N/A"
        )
        lines.append(f"- **TX Lag**: {core_data.get('tx_lag', 'N/A')}")
        lines.append(f"- **Change Set Lag**: {core_data.get('changeset_lag', 'N/A')}")
        lines.append(f"- **Disk size**: {core_data.get('disk_size_gb', 'N/A')} GB")
        lines.append("")

        # Searcher information
        searcher = core_data.get("searcher", {})
        if searcher:
            lines.append("**Searcher:**")
            lines.append(f"- **Documents**: {searcher.get('num_docs', 0):,}")
            lines.append(f"- **Max doc**: {searcher.get('max_doc', 0):,}")
            lines.append(f"- **Deleted docs**: {searcher.get('deleted_docs', 0):,}")
            lines.append("")

        # Trackers status
        trackers = core_data.get("trackers", {})
        if trackers:
            lines.append("**Trackers:**")
            lines.append("| Tracker | Enabled | Active |")
            lines.append("|---------|---------|--------|")
            lines.append(
                f"| Metadata | {'✅' if trackers.get('metadata_enabled') else '❌'} | {'✅' if trackers.get('metadata_active') else '❌'} |"
            )
            lines.append(
                f"| Content | {'✅' if trackers.get('content_enabled') else '❌'} | {'✅' if trackers.get('content_active') else '❌'} |"
            )
            lines.append(
                f"| ACL | {'✅' if trackers.get('acl_enabled') else '❌'} | {'✅' if trackers.get('acl_active') else '❌'} |"
            )
            lines.append("")

        # Cache statistics
        caches = core_data.get("caches", {})
        if caches:
            lines.append("**Cache Statistics:**")
            table_data = []
            for cache_name, cache_data in caches.items():
                hit_ratio = cache_data.get("cumulative_hitratio", 0.0)
                hits = cache_data.get("cumulative_hits", 0)
                lookups = cache_data.get("cumulative_lookups", 0)
                size = cache_data.get("size", 0)
                evictions = cache_data.get("evictions", 0)
                table_data.append(
                    [
                        cache_name,
                        f"{hit_ratio:.2%}",
                        f"{hits:,}",
                        f"{lookups:,}",
                        f"{size:,}",
                        f"{evictions:,}",
                    ]
                )
            lines.append(
                tabulate(
                    table_data,
                    headers=[
                        "Cache",
                        "Hit Ratio",
                        "Hits",
                        "Lookups",
                        "Size",
                        "Evictions",
                    ],
                    tablefmt="github",
                )
            )
            lines.append("")

        # Handler statistics
        handlers = core_data.get("handlers", {})
        if handlers:
            lines.append("**Handler Statistics:**")
            table_data = []
            for handler_name, handler_data in handlers.items():
                requests = handler_data.get("requests", 0)
                errors_count = handler_data.get("errors", 0)
                avg_time = handler_data.get("avg_time_per_request", 0.0)
                table_data.append(
                    [
                        handler_name,
                        f"{requests:,}",
                        f"{errors_count:,}",
                        f"{avg_time:.2f}ms",
                    ]
                )
            lines.append(
                tabulate(
                    table_data,
                    headers=["Handler", "Requests", "Errors", "Avg Time"],
                    tablefmt="github",
                )
            )
            lines.append("")

        # FTS statistics
        fts = core_data.get("fts", {})
        if fts:
            lines.append("**Full Text Search:**")
            lines.append(f"- **Content in sync**: {fts.get('content_in_sync', 0):,}")
            lines.append(
                f"- **Content needs update**: {fts.get('content_needs_update', 0):,}"
            )
            lines.append("")

    # Synchronization report
    report = data.get("report", {})
    if report:
        lines.append("### Synchronization Report")
        lines.append("")

        for core_name in ["alfresco", "archive"]:
            if core_name not in report:
                continue

            core_report = report[core_name]
            lines.append(f"**{core_name.upper()} Core:**")
            lines.append(
                f"- **DB transactions**: {core_report.get('db_transaction_count', 0):,}"
            )
            lines.append(
                f"- **Index transactions**: {core_report.get('index_transaction_count', 0):,}"
            )
            lines.append(
                f"- **Missing transactions**: {core_report.get('missing_transactions', 0):,}"
            )
            lines.append(
                f"- **Duplicate transactions**: {core_report.get('duplicated_transactions', 0):,}"
            )
            lines.append(
                f"- **DB ACLs**: {core_report.get('db_acl_transaction_count', 0):,}"
            )
            lines.append(
                f"- **Index ACLs**: {core_report.get('index_acl_transaction_count', 0):,}"
            )
            lines.append(
                f"- **Missing ACLs**: {core_report.get('missing_acl_transactions', 0):,}"
            )
            lines.append(
                f"- **Content in sync**: {core_report.get('content_in_sync', 0):,}"
            )
            lines.append(
                f"- **Content needs update**: {core_report.get('content_needs_update', 0):,}"
            )
            lines.append("")

    return "\n".join(lines)


def export_config_section(data: Dict) -> str:
    """Export configuration review as markdown."""
    lines = ["## Configuration Review\n"]

    status = data.get("status", "UNKNOWN")
    lines.append(f"**Status**: {format_status_badge(status)}")
    lines.append("")

    # Alfresco config
    alfresco = data.get("alfresco", {})
    if alfresco:
        lines.append("### Alfresco Configuration")
        lines.append(
            f"**Status**: {format_status_badge(alfresco.get('status', 'UNKNOWN'))}"
        )

        if alfresco.get("file_path"):
            lines.append(f"**File**: `{alfresco['file_path']}`")
            lines.append(f"**Total parameters**: {alfresco.get('total_parameters', 0)}")
            lines.append("")

            key_params = alfresco.get("key_parameters", {})
            if key_params:
                lines.append("**Key Parameters:**")
                for key, value in sorted(key_params.items()):
                    # Mask sensitive values
                    if "password" in key.lower() or "secret" in key.lower():
                        value = "***MASKED***"
                    lines.append(f"- `{key}`: {value}")
                lines.append("")

            if alfresco.get("warnings"):
                lines.append("**Warnings:**")
                for warning in alfresco["warnings"]:
                    lines.append(f"- ⚠️ {warning}")
                lines.append("")

    # Pristy apps config
    pristy_apps = data.get("pristy_apps", {})
    if pristy_apps:
        lines.append("### Pristy Applications Configuration")
        for app_name, app_config in pristy_apps.items():
            lines.append(f"\n#### {app_name}")
            lines.append(
                f"**Status**: {format_status_badge(app_config.get('status', 'UNKNOWN'))}"
            )

            if app_config.get("file_path"):
                lines.append(f"**File**: `{app_config['file_path']}`")
                lines.append(
                    f"**Total parameters**: {app_config.get('total_parameters', 0)}"
                )
                lines.append("")

                key_params = app_config.get("key_parameters", {})
                if key_params:
                    lines.append("**Key Parameters:**")
                    for key, value in sorted(key_params.items()):
                        # Mask sensitive values
                        if "password" in key.lower() or "secret" in key.lower():
                            value = "***MASKED***"
                        lines.append(f"- `{key}`: {value}")
                    lines.append("")

                if app_config.get("missing_parameters"):
                    missing = app_config["missing_parameters"]
                    if missing:
                        lines.append(
                            f"**Missing key parameters**: {', '.join(missing)}"
                        )
                        lines.append("")

            if app_config.get("warnings"):
                lines.append("**Warnings:**")
                for warning in app_config["warnings"]:
                    lines.append(f"- ⚠️ {warning}")
                lines.append("")

        lines.append("")

    return "\n".join(lines)


def export_to_markdown(audit_data: Dict) -> str:
    """Export complete audit data to markdown format."""
    from zoneinfo import ZoneInfo

    # Local time with timezone
    now_local = datetime.now().astimezone()
    timestamp_local = now_local.strftime("%Y-%m-%d %H:%M:%S %z")

    # Paris time
    now_paris = datetime.now(ZoneInfo("Europe/Paris"))
    timestamp_paris = now_paris.strftime("%H:%M:%S")

    timestamp = f"{timestamp_local} (Paris: {timestamp_paris})"

    lines = [
        "# Pristy Support Audit Report",
        "",
        f"**Generated**: {timestamp}",
        "",
        "---",
        "",
    ]

    # Export each section
    if "system" in audit_data:
        lines.append(export_system_section(audit_data["system"]))
        lines.append("---\n")

    if "logs" in audit_data:
        lines.append(export_logs_section(audit_data["logs"]))
        lines.append("---\n")

    if "database" in audit_data:
        lines.append(export_database_section(audit_data["database"]))
        lines.append("---\n")

    if "solr" in audit_data:
        lines.append(export_solr_section(audit_data["solr"]))
        lines.append("---\n")

    if "config" in audit_data:
        lines.append(export_config_section(audit_data["config"]))
        lines.append("---\n")

    return "\n".join(lines)
