# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for config_manager module."""

import pytest
from pristy_support.config_manager import Config


def test_config_default_values():
    """Test that Config has default values."""
    config = Config()
    assert config.get("system.disk_thresholds") is not None
    assert config.get("system.memory.min_ram_gb") is not None
    assert config.get("database.container_name") is not None


def test_config_get_with_default():
    """Test that get() returns default when key doesn't exist."""
    config = Config()
    result = config.get("nonexistent.key", "default_value")
    assert result == "default_value"


def test_config_get_nested():
    """Test getting nested configuration values."""
    config = Config()
    # Test getting a nested value
    disk_thresholds = config.get("system.disk_thresholds", {})
    assert isinstance(disk_thresholds, dict)
