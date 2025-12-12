"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..status.current import ClusterHaStatusCurrentEndpoints
from ..status.manager_status import ClusterHaStatusManager_StatusEndpoints
from prmxctrl.models.cluster import Cluster_Ha_StatusGETResponse  # type: ignore

class ClusterHaStatusEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha/status
    """

    # Sub-endpoint properties
    @property
    def current(self) -> ClusterHaStatusCurrentEndpoints:
        """Access current endpoints"""
        from ..status.current import ClusterHaStatusCurrentEndpoints  # type: ignore
        return ClusterHaStatusCurrentEndpoints(self._client, self._build_path("current"))
    @property
    def manager_status(self) -> ClusterHaStatusManager_StatusEndpoints:
        """Access manager_status endpoints"""
        from ..status.manager_status import ClusterHaStatusManager_StatusEndpoints  # type: ignore
        return ClusterHaStatusManager_StatusEndpoints(self._client, self._build_path("manager_status"))



    async def list(self, ) -> Cluster_Ha_StatusGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get()

