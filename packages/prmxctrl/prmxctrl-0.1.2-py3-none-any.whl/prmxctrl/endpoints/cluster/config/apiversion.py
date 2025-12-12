"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Config_ApiversionGETResponse  # type: ignore

class ClusterConfigApiversionEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/config/apiversion
    """



    async def get(self, ) -> Cluster_Config_ApiversionGETResponse:
        """
        Return the version of the cluster join API available on this node.

        HTTP Method: GET
        """
        return await self._get()

