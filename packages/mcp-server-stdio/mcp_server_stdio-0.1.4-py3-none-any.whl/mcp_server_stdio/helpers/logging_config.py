"""Logging configuration for the MCP service.

This module sets up structured JSON logging for the entire application,
providing consistent log formatting and output.
"""

from __future__ import annotations

import logging
import sys

from pythonjsonlogger import jsonlogger

from mcp_server_stdio.core.constants import LOGGER_NAME


def setup_json_logging(level: int = logging.DEBUG) -> logging.Logger:
    """Configure JSON-formatted logging for the application.

    Sets up structured logging with JSON formatting, outputting to stdout.
    This configuration applies globally to all loggers in the application.

    Args:
        level: Logging level (default: logging.DEBUG)

    Returns:
        Configured root logger instance
    """
    log_handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [log_handler]

    # Prevent duplicate logs
    root_logger.propagate = False

    return root_logger


def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Logger name (default: 'mcp' from constants)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


__all__ = ["setup_json_logging", "get_logger"]
