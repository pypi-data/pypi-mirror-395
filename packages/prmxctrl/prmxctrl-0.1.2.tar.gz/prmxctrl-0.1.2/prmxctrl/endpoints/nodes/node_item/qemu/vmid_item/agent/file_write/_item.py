"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_File_WritePOSTRequest  # type: ignore

class NodesQemuAgentFile_WriteEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/file-write
    """



    async def file_write(self, params: Nodes_Node_Qemu_Vmid_Agent_File_WritePOSTRequest | None = None) -> Any:
        """
        Writes the given file via guest agent.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

