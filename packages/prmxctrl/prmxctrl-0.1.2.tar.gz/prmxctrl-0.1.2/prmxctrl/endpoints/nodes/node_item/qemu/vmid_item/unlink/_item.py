"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_UnlinkPUTRequest  # type: ignore

class NodesQemuUnlinkEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/unlink
    """



    async def unlink(self, params: Nodes_Node_Qemu_Vmid_UnlinkPUTRequest | None = None) -> Any:
        """
        Unlink/delete disk images.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

