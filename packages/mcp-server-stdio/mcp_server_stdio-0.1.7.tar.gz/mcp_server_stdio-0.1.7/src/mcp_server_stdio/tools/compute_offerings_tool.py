"""MCP tools for compute offerings and VPN cost operations.

This module registers FastMCP tools that expose compute offerings and VPN
cost functionality to LLM clients.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastmcp import Context
from mcp_server_stdio.core.constants import DEFAULT_LANGUAGE
from mcp_server_stdio.exceptions.exception_handler import wrap_tool_exceptions
from mcp_server_stdio.services.compute_offerings_service import ComputeService

if TYPE_CHECKING:
    from fastmcp import FastMCP

# Service instance
service = ComputeService()


def register(mcp: FastMCP) -> None:
    """Register compute offerings tools with FastMCP.

    Args:
        mcp: FastMCP instance to register tools with
    """

    @mcp.tool()
    @wrap_tool_exceptions("Failed to fetch compute offerings")
    async def get_compute_offerings(
        context: Context,
        lang: str = DEFAULT_LANGUAGE,
    ) -> dict[str, Any]:
        """Fetch compute offerings from Stackbill API.

        Credentials are automatically loaded from mcp.json via authentication middleware.

        Args:
            context: FastMCP context containing credentials
            lang: Language code for response (default: 'en')

        Returns:
            Dictionary containing status, zone_id, and compute offerings data
        """
        data = await service.get_compute_offerings(context, lang)

        return {
            "status": "success",
            "data": data,
        }

    @mcp.tool()
    @wrap_tool_exceptions("Failed to fetch VPN user cost")
    async def get_vpn_user_cost(context: Context) -> dict[str, Any]:
        """Fetch VPN user cost from Stackbill API.

        Credentials are automatically loaded from mcp.json via authentication middleware.

        Args:
            context: FastMCP context containing credentials

        Returns:
            Dictionary containing status and VPN user cost data
        """
        res = await service.get_vpn_user_cost(context)

        return {
            "status": "success",
            **res,
        }


__all__ = ["register"]
