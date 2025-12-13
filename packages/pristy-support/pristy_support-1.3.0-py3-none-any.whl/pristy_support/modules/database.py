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

"""Database statistics module for Pristy support tool."""

import subprocess
import re
from typing import Dict, Optional
from ..utils import docker_utils, logger as log_utils
from .. import config_manager


def get_db_params_from_properties() -> Optional[Dict[str, str]]:
    """Extract database connection parameters from alfresco-global.properties."""
    from . import config

    # Find and read alfresco-global.properties
    cfg = config_manager.get_config()
    paths = cfg.get("config_paths.alfresco_global_properties", [])
    config_path = config.find_config_file(paths)

    if not config_path:
        return None

    properties = config.read_properties_file(config_path)
    if properties is None:
        return None

    db_params = {}

    # Parse db.url to extract host, port, database
    db_url = properties.get("db.url", "")
    if db_url:
        # Format: jdbc:postgresql://host:port/database
        match = re.search(r"postgresql://([^:]+):(\d+)/(\w+)", db_url)
        if match:
            db_params["host"] = match.group(1)
            db_params["port"] = match.group(2)
            db_params["database"] = match.group(3)

    # Get username and password
    db_params["username"] = properties.get(
        "db.username", properties.get("db.user", "alfresco")
    )
    db_params["password"] = properties.get("db.password", "")

    # Fallback to individual properties if db.url is not complete
    if "host" not in db_params:
        db_params["host"] = properties.get("db.host", "localhost")
    if "port" not in db_params:
        db_params["port"] = properties.get("db.port", "5432")
    if "database" not in db_params:
        db_params["database"] = properties.get("db.name", "alfresco")

    return db_params


def execute_postgres_query_network(
    query: str, db_params: Dict[str, str]
) -> Optional[str]:
    """Execute a PostgreSQL query via network connection."""
    cfg = config_manager.get_config()
    timeout = cfg.get("database.timeout", 60)

    # Use psql command line with connection parameters
    cmd = [
        "psql",
        "-h",
        db_params.get("host", "localhost"),
        "-p",
        db_params.get("port", "5432"),
        "-U",
        db_params.get("username", "alfresco"),
        "-d",
        db_params.get("database", "alfresco"),
        "-t",
        "-A",
        "-c",
        query,
    ]

    try:
        log_utils.log_command(cmd, f"Executing PostgreSQL query via network")

        # Set PGPASSWORD environment variable
        env = {}
        if db_params.get("password"):
            env["PGPASSWORD"] = db_params["password"]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**subprocess.os.environ, **env} if env else None,
        )

        log_utils.log_command_result(result.returncode, result.stdout, result.stderr)

        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def execute_postgres_query(
    query: str,
    container_name: Optional[str] = None,
    db_params: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """Execute a PostgreSQL query via docker exec or network."""
    cfg = config_manager.get_config()

    # If db_params provided, use network connection
    if db_params:
        return execute_postgres_query_network(query, db_params)

    # Otherwise try docker exec
    if not docker_utils.docker_is_available():
        return None

    if container_name is None:
        container_name = cfg.get("database.container_name", "postgres")
    user = cfg.get("database.user", "alfresco")
    database = cfg.get("database.database", "alfresco")
    timeout = cfg.get("database.timeout", 60)

    # Use psql with -t (tuples only) and -A (unaligned) for easier parsing
    command = [
        "psql",
        "-U",
        user,
        "-d",
        database,
        "-t",
        "-A",
        "-c",
        query,
    ]

    result = docker_utils.docker_exec(container_name, command, timeout=timeout)
    return result


def get_node_count(db_params: Optional[Dict[str, str]] = None) -> Optional[int]:
    """Get total number of nodes in Alfresco."""
    result = execute_postgres_query(
        "SELECT COUNT(*) FROM alf_node;", db_params=db_params
    )
    if result:
        try:
            return int(result.strip())
        except ValueError:
            return None
    return None


def get_property_count(db_params: Optional[Dict[str, str]] = None) -> Optional[int]:
    """Get total number of node properties."""
    result = execute_postgres_query(
        "SELECT COUNT(*) FROM alf_node_properties;", db_params=db_params
    )
    if result:
        try:
            return int(result.strip())
        except ValueError:
            return None
    return None


def get_aspect_count(db_params: Optional[Dict[str, str]] = None) -> Optional[int]:
    """Get total number of aspects applied to nodes."""
    result = execute_postgres_query(
        "SELECT COUNT(*) FROM alf_node_aspects;", db_params=db_params
    )
    if result:
        try:
            return int(result.strip())
        except ValueError:
            return None
    return None


def get_user_and_group_count(
    db_params: Optional[Dict[str, str]] = None,
) -> Dict[str, any]:
    """Get count of users, groups, and sites."""
    # Query for non-site groups (authorities starting with 'GROUP_' but not 'GROUP_site_')
    groups_result = execute_postgres_query(
        "SELECT COUNT(*) FROM alf_authority WHERE authority LIKE 'GROUP_%' AND authority NOT LIKE 'GROUP_site_%';",
        db_params=db_params,
    )
    groups = None
    if groups_result:
        try:
            groups = int(groups_result.strip())
        except ValueError:
            pass

    # Get list of non-site groups
    groups_list_result = execute_postgres_query(
        "SELECT authority FROM alf_authority WHERE authority LIKE 'GROUP_%' AND authority NOT LIKE 'GROUP_site_%' ORDER BY authority;",
        db_params=db_params,
    )
    groups_list = []
    if groups_list_result:
        groups_list = [
            line.strip()
            for line in groups_list_result.strip().split("\n")
            if line.strip()
        ]

    # Query for total users (authorities NOT starting with 'GROUP_')
    users_result = execute_postgres_query(
        "SELECT * FROM alf_authority WHERE authority NOT LIKE 'GROUP_%' AND authority NOT LIKE 'ROLE_%' AND authority != 'guest';",
        db_params=db_params,
    )
    users = None
    if users_result:
        try:
            users = int(users_result.strip())
        except ValueError:
            pass

    # Query for internal users (with password)
    internal_users_query = """
        SELECT COUNT(*)
        FROM alf_node n
        JOIN alf_node_properties up ON n.id = up.node_id AND up.qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'username' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        LEFT JOIN alf_node_properties pa ON n.id = pa.node_id AND pa.qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'password' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        LEFT JOIN alf_node_properties pah ON n.id = pah.node_id AND pah.qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'passwordHash' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        WHERE n.type_qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'user' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        AND (
            ( pa.string_value IS NOT NULL AND pa.string_value != '' )
            OR
            ( pah.string_value IS NOT NULL AND pah.string_value != '' )
        );
    """
    internal_users_result = execute_postgres_query(
        internal_users_query, db_params=db_params
    )
    internal_users = None
    if internal_users_result:
        try:
            internal_users = int(internal_users_result.strip())
        except ValueError:
            pass

    # Calculate external users (total - internal)
    external_users = None
    if users is not None and internal_users is not None:
        external_users = users - internal_users

    # Query for internal users list (with username)
    internal_users_list_query = """
        SELECT up.string_value AS username
        FROM alf_node n
        JOIN alf_node_properties up ON n.id = up.node_id AND up.qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'username' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        LEFT JOIN alf_node_properties pa ON n.id = pa.node_id AND pa.qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'password' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        LEFT JOIN alf_node_properties pah ON n.id = pah.node_id AND pah.qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'passwordHash' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        WHERE n.type_qname_id = (
            SELECT id FROM alf_qname WHERE local_name = 'user' AND ns_id = (SELECT id FROM alf_namespace WHERE uri = 'http://www.alfresco.org/model/user/1.0')
        )
        AND (
            ( pa.string_value IS NOT NULL AND pa.string_value != '' )
            OR
            ( pah.string_value IS NOT NULL AND pah.string_value != '' )
        );
    """
    internal_users_list_result = execute_postgres_query(
        internal_users_list_query, db_params=db_params
    )
    internal_users_list = []
    if internal_users_list_result:
        internal_users_list = [
            line.strip()
            for line in internal_users_list_result.strip().split("\n")
            if line.strip()
        ]

    # Query for site groups to extract site names
    sites_result = execute_postgres_query(
        "SELECT DISTINCT authority FROM alf_authority WHERE authority LIKE 'GROUP_site_%' ORDER BY authority;",
        db_params=db_params,
    )
    sites = []
    if sites_result:
        # Extract unique site names from GROUP_site_{sitename}_Site{Role}
        site_names_set = set()
        for line in sites_result.strip().split("\n"):
            line = line.strip()
            if line:
                # Extract site name using regex: GROUP_site_{name}_Site
                match = re.search(r"GROUP_site_(.+?)_Site", line)
                if match:
                    site_names_set.add(match.group(1))
        sites = sorted(list(site_names_set))

    return {
        "users": users,
        "internal_users": internal_users,
        "internal_users_list": internal_users_list,
        "external_users": external_users,
        "groups": groups,
        "groups_list": groups_list,
        "sites": sites,
        "sites_count": len(sites),
    }


def get_database_size(db_params: Optional[Dict[str, str]] = None) -> Optional[str]:
    """Get total database size."""
    result = execute_postgres_query(
        "SELECT pg_size_pretty(pg_database_size('alfresco'));", db_params=db_params
    )
    if result:
        return result.strip()
    return None


def get_table_sizes(db_params: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Get sizes of main Alfresco tables."""
    tables = [
        "alf_node",
        "alf_node_properties",
        "alf_node_aspects",
        "alf_authority",
        "alf_content_data",
        "alf_content_url",
    ]

    table_sizes = {}
    for table in tables:
        result = execute_postgres_query(
            f"SELECT pg_size_pretty(pg_total_relation_size('{table}'));",
            db_params=db_params,
        )
        if result:
            table_sizes[table] = result.strip()
        else:
            table_sizes[table] = "Unknown"

    return table_sizes


def get_content_statistics(
    db_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Optional[int]]:
    """Get content-related statistics."""
    # Count of content URLs
    content_urls_result = execute_postgres_query(
        "SELECT COUNT(*) FROM alf_content_url;", db_params=db_params
    )
    content_urls = None
    if content_urls_result:
        try:
            content_urls = int(content_urls_result.strip())
        except ValueError:
            pass

    # Count of content data entries
    content_data_result = execute_postgres_query(
        "SELECT COUNT(*) FROM alf_content_data;", db_params=db_params
    )
    content_data = None
    if content_data_result:
        try:
            content_data = int(content_data_result.strip())
        except ValueError:
            pass

    return {
        "content_urls": content_urls,
        "content_data": content_data,
    }


def get_nodes_by_store(db_params: Optional[Dict[str, str]] = None) -> Dict[str, int]:
    """Get count of nodes per store."""
    query = """
        SELECT
            s.protocol || '://' || s.identifier AS store_name,
            COUNT(n.id) AS node_count
        FROM alf_store s
        LEFT JOIN alf_node n ON s.id = n.store_id
        GROUP BY s.protocol, s.identifier
        ORDER BY node_count DESC;
    """
    result = execute_postgres_query(query, db_params=db_params)

    nodes_by_store = {}
    if result:
        for line in result.strip().split("\n"):
            line = line.strip()
            if line and "|" in line:
                parts = line.split("|")
                if len(parts) == 2:
                    store_name = parts[0].strip()
                    try:
                        count = int(parts[1].strip())
                        nodes_by_store[store_name] = count
                    except ValueError:
                        pass

    return nodes_by_store


def get_nodes_by_type_top10(db_params: Optional[Dict[str, str]] = None) -> list:
    """Get top 10 node types by count."""
    query = """
        SELECT
            ns.uri || '/' || q.local_name AS node_type,
            COUNT(n.id) AS node_count
        FROM alf_node n
        JOIN alf_qname q ON n.type_qname_id = q.id
        JOIN alf_namespace ns ON q.ns_id = ns.id
        GROUP BY ns.uri, q.local_name
        ORDER BY node_count DESC
        LIMIT 10;
    """
    result = execute_postgres_query(query, db_params=db_params)

    nodes_by_type = []
    if result:
        for line in result.strip().split("\n"):
            line = line.strip()
            if line and "|" in line:
                parts = line.split("|")
                if len(parts) == 2:
                    node_type = parts[0].strip()
                    try:
                        count = int(parts[1].strip())
                        nodes_by_type.append({"type": node_type, "count": count})
                    except ValueError:
                        pass

    return nodes_by_type


def calculate_ratios(stats: Dict[str, any]) -> Dict[str, Optional[float]]:
    """Calculate useful ratios from statistics."""
    ratios = {}

    nodes = stats.get("nodes")
    properties = stats.get("properties")
    aspects = stats.get("aspects")

    if nodes and nodes > 0:
        if properties is not None:
            ratios["properties_per_node"] = round(properties / nodes, 2)
        if aspects is not None:
            ratios["aspects_per_node"] = round(aspects / nodes, 2)

    return ratios


def run_database_audit() -> Dict[str, any]:
    """Run complete database audit."""
    db_params = None
    connection_method = "docker"

    # Try Docker first
    if docker_utils.docker_is_available():
        # Check if postgres container exists
        containers = docker_utils.docker_ps(all_containers=True)
        postgres_container = None
        for container in containers:
            if "postgres" in container["name"]:
                postgres_container = container
                break

        if postgres_container and "Up" in postgres_container["status"]:
            # Use Docker connection
            connection_method = "docker"
        else:
            # No container or not running, try network connection
            db_params = get_db_params_from_properties()
            if db_params:
                connection_method = "network"
            else:
                return {
                    "status": "ERROR",
                    "error": "PostgreSQL container not found and unable to get database connection parameters from alfresco-global.properties",
                }
    else:
        # Docker not available, try network connection
        db_params = get_db_params_from_properties()
        if db_params:
            connection_method = "network"
        else:
            return {
                "status": "ERROR",
                "error": "Docker not available and unable to get database connection parameters from alfresco-global.properties",
            }

    # Gather statistics
    nodes = get_node_count(db_params)
    properties = get_property_count(db_params)
    aspects = get_aspect_count(db_params)
    users_groups = get_user_and_group_count(db_params)
    db_size = get_database_size(db_params)
    table_sizes = get_table_sizes(db_params)
    content_stats = get_content_statistics(db_params)
    nodes_by_store = get_nodes_by_store(db_params)
    nodes_by_type = get_nodes_by_type_top10(db_params)

    stats = {
        "nodes": nodes,
        "properties": properties,
        "aspects": aspects,
        "users": users_groups.get("users"),
        "groups": users_groups.get("groups"),
    }

    ratios = calculate_ratios(stats)

    # Determine status
    status = "OK"
    issues = []

    if nodes is None:
        status = "ERROR"
        issues.append("Failed to query node count")
    elif nodes == 0:
        status = "WARNING"
        issues.append("No nodes found in database (empty repository)")

    result = {
        "status": status,
        "issues": issues,
        "connection_method": connection_method,
        "statistics": {
            "nodes": nodes,
            "properties": properties,
            "aspects": aspects,
            "users": users_groups.get("users"),
            "internal_users": users_groups.get("internal_users"),
            "internal_users_list": users_groups.get("internal_users_list", []),
            "external_users": users_groups.get("external_users"),
            "groups": users_groups.get("groups"),
            "groups_list": users_groups.get("groups_list", []),
            "sites": users_groups.get("sites", []),
            "sites_count": users_groups.get("sites_count", 0),
            "content_urls": content_stats.get("content_urls"),
            "content_data": content_stats.get("content_data"),
        },
        "ratios": ratios,
        "database_size": db_size,
        "table_sizes": table_sizes,
        "nodes_by_store": nodes_by_store,
        "nodes_by_type_top10": nodes_by_type,
    }

    # Add connection info if using network
    if connection_method == "network" and db_params:
        result["connection_info"] = {
            "host": db_params.get("host"),
            "port": db_params.get("port"),
            "database": db_params.get("database"),
            "username": db_params.get("username"),
        }

    return result
