"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Get_Memory_BlocksGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Get_Memory_BlocksGETResponse  # type: ignore

class NodesQemuAgentGet_Memory_BlocksEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/get-memory-blocks
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_Agent_Get_Memory_BlocksGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Get_Memory_BlocksGETResponse:
        """
        Execute get-memory-blocks.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

