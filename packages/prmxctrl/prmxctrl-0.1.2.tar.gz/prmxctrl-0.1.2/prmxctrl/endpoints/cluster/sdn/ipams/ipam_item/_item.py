"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Sdn_Ipams_IpamDELETERequest
from prmxctrl.models.cluster import Cluster_Sdn_Ipams_IpamGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_Ipams_IpamGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_Ipams_IpamPUTRequest  # type: ignore

class ClusterSdnIpamsEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/sdn/ipams/{ipam}
    """



    async def delete(self, params: Cluster_Sdn_Ipams_IpamDELETERequest | None = None) -> Any:
        """
        Delete sdn ipam object configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Sdn_Ipams_IpamGETRequest | None = None) -> Cluster_Sdn_Ipams_IpamGETResponse:
        """
        Read sdn ipam configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Sdn_Ipams_IpamPUTRequest | None = None) -> Any:
        """
        Update sdn ipam object configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

