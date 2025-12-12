"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_PingPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_PingPOSTResponse  # type: ignore

class NodesQemuAgentPingEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/ping
    """



    async def ping(self, params: Nodes_Node_Qemu_Vmid_Agent_PingPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_PingPOSTResponse:
        """
        Execute ping.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

