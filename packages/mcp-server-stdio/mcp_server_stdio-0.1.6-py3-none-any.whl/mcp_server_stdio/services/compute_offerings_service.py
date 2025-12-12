"""Service layer for compute offerings and related API operations.

This module provides business logic for interacting with Stackbill compute
and VPN APIs. Services extract credentials directly from Context, eliminating
prop drilling.
"""

from __future__ import annotations

from typing import Any

from fastmcp import Context
from mcp_server_stdio.core.constants import (
    API_COMPUTE_OFFERINGS_PATH,
    API_VPN_USER_COST_PATH,
    COMPUTE_OFFERING_TYPE_PAY_AS_YOU_GO,
    DEFAULT_LANGUAGE,
)
from mcp_server_stdio.helpers.credentials import CredentialsService
from mcp_server_stdio.helpers.http_client import get_json


class ComputeService:
    """Service for compute offerings and VPN cost operations.

    This service extracts credentials directly from the FastMCP Context,
    eliminating the need to pass credentials as parameters.
    """

    async def get_compute_offerings(
        self,
        context: Context,
        lang: str = DEFAULT_LANGUAGE,
    ) -> dict[str, Any]:
        """Fetch compute offerings from Stackbill API.

        Args:
            context: FastMCP context containing credentials
            lang: Language code for response (default: 'en')

        Returns:
            API response containing compute offerings data

        Raises:
            httpx.HTTPError: If the API request fails
            ValueError: If zone_uuid is not provided in credentials
        """
        credentials = CredentialsService.from_context(context)

        if not credentials.zone_uuid:
            raise ValueError("zone_uuid is required for compute offerings")

        url = f"{credentials.base_url}{API_COMPUTE_OFFERINGS_PATH}"
        params = {
            "zoneUuid": credentials.zone_uuid,
            "computeOfferingType": COMPUTE_OFFERING_TYPE_PAY_AS_YOU_GO,
            "lang": lang,
        }

        return await get_json(url, params, credentials.to_headers())

    async def get_vpn_user_cost(
        self,
        context: Context,
    ) -> dict[str, Any]:
        """Fetch VPN user cost from Stackbill API.

        Args:
            context: FastMCP context containing credentials

        Returns:
            Dictionary with 'data' key containing VPN user cost information

        Raises:
            httpx.HTTPError: If the API request fails
        """
        credentials = CredentialsService.from_context(context)

        url = f"{credentials.base_url}{API_VPN_USER_COST_PATH}"
        data = await get_json(url, headers=credentials.to_headers())
        return {"data": data}


__all__ = ["ComputeService"]
