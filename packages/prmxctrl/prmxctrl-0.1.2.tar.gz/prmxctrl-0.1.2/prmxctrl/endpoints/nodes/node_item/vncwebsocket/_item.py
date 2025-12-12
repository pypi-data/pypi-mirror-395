"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_VncwebsocketGETRequest
from prmxctrl.models.nodes import Nodes_Node_VncwebsocketGETResponse  # type: ignore

class NodesVncwebsocketEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/vncwebsocket
    """



    async def get(self, params: Nodes_Node_VncwebsocketGETRequest | None = None) -> Nodes_Node_VncwebsocketGETResponse:
        """
        Opens a websocket for VNC traffic.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

