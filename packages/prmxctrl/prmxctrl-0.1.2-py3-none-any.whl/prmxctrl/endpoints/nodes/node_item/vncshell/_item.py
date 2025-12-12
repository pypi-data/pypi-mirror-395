"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_VncshellPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_VncshellPOSTResponse  # type: ignore

class NodesVncshellEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/vncshell
    """



    async def vncshell(self, params: Nodes_Node_VncshellPOSTRequest | None = None) -> Nodes_Node_VncshellPOSTResponse:
        """
        Creates a VNC Shell proxy.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

