"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..sdn.vnets import ClusterSdnVnetsEndpoints
from ..sdn.zones import ClusterSdnZonesEndpoints
from ..sdn.controllers import ClusterSdnControllersEndpoints
from ..sdn.ipams import ClusterSdnIpamsEndpoints
from ..sdn.dns import ClusterSdnDnsEndpoints
from prmxctrl.models.cluster import Cluster_SdnGETResponse
from prmxctrl.models.cluster import Cluster_SdnPUTResponse  # type: ignore

class ClusterSdnEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/sdn
    """

    # Sub-endpoint properties
    @property
    def vnets(self) -> ClusterSdnVnetsEndpoints:
        """Access vnets endpoints"""
        from ..sdn.vnets import ClusterSdnVnetsEndpoints  # type: ignore
        return ClusterSdnVnetsEndpoints(self._client, self._build_path("vnets"))
    @property
    def zones(self) -> ClusterSdnZonesEndpoints:
        """Access zones endpoints"""
        from ..sdn.zones import ClusterSdnZonesEndpoints  # type: ignore
        return ClusterSdnZonesEndpoints(self._client, self._build_path("zones"))
    @property
    def controllers(self) -> ClusterSdnControllersEndpoints:
        """Access controllers endpoints"""
        from ..sdn.controllers import ClusterSdnControllersEndpoints  # type: ignore
        return ClusterSdnControllersEndpoints(self._client, self._build_path("controllers"))
    @property
    def ipams(self) -> ClusterSdnIpamsEndpoints:
        """Access ipams endpoints"""
        from ..sdn.ipams import ClusterSdnIpamsEndpoints  # type: ignore
        return ClusterSdnIpamsEndpoints(self._client, self._build_path("ipams"))
    @property
    def dns(self) -> ClusterSdnDnsEndpoints:
        """Access dns endpoints"""
        from ..sdn.dns import ClusterSdnDnsEndpoints  # type: ignore
        return ClusterSdnDnsEndpoints(self._client, self._build_path("dns"))



    async def list(self, ) -> Cluster_SdnGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get()

    async def reload(self, ) -> Cluster_SdnPUTResponse:
        """
        Apply sdn controller changes && reload.

        HTTP Method: PUT
        """
        return await self._put()

