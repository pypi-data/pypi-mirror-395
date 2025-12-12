"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_StopPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_StopPOSTResponse  # type: ignore

class NodesQemuStatusStopEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/status/stop
    """



    async def vm_stop(self, params: Nodes_Node_Qemu_Vmid_Status_StopPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Status_StopPOSTResponse:
        """
        Stop virtual machine. The qemu process will exit immediately. Thisis akin to pulling the power plug of a running computer and may damage the VM data

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

