"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Get_Host_NameGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Get_Host_NameGETResponse  # type: ignore

class NodesQemuAgentGet_Host_NameEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/get-host-name
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_Agent_Get_Host_NameGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Get_Host_NameGETResponse:
        """
        Execute get-host-name.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

