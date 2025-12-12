"""Logging configuration for InnerLoop SDK.

Provides a simple API for users to configure logging levels and handlers.
"""

from __future__ import annotations

import logging
import sys
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# InnerLoop logger namespace
INNERLOOP_LOGGER = "innerloop"

# Default format for InnerLoop logs
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def configure_logging(
    level: LogLevel | int = "INFO",
    *,
    format: str | None = None,
    handler: logging.Handler | None = None,
) -> None:
    """Configure logging for the InnerLoop SDK.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) or numeric level
        format: Custom log format string (uses default if not provided)
        handler: Custom logging handler (creates StreamHandler if not provided)

    Examples:
        >>> import innerloop
        >>> innerloop.configure_logging("DEBUG")  # Enable debug logging
        >>> innerloop.configure_logging("WARNING")  # Only warnings and above
        >>> innerloop.configure_logging("INFO", format="%(levelname)s: %(message)s")
    """
    logger = logging.getLogger(INNERLOOP_LOGGER)

    # Convert string level to logging constant
    if isinstance(level, str):
        numeric_level = getattr(logging, level.upper())
    else:
        numeric_level = level

    logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create handler if not provided
    if handler is None:
        handler = logging.StreamHandler(sys.stderr)

    # Set format
    log_format = format or DEFAULT_FORMAT
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a logger within the InnerLoop namespace.

    Args:
        name: Name of the logger (will be prefixed with 'innerloop.')

    Returns:
        Logger instance
    """
    return logging.getLogger(f"{INNERLOOP_LOGGER}.{name}")


def disable_logging() -> None:
    """Disable all InnerLoop logging."""
    logger = logging.getLogger(INNERLOOP_LOGGER)
    logger.setLevel(logging.CRITICAL + 1)  # Higher than CRITICAL
    logger.handlers.clear()
    logger.propagate = False
