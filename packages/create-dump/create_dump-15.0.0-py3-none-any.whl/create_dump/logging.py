# src/create_dump/logging.py

"""Manages logging, console output, and Rich integration."""

from __future__ import annotations

import logging
import re
import structlog

# Rich
HAS_RICH = False
console = None
Progress = None
SpinnerColumn = None
TextColumn = None
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

    console = Console()
    HAS_RICH = True
except ImportError:
    pass

# Define logger EARLY to avoid circular imports
logger = structlog.get_logger("create_dump")


def styled_print(text: str, nl: bool = True, **kwargs) -> None:
    """Prints text using Rich if available, falling back to plain print."""
    end = "" if not nl else "\n"
    if HAS_RICH and console is not None:
        console.print(text, end=end, **kwargs)
    else:
        clean_text = re.sub(r"\[/?[^\]]+\]", "", text)
        print(clean_text, end=end, **kwargs)


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure structured logging once."""
    level = "DEBUG" if verbose else "WARNING" if quiet else "INFO"
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if HAS_RICH:
        try:
            from structlog.dev import ConsoleRenderer
            processors.append(ConsoleRenderer(pad_event=40))
        except ImportError:
            processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=level, force=True)