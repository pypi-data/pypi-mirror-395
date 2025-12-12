"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..metrics.server import ClusterMetricsServerEndpoints
from prmxctrl.models.cluster import Cluster_MetricsGETResponse  # type: ignore

class ClusterMetricsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/metrics
    """

    # Sub-endpoint properties
    @property
    def server(self) -> ClusterMetricsServerEndpoints:
        """Access server endpoints"""
        from ..metrics.server import ClusterMetricsServerEndpoints  # type: ignore
        return ClusterMetricsServerEndpoints(self._client, self._build_path("server"))



    async def list(self, ) -> Cluster_MetricsGETResponse:
        """
        Metrics index.

        HTTP Method: GET
        """
        return await self._get()

