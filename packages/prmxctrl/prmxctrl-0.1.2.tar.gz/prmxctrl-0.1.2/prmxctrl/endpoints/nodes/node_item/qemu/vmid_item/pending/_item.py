"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_PendingGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_PendingGETResponse  # type: ignore

class NodesQemuPendingEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/pending
    """



    async def list(self, params: Nodes_Node_Qemu_Vmid_PendingGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_PendingGETResponse:
        """
        Get the virtual machine configuration with both current and pending values.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

