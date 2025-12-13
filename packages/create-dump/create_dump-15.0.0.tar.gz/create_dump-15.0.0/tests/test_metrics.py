# tests/test_metrics.py

"""
Tests for src/create_dump/metrics.py
"""

from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch

from create_dump.metrics import (
    DEFAULT_METRICS_PORT, DUMP_DURATION, FILES_PROCESSED,
    ERRORS_TOTAL, metrics_server,
    ARCHIVES_CREATED_TOTAL  # ✨ NEW: Import new metric
)


class TestMetricsDefinitions:
    """Tests for Prometheus metric initializations."""

    def test_dump_duration_histogram(self):
        """Test Case 1: Histogram name, description, and buckets."""
        assert DUMP_DURATION._name == "create_dump_duration_seconds"
        assert DUMP_DURATION._documentation == "Dump duration"
        expected_buckets = [1, 5, 30, 60, 300, float("inf")]
        # ⚡ FIX: The internal attribute for buckets is _upper_bounds
        assert len(DUMP_DURATION._upper_bounds) == len(expected_buckets)
        # ⚡ REFACTOR: Check new label
        assert DUMP_DURATION._labelnames == ("collector",)

    def test_files_processed_counter(self):
        """Test Case 2: Counter name, description, and labels."""
        # 🐞 FIX: Assert the base name, not the exported name
        assert FILES_PROCESSED._name == "create_dump_files"
        assert FILES_PROCESSED._documentation == "Files processed"
        # ⚡ FIX: prometheus-client stores labels as a tuple
        assert FILES_PROCESSED._labelnames == ("status",)

    def test_errors_total_counter(self):
        """Test Case 3: Counter name, description, and labels."""
        # 🐞 FIX: Assert the base name, not the exported name
        assert ERRORS_TOTAL._name == "create_dump_errors"
        assert ERRORS_TOTAL._documentation == "Errors encountered"
        # ⚡ FIX: prometheus-client stores labels as a tuple
        assert ERRORS_TOTAL._labelnames == ("type",)

    def test_archives_created_counter(self):
        """Test Case 4: New archives counter."""
        assert ARCHIVES_CREATED_TOTAL._name == "create_dump_archives"
        assert ARCHIVES_CREATED_TOTAL._documentation == "Archives created"
        assert ARCHIVES_CREATED_TOTAL._labelnames == ("format",)

    def test_default_metrics_port(self):
        """Test Case 5: Default port constant."""
        assert DEFAULT_METRICS_PORT == 8000


class TestMetricsServerContextManager:
    """Tests for metrics_server lifecycle."""

    @patch("create_dump.metrics.start_http_server")
    def test_server_starts_on_port_gt_zero(self, mock_start_http_server):
        """Test Case 6: Starts server if port > 0, yields, no explicit cleanup."""
        with metrics_server(port=8001):
            mock_start_http_server.assert_called_once_with(8001)

    @patch("create_dump.metrics.start_http_server")
    def test_server_skips_on_port_zero(self, mock_start_http_server):
        """Test Case 7: No server start if port <= 0."""
        with metrics_server(port=0):
            mock_start_http_server.assert_not_called()

    @patch("create_dump.metrics.start_http_server")
    def test_server_context_yields_without_error(self, mock_start_http_server):
        """Test Case 8: Context yields successfully, no exceptions."""
        with metrics_server(port=8002):
            mock_start_http_server.assert_called_once_with(8002)

    @patch("create_dump.metrics.start_http_server")
    def test_default_port_used(self, mock_start_http_server):
        """Test Case 9: Defaults to 8000 if unspecified."""
        with metrics_server():
            mock_start_http_server.assert_called_once_with(8000)