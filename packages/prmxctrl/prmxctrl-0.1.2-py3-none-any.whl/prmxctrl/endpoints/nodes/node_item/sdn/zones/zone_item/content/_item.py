"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Sdn_Zones_Zone_ContentGETRequest
from prmxctrl.models.nodes import Nodes_Node_Sdn_Zones_Zone_ContentGETResponse  # type: ignore

class NodesSdnZonesContentEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/sdn/zones/{zone}/content
    """



    async def list(self, params: Nodes_Node_Sdn_Zones_Zone_ContentGETRequest | None = None) -> Nodes_Node_Sdn_Zones_Zone_ContentGETResponse:
        """
        List zone content.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

