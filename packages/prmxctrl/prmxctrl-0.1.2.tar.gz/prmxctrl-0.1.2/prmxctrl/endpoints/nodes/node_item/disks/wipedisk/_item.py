"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Disks_WipediskPUTRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_WipediskPUTResponse  # type: ignore

class NodesDisksWipediskEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/wipedisk
    """



    async def wipe_disk(self, params: Nodes_Node_Disks_WipediskPUTRequest | None = None) -> Nodes_Node_Disks_WipediskPUTResponse:
        """
        Wipe a disk or partition.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

