"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_AclGETResponse
from prmxctrl.models.access import Access_AclPUTRequest  # type: ignore

class AccessAclEndpoints(EndpointBase):
    """
    Endpoint class for /access/acl
    """



    async def list(self, ) -> Access_AclGETResponse:
        """
        Get Access Control List (ACLs).

        HTTP Method: GET
        """
        return await self._get()

    async def update_acl(self, params: Access_AclPUTRequest | None = None) -> Any:
        """
        Update Access Control List (add or remove permissions).

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

