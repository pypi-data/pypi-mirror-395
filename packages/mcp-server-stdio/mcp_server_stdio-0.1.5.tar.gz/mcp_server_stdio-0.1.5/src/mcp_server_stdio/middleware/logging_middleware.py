"""Logging middleware for FastMCP requests.

This module provides middleware for logging all incoming requests and responses
in a structured format.
"""

from __future__ import annotations

import json

from fastmcp.server.middleware import Middleware, MiddlewareContext

from helpers.logging_config import get_logger

logger = get_logger()


class LoggingMiddleware(Middleware):
    """Middleware that logs all MCP requests and responses."""

    async def on_message(
        self, context: MiddlewareContext, call_next
    ) -> MiddlewareContext:
        """Log request received, process it, and log completion or failure.

        Args:
            context: Middleware context containing request information
            call_next: Next middleware in the chain

        Returns:
            Result from the next middleware

        Raises:
            Exception: Re-raises any exception after logging
        """
        # Log request with safe fields only
        safe_log = {
            "event": "request_received",
            "method": context.method,
            "source": context.source,
        }
        logger.info(json.dumps(safe_log))

        try:
            result = await call_next(context)

            logger.info(
                json.dumps(
                    {
                        "event": "request_completed",
                        "method": context.method,
                    }
                )
            )
            return result

        except Exception as e:
            logger.error(
                json.dumps(
                    {
                        "event": "request_failed",
                        "method": context.method,
                        "error": str(e),
                    }
                )
            )
            raise


__all__ = ["LoggingMiddleware"]
