"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Sdn_Zones_ZoneDELETERequest
from prmxctrl.models.cluster import Cluster_Sdn_Zones_ZoneGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_Zones_ZoneGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_Zones_ZonePUTRequest  # type: ignore

class ClusterSdnZonesEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/sdn/zones/{zone}
    """



    async def delete(self, params: Cluster_Sdn_Zones_ZoneDELETERequest | None = None) -> Any:
        """
        Delete sdn zone object configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Sdn_Zones_ZoneGETRequest | None = None) -> Cluster_Sdn_Zones_ZoneGETResponse:
        """
        Read sdn zone configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Sdn_Zones_ZonePUTRequest | None = None) -> Any:
        """
        Update sdn zone object configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

