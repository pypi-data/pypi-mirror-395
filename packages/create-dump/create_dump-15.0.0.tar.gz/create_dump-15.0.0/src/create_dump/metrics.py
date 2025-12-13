# src/create_dump/metrics.py

"""Defines Prometheus metrics and the metrics server."""

from __future__ import annotations

from contextlib import contextmanager
from prometheus_client import Counter, Histogram, start_http_server

# Port
DEFAULT_METRICS_PORT = 8000

# Metrics
DUMP_DURATION = Histogram(
    "create_dump_duration_seconds",
    "Dump duration",
    buckets=[1, 5, 30, 60, 300, float("inf")],
    labelnames=["collector"],  # ⚡ REFACTOR: Add collector label
)
# 🐞 FIX: Add _total suffix for Prometheus convention
FILES_PROCESSED = Counter("create_dump_files_total", "Files processed", ["status"])
# 🐞 FIX: Add _total suffix for Prometheus convention
ERRORS_TOTAL = Counter("create_dump_errors_total", "Errors encountered", ["type"])
ROLLBACKS_TOTAL = Counter("create_dump_rollbacks_total", "Batch rollbacks", ["reason"])

# ✨ NEW: Add metric for archive creation
ARCHIVES_CREATED_TOTAL = Counter(
    "create_dump_archives_total",
    "Archives created",
    ["format"],
)


@contextmanager
def metrics_server(port: int = DEFAULT_METRICS_PORT):
    """Start configurable metrics server with auto-cleanup."""
    if port > 0:
        start_http_server(port)
    try:
        yield
    finally:
        pass  # Server runs in a daemon thread