"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_RebootPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_RebootPOSTResponse  # type: ignore

class NodesQemuStatusRebootEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/status/reboot
    """



    async def vm_reboot(self, params: Nodes_Node_Qemu_Vmid_Status_RebootPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Status_RebootPOSTResponse:
        """
        Reboot the VM by shutting it down, and starting it again. Applies pending changes.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

