# src/create_dump/cli/__init__.py
"""
CLI package entry point.

This file exposes the main 'app' object from main.py, allowing
the entry point 'create_dump.cli:app' to resolve correctly.
"""
from .main import app

__all__ = ["app"]