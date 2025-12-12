"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import ClusterGETResponse  # type: ignore

class ClusterEndpoints(EndpointBase):
    """
    Root endpoint class for cluster API endpoints.
    """



    async def list(self, ) -> ClusterGETResponse:
        """
        Cluster index.

        HTTP Method: GET
        """
        return await self._get()

