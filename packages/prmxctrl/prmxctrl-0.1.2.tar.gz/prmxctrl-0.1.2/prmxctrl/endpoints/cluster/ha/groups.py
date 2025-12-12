"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .group_item._item import ClusterHaGroupsEndpoints1
from prmxctrl.models.cluster import Cluster_Ha_GroupsGETResponse
from prmxctrl.models.cluster import Cluster_Ha_GroupsPOSTRequest  # type: ignore

class ClusterHaGroupsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha/groups
    """


    def __call__(self, group: str) -> ClusterHaGroupsEndpoints1:
        """Access specific group"""
        from .group_item._item import ClusterHaGroupsEndpoints1  # type: ignore
        return ClusterHaGroupsEndpoints1(
            self._client,
            self._build_path(str(group))
        )


    async def list(self, ) -> Cluster_Ha_GroupsGETResponse:
        """
        Get HA groups.

        HTTP Method: GET
        """
        return await self._get()

    async def create(self, params: Cluster_Ha_GroupsPOSTRequest | None = None) -> Any:
        """
        Create a new HA group.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

