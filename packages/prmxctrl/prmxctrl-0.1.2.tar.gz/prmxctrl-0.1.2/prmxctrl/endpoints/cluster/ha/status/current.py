"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ha_Status_CurrentGETResponse  # type: ignore

class ClusterHaStatusCurrentEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha/status/current
    """



    async def list(self, ) -> Cluster_Ha_Status_CurrentGETResponse:
        """
        Get HA manger status.

        HTTP Method: GET
        """
        return await self._get()

