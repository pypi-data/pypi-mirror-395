"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .id_item._item import ClusterMetricsServerEndpoints1
from prmxctrl.models.cluster import Cluster_Metrics_ServerGETResponse  # type: ignore

class ClusterMetricsServerEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/metrics/server
    """


    def __call__(self, id: int) -> ClusterMetricsServerEndpoints1:
        """Access specific id"""
        from .id_item._item import ClusterMetricsServerEndpoints1  # type: ignore
        return ClusterMetricsServerEndpoints1(
            self._client,
            self._build_path(str(id))
        )


    async def list(self, ) -> Cluster_Metrics_ServerGETResponse:
        """
        List configured metric servers.

        HTTP Method: GET
        """
        return await self._get()

