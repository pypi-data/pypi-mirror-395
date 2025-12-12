"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_File_Restore_ListGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_File_Restore_ListGETResponse  # type: ignore

class NodesStorageFile_RestoreListEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/file-restore/list
    """



    async def list(self, params: Nodes_Node_Storage_Storage_File_Restore_ListGETRequest | None = None) -> Nodes_Node_Storage_Storage_File_Restore_ListGETResponse:
        """
        List files and directories for single file restore under the given path.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

