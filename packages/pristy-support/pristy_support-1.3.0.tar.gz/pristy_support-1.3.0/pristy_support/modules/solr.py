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

"""Solr 6 statistics module for Pristy support tool."""

import os
import subprocess
import json
import xml.etree.ElementTree as ET
from typing import Dict, Optional
from ..utils import docker_utils, logger as log_utils
from .. import config_manager


def get_solr_secret() -> Optional[str]:
    """Read Solr secret from init_solrcore.properties file."""
    from ..utils import permissions
    import subprocess

    cfg = config_manager.get_config()
    secret_path = cfg.get(
        "solr.secret_file_path",
        "/opt/alfresco-search-services/init_solrcore.properties",
    )

    if not os.path.exists(secret_path):
        log_utils.get_logger().debug(f"Solr secret file not found: {secret_path}")
        return None

    # Try to read with sudo if available
    perms = permissions.detect_permissions()
    use_sudo = perms.get("has_sudo", False) and not perms.get("is_root", False)

    try:
        log_utils.log_file_read(secret_path)

        # Try reading with sudo first if available
        if use_sudo:
            try:
                cmd = ["sudo", "-n", "cat", secret_path]
                log_utils.log_command(cmd, f"Reading {secret_path} with sudo")
                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=False
                )
                if result.returncode == 0:
                    content = result.stdout
                else:
                    # Sudo failed, try without sudo
                    with open(secret_path, "r") as f:
                        content = f.read()
            except Exception:
                # Sudo failed, try without sudo
                with open(secret_path, "r") as f:
                    content = f.read()
        else:
            # No sudo, read directly
            with open(secret_path, "r") as f:
                content = f.read()

        # Parse the content
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("alfresco.secureComms.secret="):
                secret = line.split("=", 1)[1].strip()
                # Remove quotes if present
                secret = secret.strip('"').strip("'")
                log_utils.get_logger().debug(f"✓ Solr secret found")
                return secret

        return None

    except FileNotFoundError:
        log_utils.get_logger().debug(f"Solr secret file not found: {secret_path}")
        return None
    except Exception as e:
        log_utils.get_logger().debug(f"Error reading Solr secret: {e}")
        return None


def get_solr_container_ip(container_name: Optional[str] = None) -> Optional[str]:
    """Get IP address of Solr container via docker inspect."""
    if not docker_utils.docker_is_available():
        return None

    cfg = config_manager.get_config()
    if container_name is None:
        container_name = cfg.get("solr.container_name", "solr6")

    cmd = [
        "docker",
        "inspect",
        "-f",
        "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
        container_name,
    ]

    try:
        log_utils.log_command(cmd, f"Getting IP of container {container_name}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        log_utils.log_command_result(result.returncode, result.stdout, result.stderr)

        if result.returncode == 0 and result.stdout.strip():
            ip_address = result.stdout.strip()
            log_utils.get_logger().debug(f"✓ Solr container IP: {ip_address}")
            return ip_address
        else:
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def execute_solr_api_request(
    action: str, ip: str, secret: str, timeout: Optional[int] = None
) -> Optional[str]:
    """Execute Solr API request with authentication."""
    cfg = config_manager.get_config()
    if timeout is None:
        timeout = cfg.get("solr.timeout", 30)

    url = f"http://{ip}:8983/solr/admin/cores?wt=xml&action={action}"

    cmd = ["curl", "-s", "-H", f"X-Alfresco-Search-Secret: {secret}", url]

    try:
        log_utils.log_command(cmd, f"Executing Solr API request: {action}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

        log_utils.log_command_result(result.returncode, result.stdout, result.stderr)

        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def parse_xml_value(element, default=None):
    """Parse XML element value, handling different types."""
    if element is None:
        return default

    tag = element.tag
    text = element.text

    if tag == "long" or tag == "int":
        try:
            return int(text) if text else default
        except (ValueError, TypeError):
            return default
    elif tag == "double" or tag == "float":
        try:
            return float(text) if text else default
        except (ValueError, TypeError):
            return default
    elif tag == "bool":
        return text.lower() == "true" if text else default
    elif tag == "str":
        return text if text else default
    elif tag == "date":
        return text if text else default
    else:
        return text if text else default


def parse_lst_to_dict(lst_element) -> Dict:
    """Parse Solr <lst> element to dictionary."""
    result = {}
    if lst_element is None:
        return result

    for child in lst_element:
        name = child.get("name")
        if child.tag == "lst":
            result[name] = parse_lst_to_dict(child)
        else:
            result[name] = parse_xml_value(child)

    return result


def parse_summary_response(xml_content: str) -> Dict:
    """Parse SUMMARY XML response and extract key statistics."""
    try:
        root = ET.fromstring(xml_content)
        summary = root.find(".//lst[@name='Summary']")

        if summary is None:
            return {}

        cores = {}

        for core_element in summary.findall("lst"):
            core_name = core_element.get("name")
            if core_name not in ["alfresco", "archive"]:
                continue

            core_data = {}

            # Index statistics
            core_data["nodes_in_index"] = parse_xml_value(
                core_element.find("long[@name='Alfresco Nodes in Index']"), 0
            )
            core_data["transactions_in_index"] = parse_xml_value(
                core_element.find("long[@name='Alfresco Transactions in Index']"), 0
            )
            core_data["acls_in_index"] = parse_xml_value(
                core_element.find("long[@name='Alfresco Acls in Index']"), 0
            )
            core_data["acl_transactions_in_index"] = parse_xml_value(
                core_element.find("long[@name='Alfresco Acl Transactions in Index']"), 0
            )
            core_data["unindexed_nodes"] = parse_xml_value(
                core_element.find("long[@name='Alfresco Unindexed Nodes']"), 0
            )
            core_data["error_nodes"] = parse_xml_value(
                core_element.find("long[@name='Alfresco Error Nodes in Index']"), 0
            )

            # Lag information
            core_data["tx_lag"] = parse_xml_value(
                core_element.find("str[@name='TX Lag']"), "N/A"
            )
            core_data["changeset_lag"] = parse_xml_value(
                core_element.find("str[@name='Change Set Lag']"), "N/A"
            )

            # Disk size
            core_data["disk_size_gb"] = parse_xml_value(
                core_element.find("str[@name='On disk (GB)']"), "N/A"
            )

            # Trackers status
            core_data["trackers"] = {
                "metadata_enabled": parse_xml_value(
                    core_element.find("bool[@name='MetadataTracker Enabled']"), False
                ),
                "content_enabled": parse_xml_value(
                    core_element.find("bool[@name='ContentTracker Enabled']"), False
                ),
                "acl_enabled": parse_xml_value(
                    core_element.find("bool[@name='AclTracker Enabled']"), False
                ),
                "metadata_active": parse_xml_value(
                    core_element.find("bool[@name='MetadataTracker Active']"), False
                ),
                "content_active": parse_xml_value(
                    core_element.find("bool[@name='ContentTracker Active']"), False
                ),
                "acl_active": parse_xml_value(
                    core_element.find("bool[@name='AclTracker Active']"), False
                ),
            }

            # Searcher info
            searcher = core_element.find("lst[@name='Searcher']")
            if searcher is not None:
                core_data["searcher"] = {
                    "num_docs": parse_xml_value(
                        searcher.find("int[@name='numDocs']"), 0
                    ),
                    "max_doc": parse_xml_value(searcher.find("int[@name='maxDoc']"), 0),
                    "deleted_docs": parse_xml_value(
                        searcher.find("int[@name='deletedDocs']"), 0
                    ),
                }

            # Cache statistics
            core_data["caches"] = {}

            for cache_name in [
                "queryResultCache",
                "filterCache",
                "alfrescoPathCache",
                "alfrescoAuthorityCache",
            ]:
                cache = core_element.find(f"lst[@name='/{cache_name}']")
                if cache is not None:
                    core_data["caches"][cache_name] = {
                        "cumulative_hits": parse_xml_value(
                            cache.find("long[@name='cumulative_hits']"), 0
                        ),
                        "cumulative_lookups": parse_xml_value(
                            cache.find("long[@name='cumulative_lookups']"), 0
                        ),
                        "cumulative_hitratio": parse_xml_value(
                            cache.find("float[@name='cumulative_hitratio']"), 0.0
                        ),
                        "size": parse_xml_value(cache.find("int[@name='size']"), 0),
                        "evictions": parse_xml_value(
                            cache.find("long[@name='cumulative_evictions']"), 0
                        ),
                    }

            # Handler statistics
            core_data["handlers"] = {}

            for handler_name in ["/alfresco", "/afts", "/cmis"]:
                handler = core_element.find(f"lst[@name='{handler_name}']")
                if handler is not None:
                    core_data["handlers"][handler_name] = {
                        "requests": parse_xml_value(
                            handler.find("long[@name='requests']"), 0
                        ),
                        "errors": parse_xml_value(
                            handler.find("long[@name='errors']"), 0
                        ),
                        "server_errors": parse_xml_value(
                            handler.find("long[@name='serverErrors']"), 0
                        ),
                        "client_errors": parse_xml_value(
                            handler.find("long[@name='clientErrors']"), 0
                        ),
                        "timeouts": parse_xml_value(
                            handler.find("long[@name='timeouts']"), 0
                        ),
                        "avg_time_per_request": parse_xml_value(
                            handler.find("double[@name='avgTimePerRequest']"), 0.0
                        ),
                    }

            # FTS statistics
            fts = core_element.find("lst[@name='FTS']")
            if fts is not None:
                core_data["fts"] = {
                    "content_in_sync": parse_xml_value(
                        fts.find("long[@name='Node count whose content is in sync']"), 0
                    ),
                    "content_needs_update": parse_xml_value(
                        fts.find(
                            "long[@name='Node count whose content needs to be updated']"
                        ),
                        0,
                    ),
                }

            cores[core_name] = core_data

        return cores

    except ET.ParseError as e:
        log_utils.get_logger().debug(f"Error parsing SUMMARY XML: {e}")
        return {}
    except Exception as e:
        log_utils.get_logger().debug(f"Error processing SUMMARY data: {e}")
        return {}


def parse_report_response(xml_content: str) -> Dict:
    """Parse REPORT XML response and extract synchronization statistics."""
    try:
        root = ET.fromstring(xml_content)
        report = root.find(".//lst[@name='report']")

        if report is None:
            return {}

        cores = {}

        for core_element in report.findall("lst"):
            core_name = core_element.get("name")
            if core_name not in ["alfresco", "archive"]:
                continue

            core_data = {}

            # Tracker status
            core_data["acl_tracker"] = parse_xml_value(
                core_element.find("str[@name='ACL Tracker']"), "N/A"
            )
            core_data["metadata_tracker"] = parse_xml_value(
                core_element.find("str[@name='Metadata Tracker']"), "N/A"
            )

            # ACL statistics
            core_data["db_acl_transaction_count"] = parse_xml_value(
                core_element.find("long[@name='DB acl transaction count']"), 0
            )
            core_data["index_acl_transaction_count"] = parse_xml_value(
                core_element.find("long[@name='Index acl transaction count']"), 0
            )
            core_data["duplicated_acl_transactions"] = parse_xml_value(
                core_element.find(
                    "long[@name='Count of duplicated acl transactions in the index']"
                ),
                0,
            )
            core_data["acl_transactions_in_index_not_db"] = parse_xml_value(
                core_element.find(
                    "long[@name='Count of acl transactions in the index but not the DB']"
                ),
                0,
            )
            core_data["missing_acl_transactions"] = parse_xml_value(
                core_element.find(
                    "long[@name='Count of missing acl transactions from the Index']"
                ),
                0,
            )

            # Transaction statistics
            core_data["db_transaction_count"] = parse_xml_value(
                core_element.find("long[@name='DB transaction count']"), 0
            )
            core_data["index_transaction_count"] = parse_xml_value(
                core_element.find("long[@name='Index transaction count']"), 0
            )
            core_data["duplicated_transactions"] = parse_xml_value(
                core_element.find(
                    "long[@name='Count of duplicated transactions in the index']"
                ),
                0,
            )
            core_data["transactions_in_index_not_db"] = parse_xml_value(
                core_element.find(
                    "long[@name='Count of transactions in the index but not the DB']"
                ),
                0,
            )
            core_data["missing_transactions"] = parse_xml_value(
                core_element.find(
                    "long[@name='Count of missing transactions from the Index']"
                ),
                0,
            )

            # Node statistics
            core_data["index_node_count"] = parse_xml_value(
                core_element.find("long[@name='Index node count']"), 0
            )
            core_data["duplicate_nodes"] = parse_xml_value(
                core_element.find(
                    "long[@name='Count of duplicate nodes in the index']"
                ),
                0,
            )
            core_data["index_error_count"] = parse_xml_value(
                core_element.find("long[@name='Index error count']"), 0
            )
            core_data["index_unindexed_count"] = parse_xml_value(
                core_element.find("long[@name='Index unindexed count']"), 0
            )

            # Last indexed info
            core_data["last_indexed_tx_commit_time"] = parse_xml_value(
                core_element.find("long[@name='Last indexed transaction commit time']"),
                0,
            )
            core_data["last_indexed_tx_commit_date"] = parse_xml_value(
                core_element.find("str[@name='Last indexed transaction commit date']"),
                "N/A",
            )

            # Content synchronization
            core_data["content_in_sync"] = parse_xml_value(
                core_element.find("long[@name='Node count whose content is in sync']"),
                0,
            )
            core_data["content_needs_update"] = parse_xml_value(
                core_element.find(
                    "long[@name='Node count whose content needs to be updated']"
                ),
                0,
            )

            cores[core_name] = core_data

        return cores

    except ET.ParseError as e:
        log_utils.get_logger().debug(f"Error parsing REPORT XML: {e}")
        return {}
    except Exception as e:
        log_utils.get_logger().debug(f"Error processing REPORT data: {e}")
        return {}


def run_solr_audit() -> Dict:
    """Run complete Solr audit."""
    result = {
        "status": "OK",
        "connection_method": "api",
        "cores": {},
        "report": {},
    }

    # Get Solr secret
    secret = get_solr_secret()
    if not secret:
        return {
            "status": "ERROR",
            "error": "Unable to read Solr secret from init_solrcore.properties",
        }

    # Get Solr container IP
    ip = get_solr_container_ip()
    if not ip:
        return {"status": "ERROR", "error": "Unable to get Solr container IP address"}

    result["solr_ip"] = ip

    # Execute SUMMARY request
    summary_xml = execute_solr_api_request("SUMMARY", ip, secret)
    if summary_xml:
        result["cores"] = parse_summary_response(summary_xml)
    else:
        return {"status": "ERROR", "error": "Failed to execute SUMMARY API request"}

    # Execute REPORT request
    report_xml = execute_solr_api_request("REPORT", ip, secret)
    if report_xml:
        result["report"] = parse_report_response(report_xml)
    else:
        log_utils.get_logger().debug("Warning: Failed to execute REPORT API request")
        result["report"] = {}

    return result
