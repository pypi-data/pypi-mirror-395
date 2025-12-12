"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_SpiceshellPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_SpiceshellPOSTResponse  # type: ignore

class NodesSpiceshellEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/spiceshell
    """



    async def spiceshell(self, params: Nodes_Node_SpiceshellPOSTRequest | None = None) -> Nodes_Node_SpiceshellPOSTResponse:
        """
        Creates a SPICE shell.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

