"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .ipam_item._item import ClusterSdnIpamsEndpoints1
from prmxctrl.models.cluster import Cluster_Sdn_IpamsGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_IpamsGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_IpamsPOSTRequest  # type: ignore

class ClusterSdnIpamsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/sdn/ipams
    """


    def __call__(self, ipam: str) -> ClusterSdnIpamsEndpoints1:
        """Access specific ipam"""
        from .ipam_item._item import ClusterSdnIpamsEndpoints1  # type: ignore
        return ClusterSdnIpamsEndpoints1(
            self._client,
            self._build_path(str(ipam))
        )


    async def list(self, params: Cluster_Sdn_IpamsGETRequest | None = None) -> Cluster_Sdn_IpamsGETResponse:
        """
        SDN ipams index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Sdn_IpamsPOSTRequest | None = None) -> Any:
        """
        Create a new sdn ipam object.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

