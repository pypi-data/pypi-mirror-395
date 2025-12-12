"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Get_VcpusGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Get_VcpusGETResponse  # type: ignore

class NodesQemuAgentGet_VcpusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/get-vcpus
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_Agent_Get_VcpusGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Get_VcpusGETResponse:
        """
        Execute get-vcpus.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

