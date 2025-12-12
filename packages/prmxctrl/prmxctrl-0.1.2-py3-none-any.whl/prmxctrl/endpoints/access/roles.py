"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .roleid_item._item import AccessRolesEndpoints1
from prmxctrl.models.access import Access_RolesGETResponse
from prmxctrl.models.access import Access_RolesPOSTRequest  # type: ignore

class AccessRolesEndpoints(EndpointBase):
    """
    Endpoint class for /access/roles
    """


    def __call__(self, roleid: int) -> AccessRolesEndpoints1:
        """Access specific roleid"""
        from .roleid_item._item import AccessRolesEndpoints1  # type: ignore
        return AccessRolesEndpoints1(
            self._client,
            self._build_path(str(roleid))
        )


    async def list(self, ) -> Access_RolesGETResponse:
        """
        Role index.

        HTTP Method: GET
        """
        return await self._get()

    async def create_role(self, params: Access_RolesPOSTRequest | None = None) -> Any:
        """
        Create new role.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

