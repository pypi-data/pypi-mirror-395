"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Roles_RoleidDELETERequest
from prmxctrl.models.access import Access_Roles_RoleidGETRequest
from prmxctrl.models.access import Access_Roles_RoleidGETResponse
from prmxctrl.models.access import Access_Roles_RoleidPUTRequest  # type: ignore

class AccessRolesEndpoints1(EndpointBase):
    """
    Endpoint class for /access/roles/{roleid}
    """



    async def delete(self, params: Access_Roles_RoleidDELETERequest | None = None) -> Any:
        """
        Delete role.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Access_Roles_RoleidGETRequest | None = None) -> Access_Roles_RoleidGETResponse:
        """
        Get role configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_role(self, params: Access_Roles_RoleidPUTRequest | None = None) -> Any:
        """
        Update an existing role.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

