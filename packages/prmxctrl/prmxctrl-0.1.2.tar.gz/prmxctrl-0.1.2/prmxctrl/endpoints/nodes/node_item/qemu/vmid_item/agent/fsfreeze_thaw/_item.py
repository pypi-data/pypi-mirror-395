"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_ThawPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_ThawPOSTResponse  # type: ignore

class NodesQemuAgentFsfreeze_ThawEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-thaw
    """



    async def fsfreeze_thaw(self, params: Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_ThawPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_ThawPOSTResponse:
        """
        Execute fsfreeze-thaw.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

