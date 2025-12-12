"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_ResetPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_ResetPOSTResponse  # type: ignore

class NodesQemuStatusResetEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/status/reset
    """



    async def vm_reset(self, params: Nodes_Node_Qemu_Vmid_Status_ResetPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Status_ResetPOSTResponse:
        """
        Reset virtual machine.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

