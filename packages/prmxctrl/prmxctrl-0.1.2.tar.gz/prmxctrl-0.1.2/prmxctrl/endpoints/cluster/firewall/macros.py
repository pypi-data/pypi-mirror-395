"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Firewall_MacrosGETResponse  # type: ignore

class ClusterFirewallMacrosEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall/macros
    """



    async def list(self, ) -> Cluster_Firewall_MacrosGETResponse:
        """
        List available macros

        HTTP Method: GET
        """
        return await self._get()

