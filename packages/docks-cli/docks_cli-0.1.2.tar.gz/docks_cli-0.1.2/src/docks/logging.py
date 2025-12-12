"""Logging configuration for Docks CLI."""

import logging
import sys
from typing import Optional

# Global logger instance
logger = logging.getLogger("docks")

# Track if logging has been configured
_configured = False


def setup_logging(verbose: bool = False, debug: bool = False) -> None:
    """Configure logging for the CLI.

    Args:
        verbose: Enable INFO level logging
        debug: Enable DEBUG level logging (includes HTTP requests)
    """
    global _configured
    if _configured:
        return

    # Determine log level
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    # Configure root logger
    logger.setLevel(level)

    # Create console handler with formatting
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    # Format: timestamp - level - message (for verbose/debug)
    if debug:
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    elif verbose:
        fmt = "%(levelname)s: %(message)s"
    else:
        fmt = "%(message)s"

    formatter = logging.Formatter(fmt, datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Also configure httpx logging for debug mode
    if debug:
        httpx_logger = logging.getLogger("httpx")
        httpx_logger.setLevel(logging.DEBUG)
        httpx_logger.addHandler(handler)

        httpcore_logger = logging.getLogger("httpcore")
        httpcore_logger.setLevel(logging.DEBUG)
        httpcore_logger.addHandler(handler)

    _configured = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Optional name for child logger (e.g., "docks.client")

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"docks.{name}")
    return logger
