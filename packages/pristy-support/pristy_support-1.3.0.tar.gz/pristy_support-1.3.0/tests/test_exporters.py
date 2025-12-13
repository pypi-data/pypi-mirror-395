# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for exporters."""

import pytest
from pristy_support.exporters import markdown, html


def test_markdown_export_empty_data():
    """Test markdown export with minimal data."""
    audit_data = {
        "system": {
            "system_info": {"hostname": "test-host", "os_distribution": "Test OS"}
        }
    }
    result = markdown.export_to_markdown(audit_data)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "test-host" in result


def test_html_export_empty_data():
    """Test HTML export with minimal data."""
    audit_data = {
        "system": {
            "system_info": {"hostname": "test-host", "os_distribution": "Test OS"}
        }
    }
    result = html.export_to_html(audit_data)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "<!DOCTYPE html>" in result or "<html" in result
    assert "test-host" in result


def test_markdown_format_status_badge():
    """Test status badge formatting."""
    from pristy_support.exporters.markdown import format_status_badge

    assert "✅" in format_status_badge("OK")
    assert "⚠️" in format_status_badge("WARNING")
    assert "❌" in format_status_badge("ERROR")
