"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_ClonePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_ClonePOSTResponse  # type: ignore

class NodesQemuCloneEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/clone
    """



    async def clone_vm(self, params: Nodes_Node_Qemu_Vmid_ClonePOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_ClonePOSTResponse:
        """
        Create a copy of virtual machine/template.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

