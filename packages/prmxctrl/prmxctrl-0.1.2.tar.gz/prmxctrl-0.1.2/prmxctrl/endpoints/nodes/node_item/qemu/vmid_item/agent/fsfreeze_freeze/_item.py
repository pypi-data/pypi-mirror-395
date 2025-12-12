"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_FreezePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_FreezePOSTResponse  # type: ignore

class NodesQemuAgentFsfreeze_FreezeEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-freeze
    """



    async def fsfreeze_freeze(self, params: Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_FreezePOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_FreezePOSTResponse:
        """
        Execute fsfreeze-freeze.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

