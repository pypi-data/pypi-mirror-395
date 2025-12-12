"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_TasksGETResponse  # type: ignore

class ClusterTasksEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/tasks
    """



    async def list(self, ) -> Cluster_TasksGETResponse:
        """
        List recent tasks (cluster wide).

        HTTP Method: GET
        """
        return await self._get()

