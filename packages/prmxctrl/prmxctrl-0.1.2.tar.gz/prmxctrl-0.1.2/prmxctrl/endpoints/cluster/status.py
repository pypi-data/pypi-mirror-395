"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_StatusGETResponse  # type: ignore

class ClusterStatusEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/status
    """



    async def list(self, ) -> Cluster_StatusGETResponse:
        """
        Get cluster status information.

        HTTP Method: GET
        """
        return await self._get()

