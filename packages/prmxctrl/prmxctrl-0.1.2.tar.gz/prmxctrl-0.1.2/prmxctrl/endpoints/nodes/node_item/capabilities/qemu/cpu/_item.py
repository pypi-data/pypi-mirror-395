"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Capabilities_Qemu_CpuGETRequest
from prmxctrl.models.nodes import Nodes_Node_Capabilities_Qemu_CpuGETResponse  # type: ignore

class NodesCapabilitiesQemuCpuEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/capabilities/qemu/cpu
    """



    async def list(self, params: Nodes_Node_Capabilities_Qemu_CpuGETRequest | None = None) -> Nodes_Node_Capabilities_Qemu_CpuGETResponse:
        """
        List all custom and default CPU models.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

