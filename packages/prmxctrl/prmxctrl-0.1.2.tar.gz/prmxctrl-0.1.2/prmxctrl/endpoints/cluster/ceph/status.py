"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ceph_StatusGETResponse  # type: ignore

class ClusterCephStatusEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ceph/status
    """



    async def get(self, ) -> Cluster_Ceph_StatusGETResponse:
        """
        Get ceph status.

        HTTP Method: GET
        """
        return await self._get()

