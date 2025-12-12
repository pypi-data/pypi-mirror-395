"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_SendkeyPUTRequest  # type: ignore

class NodesQemuSendkeyEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/sendkey
    """



    async def vm_sendkey(self, params: Nodes_Node_Qemu_Vmid_SendkeyPUTRequest | None = None) -> Any:
        """
        Send key event to virtual machine.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

