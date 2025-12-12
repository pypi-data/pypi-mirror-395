"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_TermproxyPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_TermproxyPOSTResponse  # type: ignore

class NodesTermproxyEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/termproxy
    """



    async def termproxy(self, params: Nodes_Node_TermproxyPOSTRequest | None = None) -> Nodes_Node_TermproxyPOSTResponse:
        """
        Creates a VNC Shell proxy.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

