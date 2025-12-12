"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Firewall_RefsGETRequest
from prmxctrl.models.cluster import Cluster_Firewall_RefsGETResponse  # type: ignore

class ClusterFirewallRefsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall/refs
    """



    async def list(self, params: Cluster_Firewall_RefsGETRequest | None = None) -> Cluster_Firewall_RefsGETResponse:
        """
        Lists possible IPSet/Alias reference which are allowed in source/dest properties.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

