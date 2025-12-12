"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_FstrimPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_FstrimPOSTResponse  # type: ignore

class NodesQemuAgentFstrimEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/fstrim
    """



    async def fstrim(self, params: Nodes_Node_Qemu_Vmid_Agent_FstrimPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_FstrimPOSTResponse:
        """
        Execute fstrim.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

