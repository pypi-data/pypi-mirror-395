"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ha_Groups_GroupDELETERequest
from prmxctrl.models.cluster import Cluster_Ha_Groups_GroupGETRequest
from prmxctrl.models.cluster import Cluster_Ha_Groups_GroupGETResponse
from prmxctrl.models.cluster import Cluster_Ha_Groups_GroupPUTRequest  # type: ignore

class ClusterHaGroupsEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/ha/groups/{group}
    """



    async def delete(self, params: Cluster_Ha_Groups_GroupDELETERequest | None = None) -> Any:
        """
        Delete ha group configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Ha_Groups_GroupGETRequest | None = None) -> Cluster_Ha_Groups_GroupGETResponse:
        """
        Read ha group configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Ha_Groups_GroupPUTRequest | None = None) -> Any:
        """
        Update ha group configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

