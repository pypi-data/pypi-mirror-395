"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_VncproxyPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_VncproxyPOSTResponse  # type: ignore

class NodesLxcVncproxyEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/vncproxy
    """



    async def vncproxy(self, params: Nodes_Node_Lxc_Vmid_VncproxyPOSTRequest | None = None) -> Nodes_Node_Lxc_Vmid_VncproxyPOSTResponse:
        """
        Creates a TCP VNC proxy connections.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

