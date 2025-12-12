"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_PermissionsGETRequest
from prmxctrl.models.access import Access_PermissionsGETResponse  # type: ignore

class AccessPermissionsEndpoints(EndpointBase):
    """
    Endpoint class for /access/permissions
    """



    async def get(self, params: Access_PermissionsGETRequest | None = None) -> Access_PermissionsGETResponse:
        """
        Retrieve effective permissions of given user/token.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

