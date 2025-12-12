"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .subnets._item import ClusterSdnVnetsSubnetsEndpoints
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_VnetDELETERequest
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_VnetGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_VnetGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_VnetPUTRequest  # type: ignore

class ClusterSdnVnetsEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/sdn/vnets/{vnet}
    """

    # Sub-endpoint properties
    @property
    def subnets(self) -> ClusterSdnVnetsSubnetsEndpoints:
        """Access subnets endpoints"""
        from .subnets._item import ClusterSdnVnetsSubnetsEndpoints  # type: ignore
        return ClusterSdnVnetsSubnetsEndpoints(self._client, self._build_path("subnets"))



    async def delete(self, params: Cluster_Sdn_Vnets_VnetDELETERequest | None = None) -> Any:
        """
        Delete sdn vnet object configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Sdn_Vnets_VnetGETRequest | None = None) -> Cluster_Sdn_Vnets_VnetGETResponse:
        """
        Read sdn vnet configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Sdn_Vnets_VnetPUTRequest | None = None) -> Any:
        """
        Update sdn vnet object configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

