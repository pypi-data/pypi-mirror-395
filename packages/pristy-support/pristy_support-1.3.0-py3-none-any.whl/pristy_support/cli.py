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

"""CLI interface for Pristy support tool."""

import os
import sys
import click
import subprocess
import glob
from datetime import datetime
from typing import Optional
from pathlib import Path
from . import __version__
from .modules import system, logs, database, config, solr
from .exporters import markdown, html, zip_exporter
from .utils import permissions, logger
from . import config_manager


@click.group()
@click.version_option(version=__version__)
@click.option("--debug", is_flag=True, help="Enable debug mode (show all commands)")
@click.option(
    "--config", type=click.Path(exists=True), help="Path to configuration file"
)
@click.pass_context
def main(ctx, debug, config):
    """Pristy Support - Audit and support tools for Pristy ECM installations."""
    # Ensure context object exists
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug

    # Setup logging
    logger.setup_logging(debug=debug)

    # Load configuration
    if config:
        cfg = config_manager.Config(config_path=config)
    else:
        cfg = config_manager.Config()

    config_manager.set_config(cfg)
    ctx.obj["config"] = cfg

    if debug and cfg.config_path:
        logger.get_logger().debug(f"📋 Loaded config from: {cfg.config_path}")


def publish_web_report(html_path: str) -> bool:
    """
    Publish HTML report to web directory.

    - Copies report with timestamp in filename
    - Creates symlink to latest report
    - Rotates old reports (keeps N most recent)
    - Generates index.html listing all reports

    Returns True on success, False otherwise.
    """
    cfg = config_manager.get_config()

    if not cfg.get("web_publish.enabled", False):
        return False

    dest_dir = cfg.get("web_publish.destination_path", "/var/www/html/pristy-support")
    keep_reports = cfg.get("web_publish.keep_reports", 10)
    create_index = cfg.get("web_publish.create_index", True)

    logger.log_info("Publishing HTML report to web directory")
    logger.get_logger().debug(f"  Destination: {dest_dir}")
    logger.get_logger().debug(f"  Keep reports: {keep_reports}")

    # Check permissions
    perms = permissions.detect_permissions()
    use_sudo = perms.get("has_sudo", False) and not perms.get("is_root", False)

    try:
        # Create destination directory
        cmd_mkdir = []
        if use_sudo:
            cmd_mkdir.extend(["sudo", "-n"])
        cmd_mkdir.extend(["mkdir", "-p", dest_dir])

        logger.log_command(cmd_mkdir, f"Creating directory {dest_dir}")
        result = subprocess.run(cmd_mkdir, capture_output=True, text=True, check=False)
        logger.log_command_result(result.returncode, result.stdout, result.stderr)
        if result.returncode != 0:
            click.echo(f"  ⚠️  Failed to create directory {dest_dir}", err=True)
            return False

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest_filename = f"audit-{timestamp}.html"
        dest_path = os.path.join(dest_dir, dest_filename)

        # Copy file
        cmd_cp = []
        if use_sudo:
            cmd_cp.extend(["sudo", "-n"])
        cmd_cp.extend(["cp", html_path, dest_path])

        logger.log_command(cmd_cp, f"Copying report to {dest_path}")
        result = subprocess.run(cmd_cp, capture_output=True, text=True, check=False)
        logger.log_command_result(result.returncode, result.stdout, result.stderr)
        if result.returncode != 0:
            click.echo(f"  ⚠️  Failed to copy report to {dest_path}", err=True)
            return False

        # Set permissions (readable by web server)
        cmd_chmod = []
        if use_sudo:
            cmd_chmod.extend(["sudo", "-n"])
        cmd_chmod.extend(["chmod", "644", dest_path])
        logger.log_command(cmd_chmod, f"Setting permissions on {dest_path}")
        result = subprocess.run(cmd_chmod, capture_output=True, text=True, check=False)
        logger.log_command_result(result.returncode, result.stdout, result.stderr)

        click.echo(f"  ✅ Report published to: {dest_path}")

        # Create symlink to latest
        latest_path = os.path.join(dest_dir, "latest.html")
        cmd_ln = []
        if use_sudo:
            cmd_ln.extend(["sudo", "-n"])
        cmd_ln.extend(["ln", "-sf", dest_filename, latest_path])
        logger.log_command(cmd_ln, f"Creating symlink to latest report")
        result = subprocess.run(cmd_ln, capture_output=True, text=True, check=False)
        logger.log_command_result(result.returncode, result.stdout, result.stderr)

        click.echo(f"  ✅ Symlink created: {latest_path}")

        # Rotate old reports
        pattern = os.path.join(dest_dir, "audit-*.html")
        if use_sudo:
            # Use find command with sudo
            cmd_find = [
                "sudo",
                "-n",
                "find",
                dest_dir,
                "-name",
                "audit-*.html",
                "-type",
                "f",
            ]
            logger.log_command(cmd_find, f"Finding existing reports in {dest_dir}")
            result = subprocess.run(
                cmd_find, capture_output=True, text=True, check=False
            )
            logger.log_command_result(result.returncode, result.stdout, result.stderr)
            if result.returncode == 0:
                all_reports = result.stdout.strip().split("\n")
                all_reports = [r for r in all_reports if r]  # Remove empty strings
            else:
                all_reports = []
        else:
            logger.get_logger().debug(f"📄 Finding reports matching: {pattern}")
            all_reports = glob.glob(pattern)

        # Sort by filename (timestamp embedded)
        all_reports.sort(reverse=True)

        # Remove old reports
        logger.get_logger().debug(
            f"  Found {len(all_reports)} reports, keeping {keep_reports}"
        )
        if len(all_reports) > keep_reports:
            reports_to_delete = all_reports[keep_reports:]
            for report in reports_to_delete:
                cmd_rm = []
                if use_sudo:
                    cmd_rm.extend(["sudo", "-n"])
                cmd_rm.extend(["rm", "-f", report])
                logger.log_command(
                    cmd_rm, f"Removing old report: {os.path.basename(report)}"
                )
                result = subprocess.run(
                    cmd_rm, capture_output=True, text=True, check=False
                )
                logger.log_command_result(
                    result.returncode, result.stdout, result.stderr
                )

            click.echo(f"  ✅ Old reports cleaned (kept {keep_reports} most recent)")

        # Generate index.html
        if create_index:
            index_content = generate_index_html(all_reports[:keep_reports], dest_dir)
            index_path = os.path.join(dest_dir, "index.html")

            # Write to temp file first
            import tempfile

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".html"
            ) as tmp:
                tmp.write(index_content)
                tmp_path = tmp.name

            logger.log_file_write(tmp_path)

            # Copy temp file to destination with sudo if needed
            cmd_cp_index = []
            if use_sudo:
                cmd_cp_index.extend(["sudo", "-n"])
            cmd_cp_index.extend(["cp", tmp_path, index_path])
            logger.log_command(cmd_cp_index, f"Copying index to {index_path}")
            result = subprocess.run(
                cmd_cp_index, capture_output=True, text=True, check=False
            )
            logger.log_command_result(result.returncode, result.stdout, result.stderr)

            # Cleanup temp file
            os.unlink(tmp_path)

            # Set permissions
            cmd_chmod_index = []
            if use_sudo:
                cmd_chmod_index.extend(["sudo", "-n"])
            cmd_chmod_index.extend(["chmod", "644", index_path])
            logger.log_command(cmd_chmod_index, f"Setting permissions on index")
            result = subprocess.run(
                cmd_chmod_index, capture_output=True, text=True, check=False
            )
            logger.log_command_result(result.returncode, result.stdout, result.stderr)

        click.echo(f"  ℹ️  Access at: http://your-server/pristy-support/")
        click.echo(f"  ℹ️  To protect with password: see docs/WEB_PROTECTION.md")

        return True

    except Exception as e:
        logger.get_logger().error(f"Error publishing report: {e}")
        click.echo(f"  ❌ Error publishing report: {e}", err=True)
        return False


def generate_index_html(reports: list, dest_dir: str) -> str:
    """Generate index.html listing all available reports."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pristy Support - Audit Reports</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        .latest { background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #4CAF50; }
        .latest a { color: #2e7d32; font-weight: bold; font-size: 1.1em; text-decoration: none; }
        .latest a:hover { text-decoration: underline; }
        h2 { color: #555; margin-top: 30px; }
        table { border-collapse: collapse; width: 100%; margin-top: 15px; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background: #4CAF50; color: white; font-weight: bold; }
        tr:nth-child(even) { background: #f9f9f9; }
        tr:hover { background: #f5f5f5; }
        a { color: #4CAF50; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #777; font-size: 0.9em; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Pristy Support Audit Reports</h1>

        <div class="latest">
            <strong>📄 Latest Report:</strong>
            <a href="latest.html">View most recent report</a>
        </div>

        <h2>📚 Report History</h2>
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Report</th>
                </tr>
            </thead>
            <tbody>
"""

    for report_path in reports:
        filename = os.path.basename(report_path)
        # Extract timestamp from filename: audit-20250121-020530.html
        try:
            timestamp_str = filename.replace("audit-", "").replace(".html", "")
            date_part, time_part = timestamp_str.split("-")
            # Format: YYYYMMDD-HHMMSS
            date_formatted = f"{date_part[6:8]}/{date_part[4:6]}/{date_part[0:4]}"
            time_formatted = f"{time_part[0:2]}:{time_part[2:4]}:{time_part[4:6]}"
        except:
            date_formatted = "N/A"
            time_formatted = "N/A"

        html += f"""                <tr>
                    <td>{date_formatted}</td>
                    <td>{time_formatted}</td>
                    <td><a href="{filename}">📥 Download</a></td>
                </tr>
"""

    html += """            </tbody>
        </table>

        <div class="footer">
            <p>Generated by <strong>Pristy Support</strong> - Audit tool for Pristy ECM installations</p>
        </div>
    </div>
</body>
</html>
"""

    return html


@main.command()
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Output directory for reports",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
)
@click.option(
    "--formats",
    "-f",
    default="md,html,zip",
    help="Export formats (comma-separated: md, html, zip)",
)
@click.option(
    "--since",
    "-s",
    default="7d",
    help="Time period for log analysis (e.g., 24h, 7d, 30d)",
)
def audit(output_dir: str, formats: str, since: str):
    """Run complete audit of Pristy installation."""
    click.echo("🔍 Starting Pristy installation audit...\n")

    # Detect permissions
    click.echo("Detecting permissions...")
    perms = permissions.detect_permissions()
    click.echo(permissions.format_permissions_report(perms))
    click.echo()

    # Collect audit data
    audit_data = {}

    # System checks
    click.echo("Running system checks...")
    try:
        audit_data["system"] = system.run_system_audit(perms)

        # Determine overall status by checking all components
        has_error = False
        has_warning = False
        issues_found = []

        # Check memory limits
        memory_limits = audit_data["system"].get("memory_limits", {})
        mem_status = memory_limits.get("status", "UNKNOWN")
        if mem_status == "ERROR":
            has_error = True
            mem_issues = memory_limits.get("issues", [])
            for issue in mem_issues:
                issues_found.append(f"Memory: {issue}")
        elif mem_status == "WARNING":
            has_warning = True
            mem_issues = memory_limits.get("issues", [])
            for issue in mem_issues:
                issues_found.append(f"Memory: {issue}")

        # Check disk space
        disk_space = audit_data["system"].get("disk_space", [])
        for disk in disk_space:
            if disk.get("status") == "ERROR":
                has_error = True
                disk_issues = disk.get("issues", [])
                if disk_issues:
                    issues_found.append(f"Disk {disk.get('path')}: {disk_issues[0]}")
                else:
                    issues_found.append(f"Disk {disk.get('path')}: Error")
            elif disk.get("status") == "WARNING":
                has_warning = True
                free_pct = disk.get("percent_free")
                if free_pct is not None:
                    issues_found.append(
                        f"Disk {disk.get('path')}: only {free_pct}% free"
                    )
                else:
                    issues_found.append(f"Disk {disk.get('path')}: Low space")

        # Check system load
        system_load = audit_data["system"].get("system_load", {})
        if system_load.get("status") == "ERROR":
            has_error = True
            issues_found.append(f"System load: {system_load.get('load_1min')} (high)")
        elif system_load.get("status") == "WARNING":
            has_warning = True
            issues_found.append(
                f"System load: {system_load.get('load_1min')} (elevated)"
            )

        # Check firewall
        firewall = audit_data["system"].get("firewall", {})
        if firewall.get("health") == "ERROR":
            has_error = True
            issues_found.append(f"Firewall: {firewall.get('status', 'Not configured')}")
        elif firewall.get("health") == "WARNING":
            has_warning = True
            issues_found.append(f"Firewall: {firewall.get('status', 'Not detected')}")

        # Check Docker containers
        containers = audit_data["system"].get("docker_containers", [])
        unhealthy_containers = [
            c for c in containers if c.get("health") in ["ERROR", "WARNING"]
        ]
        if unhealthy_containers:
            has_warning = True
            for container in unhealthy_containers[:3]:  # Show first 3
                issues_found.append(
                    f"Container {container.get('name')}: {container.get('state')}"
                )
            if len(unhealthy_containers) > 3:
                issues_found.append(
                    f"... and {len(unhealthy_containers) - 3} more container(s) with issues"
                )

        # Determine final status
        if has_error:
            final_status = "ERROR"
        elif has_warning:
            final_status = "WARNING"
        else:
            final_status = "OK"

        click.echo(f"  System checks: {final_status}")

        # Display issues
        if issues_found:
            for issue in issues_found:
                if (
                    "ERROR" in final_status
                    or "Disk" in issue
                    or "Memory" in issue
                    or "load" in issue
                ):
                    click.echo(f"    ❌ {issue}")
                else:
                    click.echo(f"    ⚠️  {issue}")

    except Exception as e:
        click.echo(f"  System checks: ERROR")
        click.echo(f"    ❌ {str(e)}", err=True)
        audit_data["system"] = {"status": "ERROR", "error": str(e)}
    click.echo()

    # Logs analysis
    click.echo(f"Analyzing logs (last {since})...")
    try:
        audit_data["logs"] = logs.run_logs_audit(since, perms)
        status = audit_data["logs"].get("status", "UNKNOWN")
        click.echo(f"  Logs analysis: {status}")

        # Display services with errors/warnings
        services = audit_data["logs"].get("services", [])
        critical_services = []
        error_services = []
        warning_services = []

        for service in services:
            if service.get("error"):
                continue
            critical = service.get("critical_count", 0)
            errors = service.get("error_count", 0)
            warnings = service.get("warning_count", 0)

            if critical > 0:
                critical_services.append(f"{service['service']}: {critical} critical")
            elif errors > 0:
                error_services.append(f"{service['service']}: {errors} errors")
            elif warnings > 0:
                warning_services.append(f"{service['service']}: {warnings} warnings")

        # Display critical first
        for msg in critical_services[:3]:
            click.echo(f"    🔴 {msg}")
        if len(critical_services) > 3:
            click.echo(
                f"    ... and {len(critical_services) - 3} more service(s) with critical issues"
            )

        # Then errors
        for msg in error_services[:3]:
            click.echo(f"    ❌ {msg}")
        if len(error_services) > 3:
            click.echo(
                f"    ... and {len(error_services) - 3} more service(s) with errors"
            )

        # Then warnings
        for msg in warning_services[:3]:
            click.echo(f"    ⚠️  {msg}")
        if len(warning_services) > 3:
            click.echo(
                f"    ... and {len(warning_services) - 3} more service(s) with warnings"
            )

    except Exception as e:
        click.echo(f"  Logs analysis: ERROR")
        click.echo(f"    ❌ {str(e)}", err=True)
        audit_data["logs"] = {"status": "ERROR", "error": str(e)}
    click.echo()

    # Database statistics
    click.echo("Collecting database statistics...")
    try:
        audit_data["database"] = database.run_database_audit()
        status = audit_data["database"].get("status", "UNKNOWN")
        click.echo(f"  Database audit: {status}")

        # Display error if present
        if audit_data["database"].get("error"):
            click.echo(f"    ❌ {audit_data['database']['error']}")

        # Display issues if present
        issues = audit_data["database"].get("issues", [])
        for issue in issues:
            click.echo(f"    ⚠️  {issue}")

    except Exception as e:
        click.echo(f"  Database audit: ERROR")
        click.echo(f"    ❌ {str(e)}", err=True)
        audit_data["database"] = {"status": "ERROR", "error": str(e)}
    click.echo()

    # Configuration review
    click.echo("Reviewing configuration...")
    try:
        audit_data["config"] = config.run_config_audit()
        status = audit_data["config"].get("status", "UNKNOWN")
        click.echo(f"  Configuration audit: {status}")

        # Show Alfresco issues
        alfresco = audit_data["config"].get("alfresco", {})
        if alfresco.get("error"):
            click.echo(f"    ❌ Alfresco: {alfresco['error']}")
        elif alfresco.get("issues"):
            for issue in alfresco["issues"][:3]:
                click.echo(f"    ❌ Alfresco: {issue}")
            if len(alfresco["issues"]) > 3:
                click.echo(f"    ... and {len(alfresco['issues']) - 3} more issue(s)")
        elif alfresco.get("warnings"):
            for warning in alfresco["warnings"][:3]:
                click.echo(f"    ⚠️  Alfresco: {warning}")
            if len(alfresco["warnings"]) > 3:
                click.echo(
                    f"    ... and {len(alfresco['warnings']) - 3} more warning(s)"
                )

        # Show Pristy apps issues
        pristy_apps = audit_data["config"].get("pristy_apps", {})
        for app_name, app_config in pristy_apps.items():
            if app_config.get("error"):
                click.echo(f"    ❌ {app_name}: {app_config['error']}")
            elif app_config.get("warnings"):
                for warning in app_config["warnings"][:2]:
                    click.echo(f"    ⚠️  {app_name}: {warning}")
                if len(app_config["warnings"]) > 2:
                    click.echo(
                        f"    ... and {len(app_config['warnings']) - 2} more warning(s) for {app_name}"
                    )

    except Exception as e:
        click.echo(f"  Configuration audit: ERROR")
        click.echo(f"    ❌ {str(e)}", err=True)
        audit_data["config"] = {"status": "ERROR", "error": str(e)}
    click.echo()

    # Solr statistics
    click.echo("Collecting Solr statistics...")
    try:
        audit_data["solr"] = solr.run_solr_audit()
        status = audit_data["solr"].get("status", "UNKNOWN")
        click.echo(f"  Solr audit: {status}")

        # Display error if present
        if audit_data["solr"].get("error"):
            click.echo(f"    ❌ {audit_data['solr']['error']}")
        else:
            # Show summary stats
            cores = audit_data["solr"].get("cores", {})
            if "alfresco" in cores:
                alfresco_core = cores["alfresco"]
                nodes = alfresco_core.get("nodes_in_index", 0)
                lag = alfresco_core.get("tx_lag", "N/A")
                click.echo(f"    Alfresco core: {nodes:,} nodes indexed, TX lag: {lag}")

    except Exception as e:
        click.echo(f"  Solr audit: ERROR")
        click.echo(f"    ❌ {str(e)}", err=True)
        audit_data["solr"] = {"status": "ERROR", "error": str(e)}
    click.echo()

    # Export results
    click.echo("Generating reports...")
    export_formats = [f.strip().lower() for f in formats.split(",")]

    for fmt in export_formats:
        try:
            if fmt == "md" or fmt == "markdown":
                output_path = os.path.join(output_dir, "pristy_audit_report.md")
                md_content = markdown.export_to_markdown(audit_data)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                click.echo(f"  ✅ Markdown report: {output_path}")

            elif fmt == "html":
                output_path = os.path.join(output_dir, "pristy_audit_report.html")
                html_content = html.export_to_html(audit_data)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                click.echo(f"  ✅ HTML report: {output_path}")

                # Publish to web if enabled
                publish_web_report(output_path)

            elif fmt == "zip":
                base_path = os.path.join(output_dir, "pristy_audit")
                zip_path = zip_exporter.export_to_zip(audit_data, base_path)
                click.echo(f"  ✅ ZIP archive: {zip_path}")

            else:
                click.echo(f"  ⚠️  Unknown format: {fmt}", err=True)

        except Exception as e:
            click.echo(f"  ❌ Error exporting {fmt}: {str(e)}", err=True)

    click.echo("\n✨ Audit complete!")


@main.command()
def system_check():
    """Run system checks only."""
    click.echo("Running system checks...\n")

    perms = permissions.detect_permissions()
    result = system.run_system_audit(perms)

    # System info
    system_info = result.get("system_info", {})
    if system_info:
        click.echo("=== System Information ===")
        click.echo(f"Hostname: {system_info.get('hostname')}")
        click.echo(f"Operating System: {system_info.get('os_distribution')}")
        click.echo()

    # CPU info
    cpu_info = result.get("cpu_info", {})
    if cpu_info:
        click.echo(f"CPU: {cpu_info.get('count')} cores")
        click.echo(f"  Model: {cpu_info.get('model')}")
        click.echo()

    # Memory info
    memory_info = result.get("memory_info", {})
    if memory_info:
        click.echo(
            f"Memory: {memory_info.get('used_gb')}GB / {memory_info.get('total_gb')}GB ({memory_info.get('percent_used')}% used)"
        )
        if memory_info.get("swap_total_gb", 0) > 0:
            click.echo(
                f"Swap: {memory_info.get('swap_used_gb')}GB / {memory_info.get('swap_total_gb')}GB ({memory_info.get('swap_percent_used')}% used)"
            )
        click.echo()

    # Network interfaces
    network_interfaces = result.get("network_interfaces", [])
    if network_interfaces:
        click.echo("Network Interfaces:")
        for iface in network_interfaces:
            click.echo(f"  • {iface['name']}: {iface['ipv4']}")
        click.echo()

    # Docker info
    docker_info = result.get("docker_info", {})
    if docker_info and docker_info.get("available"):
        click.echo(f"Docker Version: {docker_info.get('version')}")
        if docker_info.get("daemon_config"):
            click.echo(f"  Daemon config: {docker_info.get('daemon_config_path')}")
        click.echo()

    # Print summary
    services = result.get("systemd_services", [])
    if services:
        click.echo(f"Systemd Services: {len(services)} found")
        for service in services:
            status_icon = "✅" if service["status"] == "OK" else "⚠️"
            click.echo(f"  {status_icon} {service['name']}: {service['active']}")

    click.echo()
    mem = result.get("memory_limits", {})
    if mem:
        click.echo(
            f"Memory: {mem.get('total_ram_gb')}GB RAM, {mem.get('total_swap_gb')}GB Swap"
        )
        click.echo(f"Status: {mem.get('status')}")

    click.echo()
    load = result.get("system_load", {})
    if load:
        click.echo(
            f"Load: {load.get('load_1min')} / {load.get('load_5min')} / {load.get('load_15min')}"
        )


@main.command()
@click.option(
    "--since",
    "-s",
    default="7d",
    help="Time period for log analysis (e.g., 24h, 7d, 30d)",
)
def logs_check(since: str):
    """Analyze logs only."""
    click.echo(f"Analyzing logs (last {since})...\n")

    perms = permissions.detect_permissions()
    result = logs.run_logs_audit(since, perms)

    click.echo(f"Status: {result.get('status')}\n")

    services_data = result.get("services", [])
    for service_data in services_data:
        if service_data.get("error"):
            continue

        critical = service_data.get("critical_count", 0)
        errors = service_data.get("error_count", 0)
        warnings = service_data.get("warning_count", 0)

        if critical > 0 or errors > 0 or warnings > 0:
            status_icon = "🔴" if critical > 0 else "⚠️" if errors > 0 else "ℹ️"
            click.echo(
                f"{status_icon} {service_data['service']}: "
                f"{critical} critical, {errors} errors, {warnings} warnings"
            )


@main.command()
def database_check():
    """Check database statistics only."""
    click.echo("Collecting database statistics...\n")

    result = database.run_database_audit()

    if result.get("error"):
        click.echo(f"❌ Error: {result['error']}", err=True)
        return

    stats = result.get("statistics", {})
    click.echo(f"Nodes: {stats.get('nodes', 'N/A'):,}")
    click.echo(f"Properties: {stats.get('properties', 'N/A'):,}")
    click.echo(f"Aspects: {stats.get('aspects', 'N/A'):,}")
    click.echo(f"Users: {stats.get('users', 'N/A'):,}")

    internal_users = stats.get("internal_users")
    external_users = stats.get("external_users")
    if internal_users is not None:
        click.echo(f"  Internal users (with password): {internal_users:,}")
    if external_users is not None:
        click.echo(f"  External users (SSO/LDAP): {external_users:,}")

    click.echo(f"Groups (non-site): {stats.get('groups', 'N/A'):,}")
    click.echo(f"Sites: {stats.get('sites_count', 'N/A'):,}")

    click.echo(f"\nDatabase size: {result.get('database_size', 'N/A')}")

    ratios = result.get("ratios", {})
    if ratios:
        click.echo("\nRatios:")
        click.echo(f"  Properties per node: {ratios.get('properties_per_node', 'N/A')}")
        click.echo(f"  Aspects per node: {ratios.get('aspects_per_node', 'N/A')}")

    # Display groups list
    groups_list = stats.get("groups_list", [])
    if groups_list:
        click.echo(f"\nGroups ({len(groups_list)}):")
        for group in groups_list:
            click.echo(f"  • {group}")

    # Display sites list
    sites = stats.get("sites", [])
    if sites:
        click.echo(f"\nSites ({len(sites)}):")
        for site in sites:
            click.echo(f"  • {site}")

    # Display nodes by store
    nodes_by_store = result.get("nodes_by_store", {})
    if nodes_by_store:
        click.echo(f"\nNodes by Store:")
        for store_name, count in nodes_by_store.items():
            click.echo(f"  • {store_name}: {count:,}")

    # Display top 10 node types
    nodes_by_type = result.get("nodes_by_type_top10", [])
    if nodes_by_type:
        click.echo(f"\nTop 10 Node Types:")
        for idx, item in enumerate(nodes_by_type, 1):
            click.echo(f"  {idx}. {item['type']}: {item['count']:,}")


@main.command()
def solr_check():
    """Check Solr statistics only."""
    click.echo("Collecting Solr statistics...\n")

    result = solr.run_solr_audit()

    if result.get("error"):
        click.echo(f"❌ Error: {result['error']}", err=True)
        return

    click.echo(f"Status: {result.get('status')}")
    click.echo(f"Solr IP: {result.get('solr_ip', 'N/A')}\n")

    # Display core statistics
    cores = result.get("cores", {})
    for core_name in ["alfresco", "archive"]:
        if core_name not in cores:
            continue

        core_data = cores[core_name]
        click.echo(f"=== {core_name.upper()} Core ===")
        click.echo(f"Nodes in index: {core_data.get('nodes_in_index', 'N/A'):,}")
        click.echo(
            f"Transactions in index: {core_data.get('transactions_in_index', 'N/A'):,}"
        )
        click.echo(f"ACLs in index: {core_data.get('acls_in_index', 'N/A'):,}")
        click.echo(f"Unindexed nodes: {core_data.get('unindexed_nodes', 'N/A'):,}")
        click.echo(f"Error nodes: {core_data.get('error_nodes', 'N/A'):,}")
        click.echo(f"TX Lag: {core_data.get('tx_lag', 'N/A')}")
        click.echo(f"Change Set Lag: {core_data.get('changeset_lag', 'N/A')}")
        click.echo(f"Disk size: {core_data.get('disk_size_gb', 'N/A')} GB")

        # Trackers
        trackers = core_data.get("trackers", {})
        if trackers:
            click.echo("\nTrackers:")
            click.echo(
                f"  Metadata: {'enabled' if trackers.get('metadata_enabled') else 'disabled'} "
                f"({'active' if trackers.get('metadata_active') else 'inactive'})"
            )
            click.echo(
                f"  Content: {'enabled' if trackers.get('content_enabled') else 'disabled'} "
                f"({'active' if trackers.get('content_active') else 'inactive'})"
            )
            click.echo(
                f"  ACL: {'enabled' if trackers.get('acl_enabled') else 'disabled'} "
                f"({'active' if trackers.get('acl_active') else 'inactive'})"
            )

        # Caches
        caches = core_data.get("caches", {})
        if caches:
            click.echo("\nCache Statistics:")
            for cache_name, cache_data in caches.items():
                hit_ratio = cache_data.get("cumulative_hitratio", 0.0)
                click.echo(
                    f"  {cache_name}: {hit_ratio:.2%} hit ratio "
                    f"({cache_data.get('cumulative_hits', 0):,} hits / {cache_data.get('cumulative_lookups', 0):,} lookups)"
                )

        # Handlers
        handlers = core_data.get("handlers", {})
        if handlers:
            click.echo("\nHandler Statistics:")
            for handler_name, handler_data in handlers.items():
                requests = handler_data.get("requests", 0)
                errors = handler_data.get("errors", 0)
                if requests > 0 or errors > 0:
                    click.echo(
                        f"  {handler_name}: {requests:,} requests, {errors:,} errors "
                        f"(avg: {handler_data.get('avg_time_per_request', 0):.2f}ms)"
                    )

        click.echo()

    # Display report statistics
    report = result.get("report", {})
    if report:
        click.echo("=== Synchronization Report ===")
        for core_name in ["alfresco", "archive"]:
            if core_name not in report:
                continue

            core_report = report[core_name]
            click.echo(f"\n{core_name.upper()} Core:")
            db_txs = core_report.get("db_transaction_count", 0)
            idx_txs = core_report.get("index_transaction_count", 0)
            missing_txs = core_report.get("missing_transactions", 0)
            duplicate_txs = core_report.get("duplicated_transactions", 0)

            click.echo(f"  DB transactions: {db_txs:,}")
            click.echo(f"  Index transactions: {idx_txs:,}")
            if missing_txs > 0:
                click.echo(f"  ❌ Missing transactions: {missing_txs:,}")
            if duplicate_txs > 0:
                click.echo(f"  ⚠️  Duplicate transactions: {duplicate_txs:,}")
            if missing_txs == 0 and duplicate_txs == 0:
                click.echo(f"  ✅ No synchronization issues")


@main.command()
def config_check():
    """Review configuration only."""
    click.echo("Reviewing configuration...\n")

    result = config.run_config_audit()

    # Alfresco config
    alfresco = result.get("alfresco", {})
    click.echo(f"Alfresco Configuration: {alfresco.get('status')}")
    if alfresco.get("file_path"):
        click.echo(f"  File: {alfresco['file_path']}")
        click.echo(f"  Parameters: {alfresco.get('total_parameters', 0)}")

    if alfresco.get("error"):
        click.echo(f"  ❌ Error: {alfresco['error']}")

    if alfresco.get("issues"):
        click.echo("  Issues:")
        for issue in alfresco["issues"]:
            click.echo(f"    ❌ {issue}")

    if alfresco.get("warnings"):
        click.echo("  Warnings:")
        for warning in alfresco["warnings"]:
            click.echo(f"    ⚠️  {warning}")

    if alfresco.get("missing_parameters"):
        missing = alfresco["missing_parameters"]
        if missing and len(missing) > 0:
            click.echo(f"  Missing key parameters ({len(missing)}):")
            for param in missing[:5]:  # Show first 5
                click.echo(f"    • {param}")
            if len(missing) > 5:
                click.echo(f"    ... and {len(missing) - 5} more")

    click.echo()

    # Pristy apps
    pristy_apps = result.get("pristy_apps", {})
    for app_name, app_config in pristy_apps.items():
        status = app_config.get("status")
        # Show all configs, including those not found
        click.echo(f"{app_name}: {status}")

        if app_config.get("file_path"):
            click.echo(f"  File: {app_config['file_path']}")
            click.echo(f"  Parameters: {app_config.get('total_parameters', 0)}")

        if app_config.get("error"):
            click.echo(f"  ❌ Error: {app_config['error']}")

        if app_config.get("key_parameters"):
            click.echo("  Key parameters:")
            for key, value in sorted(app_config["key_parameters"].items()):
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 60:
                    value_str = value_str[:57] + "..."
                click.echo(f"    • {key}: {value_str}")

        if app_config.get("warnings"):
            click.echo("  Warnings:")
            for warning in app_config["warnings"]:
                click.echo(f"    ⚠️  {warning}")

        if app_config.get("missing_parameters"):
            missing = app_config["missing_parameters"]
            if missing and len(missing) > 0:
                click.echo(
                    f"  Missing key parameters ({len(missing)}): {', '.join(missing)}"
                )


@main.command()
@click.option(
    "--output",
    "-o",
    default="pristy-support.yml",
    help="Output file path for the configuration file",
    type=click.Path(dir_okay=False, writable=True),
)
def init_config(output: str):
    """Generate default configuration file."""
    try:
        output_path = config_manager.Config.generate_default_config_file(output)
        click.echo(f"✅ Configuration file generated: {output_path}")
        click.echo("\nYou can now:")
        click.echo("  1. Edit the configuration file to customize settings")
        click.echo("  2. Use it with: pristy-support --config {output_path} audit")
    except Exception as e:
        click.echo(f"❌ Error generating config file: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
