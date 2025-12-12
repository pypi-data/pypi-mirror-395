"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_ResizePUTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_ResizePUTResponse  # type: ignore

class NodesLxcResizeEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/resize
    """



    async def resize_vm(self, params: Nodes_Node_Lxc_Vmid_ResizePUTRequest | None = None) -> Nodes_Node_Lxc_Vmid_ResizePUTResponse:
        """
        Resize a container mount point.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

