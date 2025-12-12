"""Application constants and configuration values.

This module centralizes all magic strings, configuration values, and
constants used throughout the application.
"""

from __future__ import annotations

# HTTP Configuration
DEFAULT_REQUEST_TIMEOUT = 30.0
JSON_CONTENT_TYPE = "application/json"

# API Configuration
API_COMPUTE_OFFERINGS_PATH = "/restapi/costestimate/compute-plan-list"
API_VPN_USER_COST_PATH = "/restapi/costestimate/vpn-user-cost"

# Compute Offering Types
COMPUTE_OFFERING_TYPE_PAY_AS_YOU_GO = "PAY_AS_YOU_GO"

# Default Language
DEFAULT_LANGUAGE = "en"

# HTTP Headers
HEADER_API_KEY = "apikey"
HEADER_SECRET_KEY = "secretkey"
HEADER_CONTENT_TYPE = "content-type"

# Context State Keys
STATE_KEY_API_KEY = "api_key"
STATE_KEY_SECRET_KEY = "secret_key"
STATE_KEY_BASE_URL = "base_url"
STATE_KEY_ZONE_UUID = "zone_uuid"

# MCP Protocol Methods (exempt from authentication)
MCP_EXEMPT_METHODS = {
    "initialize",
    "initialized",
    "ping",
    "notifications/cancelled",
    "tools/list",
    "resources/list",
    "prompts/list",
    "completion/complete",
}

# Logging
LOGGER_NAME = "mcp"


__all__ = [
    "DEFAULT_REQUEST_TIMEOUT",
    "JSON_CONTENT_TYPE",
    "API_COMPUTE_OFFERINGS_PATH",
    "API_VPN_USER_COST_PATH",
    "COMPUTE_OFFERING_TYPE_PAY_AS_YOU_GO",
    "DEFAULT_LANGUAGE",
    "HEADER_API_KEY",
    "HEADER_SECRET_KEY",
    "HEADER_CONTENT_TYPE",
    "STATE_KEY_API_KEY",
    "STATE_KEY_SECRET_KEY",
    "STATE_KEY_BASE_URL",
    "STATE_KEY_ZONE_UUID",
    "MCP_EXEMPT_METHODS",
    "LOGGER_NAME",
]
