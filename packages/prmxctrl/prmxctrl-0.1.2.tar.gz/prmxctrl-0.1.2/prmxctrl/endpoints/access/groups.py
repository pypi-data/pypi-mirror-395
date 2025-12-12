"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .groupid_item._item import AccessGroupsEndpoints1
from prmxctrl.models.access import Access_GroupsGETResponse
from prmxctrl.models.access import Access_GroupsPOSTRequest  # type: ignore

class AccessGroupsEndpoints(EndpointBase):
    """
    Endpoint class for /access/groups
    """


    def __call__(self, groupid: int) -> AccessGroupsEndpoints1:
        """Access specific groupid"""
        from .groupid_item._item import AccessGroupsEndpoints1  # type: ignore
        return AccessGroupsEndpoints1(
            self._client,
            self._build_path(str(groupid))
        )


    async def list(self, ) -> Access_GroupsGETResponse:
        """
        Group index.

        HTTP Method: GET
        """
        return await self._get()

    async def create_group(self, params: Access_GroupsPOSTRequest | None = None) -> Any:
        """
        Create new group.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

