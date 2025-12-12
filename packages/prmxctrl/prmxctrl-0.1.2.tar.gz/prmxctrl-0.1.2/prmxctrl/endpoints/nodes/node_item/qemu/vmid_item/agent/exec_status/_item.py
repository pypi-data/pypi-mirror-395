"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Exec_StatusGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Exec_StatusGETResponse  # type: ignore

class NodesQemuAgentExec_StatusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/exec-status
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_Agent_Exec_StatusGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Exec_StatusGETResponse:
        """
        Gets the status of the given pid started by the guest-agent

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

