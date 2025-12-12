"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Suspend_HybridPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Suspend_HybridPOSTResponse  # type: ignore

class NodesQemuAgentSuspend_HybridEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/suspend-hybrid
    """



    async def suspend_hybrid(self, params: Nodes_Node_Qemu_Vmid_Agent_Suspend_HybridPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Suspend_HybridPOSTResponse:
        """
        Execute suspend-hybrid.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

