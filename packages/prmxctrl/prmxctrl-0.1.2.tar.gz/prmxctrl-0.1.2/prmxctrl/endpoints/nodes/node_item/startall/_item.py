"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_StartallPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_StartallPOSTResponse  # type: ignore

class NodesStartallEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/startall
    """



    async def startall(self, params: Nodes_Node_StartallPOSTRequest | None = None) -> Nodes_Node_StartallPOSTResponse:
        """
        Start all VMs and containers located on this node (by default only those with onboot=1).

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

