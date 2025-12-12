"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Config_TotemGETResponse  # type: ignore

class ClusterConfigTotemEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/config/totem
    """



    async def get(self, ) -> Cluster_Config_TotemGETResponse:
        """
        Get corosync totem protocol settings.

        HTTP Method: GET
        """
        return await self._get()

