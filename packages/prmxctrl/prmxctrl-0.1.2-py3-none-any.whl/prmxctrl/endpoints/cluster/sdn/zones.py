"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .zone_item._item import ClusterSdnZonesEndpoints1
from prmxctrl.models.cluster import Cluster_Sdn_ZonesGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_ZonesGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_ZonesPOSTRequest  # type: ignore

class ClusterSdnZonesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/sdn/zones
    """


    def __call__(self, zone: str) -> ClusterSdnZonesEndpoints1:
        """Access specific zone"""
        from .zone_item._item import ClusterSdnZonesEndpoints1  # type: ignore
        return ClusterSdnZonesEndpoints1(
            self._client,
            self._build_path(str(zone))
        )


    async def list(self, params: Cluster_Sdn_ZonesGETRequest | None = None) -> Cluster_Sdn_ZonesGETResponse:
        """
        SDN zones index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Sdn_ZonesPOSTRequest | None = None) -> Any:
        """
        Create a new sdn zone object.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

