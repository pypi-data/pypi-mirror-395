"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_File_ReadGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_File_ReadGETResponse  # type: ignore

class NodesQemuAgentFile_ReadEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/file-read
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_Agent_File_ReadGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_File_ReadGETResponse:
        """
        Reads the given file via guest agent. Is limited to 16777216 bytes.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

