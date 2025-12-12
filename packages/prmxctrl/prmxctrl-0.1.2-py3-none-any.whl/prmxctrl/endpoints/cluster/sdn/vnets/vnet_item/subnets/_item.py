"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .subnet_item._item import ClusterSdnVnetsSubnetsEndpoints1
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_Vnet_SubnetsGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_Vnet_SubnetsGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_Vnet_SubnetsPOSTRequest  # type: ignore

class ClusterSdnVnetsSubnetsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/sdn/vnets/{vnet}/subnets
    """


    def __call__(self, subnet: str) -> ClusterSdnVnetsSubnetsEndpoints1:
        """Access specific subnet"""
        from .subnet_item._item import ClusterSdnVnetsSubnetsEndpoints1  # type: ignore
        return ClusterSdnVnetsSubnetsEndpoints1(
            self._client,
            self._build_path(str(subnet))
        )


    async def list(self, params: Cluster_Sdn_Vnets_Vnet_SubnetsGETRequest | None = None) -> Cluster_Sdn_Vnets_Vnet_SubnetsGETResponse:
        """
        SDN subnets index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Sdn_Vnets_Vnet_SubnetsPOSTRequest | None = None) -> Any:
        """
        Create a new sdn subnet object.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

