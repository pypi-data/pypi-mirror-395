"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_ShutdownPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Status_ShutdownPOSTResponse  # type: ignore

class NodesQemuStatusShutdownEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/status/shutdown
    """



    async def vm_shutdown(self, params: Nodes_Node_Qemu_Vmid_Status_ShutdownPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Status_ShutdownPOSTResponse:
        """
        Shutdown virtual machine. This is similar to pressing the power button on a physical machine.This will send an ACPI event for the guest OS, which should then proceed to a clean shutdown.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

