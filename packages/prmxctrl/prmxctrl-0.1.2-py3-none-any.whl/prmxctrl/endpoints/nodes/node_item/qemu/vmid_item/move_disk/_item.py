"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Move_DiskPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Move_DiskPOSTResponse  # type: ignore

class NodesQemuMove_DiskEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/move_disk
    """



    async def move_vm_disk(self, params: Nodes_Node_Qemu_Vmid_Move_DiskPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Move_DiskPOSTResponse:
        """
        Move volume to different storage or to a different VM.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

