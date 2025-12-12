"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ha_Status_Manager_StatusGETResponse  # type: ignore

class ClusterHaStatusManager_StatusEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha/status/manager_status
    """



    async def get(self, ) -> Cluster_Ha_Status_Manager_StatusGETResponse:
        """
        Get full HA manger status, including LRM status.

        HTTP Method: GET
        """
        return await self._get()

