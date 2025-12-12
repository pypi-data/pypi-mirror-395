"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Capabilities_Qemu_MachinesGETRequest
from prmxctrl.models.nodes import Nodes_Node_Capabilities_Qemu_MachinesGETResponse  # type: ignore

class NodesCapabilitiesQemuMachinesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/capabilities/qemu/machines
    """



    async def list(self, params: Nodes_Node_Capabilities_Qemu_MachinesGETRequest | None = None) -> Nodes_Node_Capabilities_Qemu_MachinesGETResponse:
        """
        Get available QEMU/KVM machine types.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

