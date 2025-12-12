"""HTTP client utilities for making API requests.

This module provides utilities for making HTTP requests with proper logging,
error handling, and response parsing.
"""

from __future__ import annotations

from typing import Any

import httpx

from mcp_server_stdio.helpers.logging_config import get_logger

logger = get_logger()

# Constants
DEFAULT_TIMEOUT = 30.0
JSON_CONTENT_TYPE = "application/json"


def _sanitize_headers(headers: dict[str, str] | None) -> dict[str, str]:
    """Sanitize headers by masking sensitive values.

    Args:
        headers: Dictionary of HTTP headers

    Returns:
        Dictionary with sensitive header values masked
    """
    if not headers:
        return {}
    return {k: "***" if "key" in k.lower() else v for k, v in headers.items()}


async def get_json(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any] | str:
    """Make a GET request and return JSON or text response.

    Args:
        url: The URL to request
        params: Optional query parameters
        headers: Optional HTTP headers
        timeout: Request timeout in seconds (default: 30.0)

    Returns:
        Parsed JSON response as dict, or raw text if not JSON

    Raises:
        httpx.HTTPError: If the request fails
    """
    safe_headers = _sanitize_headers(headers)

    logger.debug(
        {
            "event": "http_request",
            "url": url,
            "params": params,
            "headers": safe_headers,
        }
    )

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
            )

        logger.debug(
            {
                "event": "http_response",
                "status": response.status_code,
                "url": str(response.request.url),
            }
        )

        response.raise_for_status()

        # Parse JSON if content-type indicates JSON
        content_type = response.headers.get("content-type", "")
        if content_type.startswith(JSON_CONTENT_TYPE):
            return response.json()

        return response.text

    except httpx.HTTPError as e:
        logger.error(
            {
                "event": "http_error",
                "url": url,
                "params": params,
                "headers": safe_headers,
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
                "response_text": getattr(e.response, "text", None),
            }
        )
        raise


__all__ = ["get_json"]
