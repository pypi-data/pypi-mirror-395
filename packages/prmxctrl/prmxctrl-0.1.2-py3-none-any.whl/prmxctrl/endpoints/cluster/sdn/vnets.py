"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .vnet_item._item import ClusterSdnVnetsEndpoints1
from prmxctrl.models.cluster import Cluster_Sdn_VnetsGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_VnetsGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_VnetsPOSTRequest  # type: ignore

class ClusterSdnVnetsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/sdn/vnets
    """


    def __call__(self, vnet: str) -> ClusterSdnVnetsEndpoints1:
        """Access specific vnet"""
        from .vnet_item._item import ClusterSdnVnetsEndpoints1  # type: ignore
        return ClusterSdnVnetsEndpoints1(
            self._client,
            self._build_path(str(vnet))
        )


    async def list(self, params: Cluster_Sdn_VnetsGETRequest | None = None) -> Cluster_Sdn_VnetsGETResponse:
        """
        SDN vnets index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Sdn_VnetsPOSTRequest | None = None) -> Any:
        """
        Create a new sdn vnet object.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

