# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for access logs module."""

from datetime import datetime
from unittest.mock import MagicMock, patch
from pristy_support.modules import access_logs


def test_parse_nginx_log_line_direct():
    """Test parsing direct nginx log format."""
    line = '86.246.213.139 - - [21/Nov/2025:14:39:17 +0000] "GET /alfresco/api HTTP/2.0" 200 39659 "https://example.com/" "Mozilla/5.0"'

    result = access_logs.parse_nginx_log_line(line)

    assert result is not None
    assert result["ip"] == "86.246.213.139"
    assert result["method"] == "GET"
    assert result["url"] == "/alfresco/api"
    assert result["status"] == 200
    assert result["size"] == 39659
    assert result["referer"] == "https://example.com/"
    assert result["user_agent"] == "Mozilla/5.0"


def test_parse_nginx_log_line_journalctl():
    """Test parsing nginx log with journalctl prefix."""
    line = 'Nov 21 14:39:17 osono.jeci.xyz docker[2241314]: 86.246.213.139 - - [21/Nov/2025:14:39:17 +0000] "GET /alfresco/api HTTP/2.0" 200 39659 "https://example.com/" "Mozilla/5.0"'

    result = access_logs.parse_nginx_log_line(line)

    assert result is not None
    assert result["ip"] == "86.246.213.139"
    assert result["method"] == "GET"


def test_parse_nginx_log_line_invalid():
    """Test parsing invalid log line."""
    line = "Invalid log line format"

    result = access_logs.parse_nginx_log_line(line)

    assert result is None


def test_detect_os_and_browser_firefox_linux():
    """Test OS and browser detection for Firefox on Linux."""
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"
    )

    result = access_logs.detect_os_and_browser(user_agent)

    assert result["os"] == "Linux"
    assert result["browser"] == "Firefox"


def test_detect_os_and_browser_chrome_windows():
    """Test OS and browser detection for Chrome on Windows."""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    result = access_logs.detect_os_and_browser(user_agent)

    assert result["os"] == "Windows"
    assert result["browser"] == "Chrome"


def test_detect_os_and_browser_safari_mac():
    """Test OS and browser detection for Safari on Mac."""
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

    result = access_logs.detect_os_and_browser(user_agent)

    assert result["os"] == "Mac"
    assert result["browser"] == "Safari"


def test_classify_url_shared_link():
    """Test URL classification for shared-link."""
    url = "/alfresco/api/-default-/public/alfresco/versions/1/shared-links/RzOKXg2hTza-f5ZiqZB22g/content?attachment=false"

    result = access_logs.classify_url("GET", url)

    assert result == "shared-link"


def test_classify_url_rendition_doclib():
    """Test URL classification for rendition-doclib."""
    url = "/alfresco/api/-default-/public/alfresco/versions/1/nodes/5c64637b-fc09-4324-9b60-cd5f4a55a8c8/renditions/doclib/content"

    result = access_logs.classify_url("GET", url)

    assert result == "rendition-doclib"


def test_classify_url_search():
    """Test URL classification for search."""
    url = "/alfresco/api/-default-/public/search/versions/1/search"

    result = access_logs.classify_url("POST", url)

    assert result == "search"


def test_classify_url_download():
    """Test URL classification for download."""
    url = "/alfresco/api/-default-/public/alfresco/versions/1/nodes/4a6328f5-f18e-425e-a4f5-e4dda268fb29/versions/1.0/content"

    result = access_logs.classify_url("GET", url)

    assert result == "download"


def test_classify_url_other():
    """Test URL classification for other."""
    url = "/alfresco/api/some/other/path"

    result = access_logs.classify_url("GET", url)

    assert result == "other"


def test_extract_site_name():
    """Test site name extraction from referer."""
    referer = "https://jeci.pristy.net/espaces-rc/mes-espaces/Commercial/eebe3fe9-1966-498a-ba95-048a421acfe3"

    result = access_logs.extract_site_name(referer)

    assert result == "Commercial"


def test_extract_site_name_no_match():
    """Test site name extraction with no match."""
    referer = "https://jeci.pristy.net/some/other/path"

    result = access_logs.extract_site_name(referer)

    assert result is None


def test_calculate_requests_per_minute():
    """Test calculation of requests per minute."""
    timestamps = [
        datetime(2025, 11, 21, 14, 39, 10),
        datetime(2025, 11, 21, 14, 39, 20),
        datetime(2025, 11, 21, 14, 39, 30),
        datetime(2025, 11, 21, 14, 40, 10),
        datetime(2025, 11, 21, 14, 40, 20),
    ]

    result = access_logs.calculate_requests_per_minute(timestamps)

    assert result["max_per_minute"] == 3
    assert result["avg_per_minute"] == 2.5
    assert result["peak_timestamp"] == "2025-11-21 14:39"


def test_calculate_requests_per_minute_empty():
    """Test calculation with empty timestamps."""
    result = access_logs.calculate_requests_per_minute([])

    assert result["avg_per_minute"] == 0
    assert result["max_per_minute"] == 0
    assert result["peak_timestamp"] is None


def test_get_top_ips():
    """Test getting top IPs."""
    log_entries = [
        {"ip": "1.2.3.4"},
        {"ip": "1.2.3.4"},
        {"ip": "1.2.3.4"},
        {"ip": "5.6.7.8"},
        {"ip": "5.6.7.8"},
        {"ip": "9.10.11.12"},
    ]

    result = access_logs.get_top_ips(log_entries, limit=2)

    assert len(result) == 2
    assert result[0]["ip"] == "1.2.3.4"
    assert result[0]["requests"] == 3
    assert result[1]["ip"] == "5.6.7.8"
    assert result[1]["requests"] == 2


def test_get_top_sites():
    """Test getting top sites."""
    log_entries = [
        {"referer": "https://jeci.pristy.net/espaces-rc/mes-espaces/Commercial/xxx"},
        {"referer": "https://jeci.pristy.net/espaces-rc/mes-espaces/Commercial/yyy"},
        {"referer": "https://jeci.pristy.net/espaces-rc/mes-espaces/RH/zzz"},
        {"referer": "https://jeci.pristy.net/some/other/path"},
    ]

    result = access_logs.get_top_sites(log_entries, limit=2)

    assert len(result) == 2
    assert result[0]["site"] == "Commercial"
    assert result[0]["requests"] == 2
    assert result[1]["site"] == "RH"
    assert result[1]["requests"] == 1


@patch("pristy_support.modules.access_logs.subprocess.run")
@patch("pristy_support.modules.access_logs.permissions.detect_permissions")
def test_fetch_logs_journalctl(mock_perms, mock_subprocess):
    """Test fetching logs from journalctl."""
    mock_perms.return_value = {"has_sudo": False, "is_root": False}

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "log line 1\nlog line 2\nlog line 3"
    mock_subprocess.return_value = mock_result

    result = access_logs.fetch_logs_journalctl("nginx_pristy", 7, False)

    assert len(result) == 3
    assert result[0] == "log line 1"
    mock_subprocess.assert_called_once()


@patch("pristy_support.modules.access_logs.subprocess.run")
@patch("pristy_support.modules.access_logs.permissions.detect_permissions")
def test_fetch_logs_docker(mock_perms, mock_subprocess):
    """Test fetching logs from docker."""
    mock_perms.return_value = {"can_use_docker": False, "is_root": False}

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "log line 1\nlog line 2"
    mock_subprocess.return_value = mock_result

    result = access_logs.fetch_logs_docker("pristy-proxy", 7, False)

    assert len(result) == 2
    mock_subprocess.assert_called_once()
