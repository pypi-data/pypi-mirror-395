"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Config_QdeviceGETResponse  # type: ignore

class ClusterConfigQdeviceEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/config/qdevice
    """



    async def get(self, ) -> Cluster_Config_QdeviceGETResponse:
        """
        Get QDevice status

        HTTP Method: GET
        """
        return await self._get()

