"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_StatusPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_StatusPOSTResponse  # type: ignore

class NodesQemuAgentFsfreeze_StatusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-status
    """



    async def fsfreeze_status(self, params: Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_StatusPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_StatusPOSTResponse:
        """
        Execute fsfreeze-status.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

