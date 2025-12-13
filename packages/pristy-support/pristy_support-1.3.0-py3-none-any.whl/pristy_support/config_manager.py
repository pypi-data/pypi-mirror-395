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

"""Configuration management for Pristy support tool."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


# Default configuration
DEFAULT_CONFIG = {
    "system": {
        "services": [
            "postgres",
            "kafka",
            "alfresco",
            "share",
            "pristy",
            "solr6",
            "pristy-kafka-ocr",
            "pristy-portail",
            "pristy-espaces",
            "pristy-actes",
            "pristy-marches",
            "pristy-social",
            "nginx_pristy",
            "collabora",
        ],
        "memory": {
            "min_ram_gb": 8,
            "recommended_ram_gb": 12,
            "min_swap_gb": 2,
        },
        "disk_thresholds": {
            "/": 10,
            "/var/lib/docker": 30,
            "/data/alf_data": 30,
            "/data/pgsql": 30,
            "/data/solr": 30,
            "/var/log": 10,
        },
        "directory_paths": [
            "/data/alf_data",
            "/opt/alfresco",
            "/var/lib/docker",
            "/data/pgsql",
            "/data/solr",
            "/var/log",
        ],
        "filesystem_types": ["ext4", "xfs", "btrfs", "ext3", "f2fs"],
    },
    "docker": {
        "container_patterns": [
            "postgres",
            "kafka",
            "alfresco",
            "share",
            "solr6",
            "pristy-portail",
            "pristy-espaces",
            "pristy-actes",
            "pristy-marches",
            "pristy-social",
            "nginx_pristy",
            "collabora",
            "transform-core-aio",
            "pristy-kafka-ocr",
        ],
    },
    "logs": {
        "services": [
            "alfresco",
            "solr6",
            "postgres",
            "nginx_pristy",
            "kafka",
            "share",
            "pristy-portail",
            "pristy-espaces",
            "pristy-actes",
            "pristy-marches",
            "pristy-social",
            "pristy-kafka-ocr",
            "collabora",
        ],
        "default_since": "7d",
        "max_samples_per_severity": 10,
        "severity_keywords": {
            "critical": ["CRITICAL", "FATAL"],
            "error": ["ERROR"],
            "warning": ["WARN", "WARNING"],
        },
    },
    "access_logs": {
        "enabled": True,
        "source": "journalctl",  # "journalctl" or "docker"
        "service_name": "nginx_pristy",
        "container_name": "pristy-proxy",
        "analysis_days": 7,
        "ignore_ips": [],
        "ignore_user_agents": [
            "bot",
            "crawler",
            "spider",
            "Googlebot",
            "Bingbot",
            "YandexBot",
            "baiduspider",
        ],
        "detect_robots": True,
    },
    "web_publish": {
        "enabled": False,
        "destination_path": "/var/www/html/pristy-support",
        "keep_reports": 10,
        "create_index": True,
    },
    "database": {
        "container_name": "postgres",
        "user": "alfresco",
        "database": "alfresco",
        "timeout": 60,
    },
    "solr": {
        "container_name": "solr6",
        "secret_file_path": "/opt/alfresco-search-services/init_solrcore.properties",
        "timeout": 30,
    },
    "config_paths": {
        "alfresco_global_properties": [
            "/opt/alfresco/tomcat/shared/classes/alfresco-global.properties",
        ],
        "pristy_apps": {
            "pristy-portail": [
                "/opt/pristy/env-config-pristy-portail.json",
            ],
            "pristy-espaces": [
                "/opt/pristy/env-config-pristy-espaces.json",
            ],
            "pristy-actes": [
                "/opt/pristy/env-config-pristy-actes.json",
            ],
            "pristy-marches": [
                "/opt/pristy/env-config-pristy-marches.json",
            ],
            "pristy-social": [
                "/opt/pristy/env-config-pristy-social.json",
            ],
        },
        "alfresco_key_params": [
            "db.pool.max",
            "db.pool.validate.query",
            "alfresco.context",
            "alfresco.host",
            "alfresco.port",
            "alfresco.protocol",
            "share.context",
            "share.host",
            "share.port",
            "share.protocol",
            "solr.host",
            "solr.port",
            "solr.sharedSecret",
            "index.subsystem.name",
            "dir.contentstore",
            "dir.root",
        ],
        "pristy_key_params": {
            "pristy-portail": [
                "APP_ROOT",
                "BREADCRUMB_ROOT_URL",
                "ALFRESCO_HOST",
                "ALFRESCO_AUTH",
                "ALFRESCO_ROOT",
                "PREVIEW_URL",
                "AUTH",
            ],
            "pristy-espaces": [
                "APP_ROOT",
                "ALFRESCO_HOST",
                "ALFRESCO_AUTH",
                "ALFRESCO_ROOT",
                "PREVIEW_URL",
                "COLLABORA_HOSTING_DISCOVERY",
                "AUTH",
            ],
            "pristy-actes": [
                "APP_ROOT",
                "BREADCRUMB_ROOT_URL",
                "ALFRESCO_HOST",
                "ALFRESCO_AUTH",
                "ALFRESCO_ROOT",
                "PREVIEW_URL",
                "AUTH",
            ],
            "pristy-marches": [
                "APP_ROOT",
                "BREADCRUMB_ROOT_URL",
                "ALFRESCO_HOST",
                "ALFRESCO_AUTH",
                "ALFRESCO_ROOT",
                "PREVIEW_URL",
                "AUTH",
            ],
            "pristy-social": [
                "APP_ROOT",
                "BREADCRUMB_ROOT_URL",
                "ALFRESCO_HOST",
                "ALFRESCO_AUTH",
                "ALFRESCO_ROOT",
                "AUTH",
            ],
        },
    },
    "audit": {
        "default_formats": ["md", "html", "zip"],
        "default_output_dir": ".",
    },
}


class Config:
    """Configuration manager for Pristy support tool."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config = DEFAULT_CONFIG.copy()
        self.config_path = None

        if config_path:
            self.load_from_file(config_path)
        else:
            self.load_default_paths()

    def load_default_paths(self):
        """Try to load config from default paths."""
        default_paths = [
            Path.cwd() / "pristy-support.yml",
            Path.cwd() / ".pristy-support.yml",
            Path.home() / ".pristy-support.yml",
            Path.home() / ".config" / "pristy-support" / "config.yml",
            Path("/etc/pristy/pristy-support.yml"),
        ]

        for path in default_paths:
            if path.exists():
                self.load_from_file(str(path))
                break

    def load_from_file(self, config_path: str):
        """Load configuration from YAML file."""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f)

            if user_config:
                self._merge_config(self.config, user_config)
                self.config_path = config_path
        except (FileNotFoundError, yaml.YAMLError) as e:
            # Keep default config if file not found or invalid
            pass

    def _merge_config(self, base: Dict, update: Dict):
        """Recursively merge user config into base config."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key_path.split(".")
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def to_yaml(self) -> str:
        """Export configuration to YAML string."""
        return yaml.dump(self.config, default_flow_style=False, sort_keys=False)

    @staticmethod
    def generate_default_config_file(output_path: str) -> str:
        """Generate default configuration file."""
        header = """# Pristy Support Configuration File
#
# This file allows you to customize the behavior of pristy-support tool.
# All values shown are defaults and can be modified as needed.
#
# Configuration file locations (in order of priority):
#   1. ./pristy-support.yml (current directory)
#   2. ./.pristy-support.yml (current directory, hidden)
#   3. ~/.pristy-support.yml (user home directory)
#   4. ~/.config/pristy-support/config.yml (XDG config directory)
#   5. /etc/pristy/pristy-support.yml (system-wide configuration)
#
# You can also specify a custom config file with: pristy-support --config /path/to/config.yml

"""
        config_yaml = yaml.dump(
            DEFAULT_CONFIG, default_flow_style=False, sort_keys=False
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(config_yaml)

        return output_path


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def set_config(config: Config):
    """Set global configuration instance."""
    global _config_instance
    _config_instance = config
