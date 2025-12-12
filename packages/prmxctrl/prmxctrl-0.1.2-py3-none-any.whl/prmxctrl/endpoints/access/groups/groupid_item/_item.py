"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Groups_GroupidDELETERequest
from prmxctrl.models.access import Access_Groups_GroupidGETRequest
from prmxctrl.models.access import Access_Groups_GroupidGETResponse
from prmxctrl.models.access import Access_Groups_GroupidPUTRequest  # type: ignore

class AccessGroupsEndpoints1(EndpointBase):
    """
    Endpoint class for /access/groups/{groupid}
    """



    async def delete(self, params: Access_Groups_GroupidDELETERequest | None = None) -> Any:
        """
        Delete group.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Access_Groups_GroupidGETRequest | None = None) -> Access_Groups_GroupidGETResponse:
        """
        Get group configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_group(self, params: Access_Groups_GroupidPUTRequest | None = None) -> Any:
        """
        Update group data.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

