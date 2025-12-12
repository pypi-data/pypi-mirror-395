"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_ExecPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_ExecPOSTResponse  # type: ignore

class NodesQemuAgentExecEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/exec
    """



    async def exec(self, params: Nodes_Node_Qemu_Vmid_Agent_ExecPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_ExecPOSTResponse:
        """
        Executes the given command in the vm via the guest-agent and returns an object with the pid.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

