"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Suspend_RamPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Suspend_RamPOSTResponse  # type: ignore

class NodesQemuAgentSuspend_RamEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/suspend-ram
    """



    async def suspend_ram(self, params: Nodes_Node_Qemu_Vmid_Agent_Suspend_RamPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Suspend_RamPOSTResponse:
        """
        Execute suspend-ram.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

