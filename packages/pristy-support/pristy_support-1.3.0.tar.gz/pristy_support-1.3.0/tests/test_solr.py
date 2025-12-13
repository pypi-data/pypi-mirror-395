# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for Solr module."""

import pytest
from pristy_support.modules import solr


def test_parse_xml_value_long():
    """Test parsing long XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<long name="test">12345</long>')
    result = solr.parse_xml_value(element)
    assert result == 12345
    assert isinstance(result, int)


def test_parse_xml_value_int():
    """Test parsing int XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<int name="test">42</int>')
    result = solr.parse_xml_value(element)
    assert result == 42
    assert isinstance(result, int)


def test_parse_xml_value_double():
    """Test parsing double XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<double name="test">3.14159</double>')
    result = solr.parse_xml_value(element)
    assert result == 3.14159
    assert isinstance(result, float)


def test_parse_xml_value_float():
    """Test parsing float XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<float name="test">2.718</float>')
    result = solr.parse_xml_value(element)
    assert result == 2.718
    assert isinstance(result, float)


def test_parse_xml_value_bool_true():
    """Test parsing boolean true XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<bool name="test">true</bool>')
    result = solr.parse_xml_value(element)
    assert result is True


def test_parse_xml_value_bool_false():
    """Test parsing boolean false XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<bool name="test">false</bool>')
    result = solr.parse_xml_value(element)
    assert result is False


def test_parse_xml_value_str():
    """Test parsing string XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<str name="test">Hello World</str>')
    result = solr.parse_xml_value(element)
    assert result == "Hello World"
    assert isinstance(result, str)


def test_parse_xml_value_date():
    """Test parsing date XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<date name="test">2025-10-23T12:00:00Z</date>')
    result = solr.parse_xml_value(element)
    assert result == "2025-10-23T12:00:00Z"


def test_parse_xml_value_none():
    """Test parsing None (no element)."""
    result = solr.parse_xml_value(None, default="default")
    assert result == "default"


def test_parse_xml_value_empty():
    """Test parsing empty XML values."""
    import xml.etree.ElementTree as ET

    element = ET.fromstring('<str name="test"></str>')
    result = solr.parse_xml_value(element, default="default")
    assert result == "default"


def test_parse_lst_to_dict():
    """Test parsing Solr lst element to dictionary."""
    import xml.etree.ElementTree as ET

    xml_str = """
    <lst name="test">
        <long name="count">100</long>
        <str name="status">OK</str>
        <bool name="enabled">true</bool>
    </lst>
    """
    element = ET.fromstring(xml_str)
    result = solr.parse_lst_to_dict(element)

    assert result == {"count": 100, "status": "OK", "enabled": True}


def test_parse_lst_to_dict_nested():
    """Test parsing nested Solr lst elements."""
    import xml.etree.ElementTree as ET

    xml_str = """
    <lst name="test">
        <long name="count">100</long>
        <lst name="nested">
            <str name="value">nested_value</str>
        </lst>
    </lst>
    """
    element = ET.fromstring(xml_str)
    result = solr.parse_lst_to_dict(element)

    assert result == {"count": 100, "nested": {"value": "nested_value"}}


def test_parse_summary_response_alfresco_core():
    """Test parsing SUMMARY response for alfresco core."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="responseHeader">
            <int name="status">0</int>
        </lst>
        <lst name="Summary">
            <lst name="alfresco">
                <long name="Alfresco Nodes in Index">1000</long>
                <long name="Alfresco Transactions in Index">500</long>
                <long name="Alfresco Acls in Index">200</long>
                <long name="Alfresco Acl Transactions in Index">100</long>
                <long name="Alfresco Unindexed Nodes">5</long>
                <long name="Alfresco Error Nodes in Index">2</long>
                <str name="TX Lag">0 s</str>
                <str name="Change Set Lag">0 s</str>
                <str name="On disk (GB)">2.5</str>
                <bool name="MetadataTracker Enabled">true</bool>
                <bool name="ContentTracker Enabled">true</bool>
                <bool name="AclTracker Enabled">true</bool>
                <bool name="MetadataTracker Active">true</bool>
                <bool name="ContentTracker Active">false</bool>
                <bool name="AclTracker Active">true</bool>
                <lst name="Searcher">
                    <int name="numDocs">1000</int>
                    <int name="maxDoc">1005</int>
                    <int name="deletedDocs">5</int>
                </lst>
            </lst>
        </lst>
    </response>
    """

    result = solr.parse_summary_response(xml_content)

    assert "alfresco" in result
    core = result["alfresco"]
    assert core["nodes_in_index"] == 1000
    assert core["transactions_in_index"] == 500
    assert core["acls_in_index"] == 200
    assert core["acl_transactions_in_index"] == 100
    assert core["unindexed_nodes"] == 5
    assert core["error_nodes"] == 2
    assert core["tx_lag"] == "0 s"
    assert core["changeset_lag"] == "0 s"
    assert core["disk_size_gb"] == "2.5"

    assert "trackers" in core
    assert core["trackers"]["metadata_enabled"] is True
    assert core["trackers"]["content_enabled"] is True
    assert core["trackers"]["acl_enabled"] is True
    assert core["trackers"]["metadata_active"] is True
    assert core["trackers"]["content_active"] is False
    assert core["trackers"]["acl_active"] is True

    assert "searcher" in core
    assert core["searcher"]["num_docs"] == 1000
    assert core["searcher"]["max_doc"] == 1005
    assert core["searcher"]["deleted_docs"] == 5


def test_parse_summary_response_with_cache():
    """Test parsing SUMMARY response with cache statistics."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="Summary">
            <lst name="alfresco">
                <long name="Alfresco Nodes in Index">1000</long>
                <long name="Alfresco Transactions in Index">500</long>
                <long name="Alfresco Acls in Index">200</long>
                <long name="Alfresco Acl Transactions in Index">100</long>
                <long name="Alfresco Unindexed Nodes">0</long>
                <long name="Alfresco Error Nodes in Index">0</long>
                <str name="TX Lag">0 s</str>
                <str name="Change Set Lag">0 s</str>
                <lst name="/queryResultCache">
                    <long name="cumulative_hits">5000</long>
                    <long name="cumulative_lookups">10000</long>
                    <float name="cumulative_hitratio">0.5</float>
                    <int name="size">100</int>
                    <long name="cumulative_evictions">10</long>
                </lst>
            </lst>
        </lst>
    </response>
    """

    result = solr.parse_summary_response(xml_content)

    assert "alfresco" in result
    core = result["alfresco"]
    assert "caches" in core
    assert "queryResultCache" in core["caches"]

    cache = core["caches"]["queryResultCache"]
    assert cache["cumulative_hits"] == 5000
    assert cache["cumulative_lookups"] == 10000
    assert cache["cumulative_hitratio"] == 0.5
    assert cache["size"] == 100
    assert cache["evictions"] == 10


def test_parse_summary_response_with_handler():
    """Test parsing SUMMARY response with handler statistics."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="Summary">
            <lst name="alfresco">
                <long name="Alfresco Nodes in Index">1000</long>
                <long name="Alfresco Transactions in Index">500</long>
                <long name="Alfresco Acls in Index">200</long>
                <long name="Alfresco Acl Transactions in Index">100</long>
                <long name="Alfresco Unindexed Nodes">0</long>
                <long name="Alfresco Error Nodes in Index">0</long>
                <str name="TX Lag">0 s</str>
                <str name="Change Set Lag">0 s</str>
                <lst name="/alfresco">
                    <long name="requests">10000</long>
                    <long name="errors">5</long>
                    <long name="serverErrors">2</long>
                    <long name="clientErrors">3</long>
                    <long name="timeouts">0</long>
                    <double name="avgTimePerRequest">25.5</double>
                </lst>
            </lst>
        </lst>
    </response>
    """

    result = solr.parse_summary_response(xml_content)

    assert "alfresco" in result
    core = result["alfresco"]
    assert "handlers" in core
    assert "/alfresco" in core["handlers"]

    handler = core["handlers"]["/alfresco"]
    assert handler["requests"] == 10000
    assert handler["errors"] == 5
    assert handler["server_errors"] == 2
    assert handler["client_errors"] == 3
    assert handler["timeouts"] == 0
    assert handler["avg_time_per_request"] == 25.5


def test_parse_summary_response_with_fts():
    """Test parsing SUMMARY response with FTS statistics."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="Summary">
            <lst name="alfresco">
                <long name="Alfresco Nodes in Index">1000</long>
                <long name="Alfresco Transactions in Index">500</long>
                <long name="Alfresco Acls in Index">200</long>
                <long name="Alfresco Acl Transactions in Index">100</long>
                <long name="Alfresco Unindexed Nodes">0</long>
                <long name="Alfresco Error Nodes in Index">0</long>
                <str name="TX Lag">0 s</str>
                <str name="Change Set Lag">0 s</str>
                <lst name="FTS">
                    <long name="Node count whose content is in sync">950</long>
                    <long name="Node count whose content needs to be updated">50</long>
                </lst>
            </lst>
        </lst>
    </response>
    """

    result = solr.parse_summary_response(xml_content)

    assert "alfresco" in result
    core = result["alfresco"]
    assert "fts" in core
    assert core["fts"]["content_in_sync"] == 950
    assert core["fts"]["content_needs_update"] == 50


def test_parse_report_response():
    """Test parsing REPORT response."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="report">
            <lst name="alfresco">
                <str name="ACL Tracker">Up to date</str>
                <str name="Metadata Tracker">Up to date</str>
                <long name="DB acl transaction count">100</long>
                <long name="Index acl transaction count">100</long>
                <long name="Count of duplicated acl transactions in the index">0</long>
                <long name="Count of acl transactions in the index but not the DB">0</long>
                <long name="Count of missing acl transactions from the Index">0</long>
                <long name="DB transaction count">500</long>
                <long name="Index transaction count">500</long>
                <long name="Count of duplicated transactions in the index">0</long>
                <long name="Count of transactions in the index but not the DB">0</long>
                <long name="Count of missing transactions from the Index">0</long>
                <long name="Index node count">1000</long>
                <long name="Count of duplicate nodes in the index">0</long>
                <long name="Index error count">0</long>
                <long name="Index unindexed count">0</long>
                <long name="Last indexed transaction commit time">1729680000000</long>
                <str name="Last indexed transaction commit date">2025-10-23T10:00:00.000Z</str>
                <long name="Node count whose content is in sync">950</long>
                <long name="Node count whose content needs to be updated">50</long>
            </lst>
        </lst>
    </response>
    """

    result = solr.parse_report_response(xml_content)

    assert "alfresco" in result
    report = result["alfresco"]

    assert report["acl_tracker"] == "Up to date"
    assert report["metadata_tracker"] == "Up to date"
    assert report["db_acl_transaction_count"] == 100
    assert report["index_acl_transaction_count"] == 100
    assert report["duplicated_acl_transactions"] == 0
    assert report["acl_transactions_in_index_not_db"] == 0
    assert report["missing_acl_transactions"] == 0
    assert report["db_transaction_count"] == 500
    assert report["index_transaction_count"] == 500
    assert report["duplicated_transactions"] == 0
    assert report["transactions_in_index_not_db"] == 0
    assert report["missing_transactions"] == 0
    assert report["index_node_count"] == 1000
    assert report["duplicate_nodes"] == 0
    assert report["index_error_count"] == 0
    assert report["index_unindexed_count"] == 0
    assert report["last_indexed_tx_commit_time"] == 1729680000000
    assert report["last_indexed_tx_commit_date"] == "2025-10-23T10:00:00.000Z"
    assert report["content_in_sync"] == 950
    assert report["content_needs_update"] == 50


def test_parse_summary_response_invalid_xml():
    """Test parsing invalid XML returns empty dict."""
    xml_content = "not valid xml"
    result = solr.parse_summary_response(xml_content)
    assert result == {}


def test_parse_report_response_invalid_xml():
    """Test parsing invalid XML returns empty dict."""
    xml_content = "not valid xml"
    result = solr.parse_report_response(xml_content)
    assert result == {}


def test_parse_summary_response_empty():
    """Test parsing empty SUMMARY response."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="Summary">
        </lst>
    </response>
    """
    result = solr.parse_summary_response(xml_content)
    assert result == {}


def test_parse_report_response_empty():
    """Test parsing empty REPORT response."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="report">
        </lst>
    </response>
    """
    result = solr.parse_report_response(xml_content)
    assert result == {}


def test_parse_summary_response_archive_core():
    """Test parsing SUMMARY response for archive core."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="Summary">
            <lst name="archive">
                <long name="Alfresco Nodes in Index">50</long>
                <long name="Alfresco Transactions in Index">25</long>
                <long name="Alfresco Acls in Index">10</long>
                <long name="Alfresco Acl Transactions in Index">5</long>
                <long name="Alfresco Unindexed Nodes">0</long>
                <long name="Alfresco Error Nodes in Index">0</long>
                <str name="TX Lag">0 s</str>
                <str name="Change Set Lag">0 s</str>
            </lst>
        </lst>
    </response>
    """

    result = solr.parse_summary_response(xml_content)

    assert "archive" in result
    core = result["archive"]
    assert core["nodes_in_index"] == 50
    assert core["transactions_in_index"] == 25


def test_parse_report_response_archive_core():
    """Test parsing REPORT response for archive core."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <lst name="report">
            <lst name="archive">
                <str name="ACL Tracker">Up to date</str>
                <str name="Metadata Tracker">Up to date</str>
                <long name="DB acl transaction count">5</long>
                <long name="Index acl transaction count">5</long>
                <long name="Count of duplicated acl transactions in the index">0</long>
                <long name="Count of acl transactions in the index but not the DB">0</long>
                <long name="Count of missing acl transactions from the Index">0</long>
                <long name="DB transaction count">25</long>
                <long name="Index transaction count">25</long>
                <long name="Count of duplicated transactions in the index">0</long>
                <long name="Count of transactions in the index but not the DB">0</long>
                <long name="Count of missing transactions from the Index">0</long>
                <long name="Index node count">50</long>
                <long name="Count of duplicate nodes in the index">0</long>
                <long name="Index error count">0</long>
                <long name="Index unindexed count">0</long>
                <long name="Last indexed transaction commit time">1729680000000</long>
                <str name="Last indexed transaction commit date">2025-10-23T10:00:00.000Z</str>
                <long name="Node count whose content is in sync">50</long>
                <long name="Node count whose content needs to be updated">0</long>
            </lst>
        </lst>
    </response>
    """

    result = solr.parse_report_response(xml_content)

    assert "archive" in result
    report = result["archive"]
    assert report["acl_tracker"] == "Up to date"
    assert report["metadata_tracker"] == "Up to date"
    assert report["index_node_count"] == 50
