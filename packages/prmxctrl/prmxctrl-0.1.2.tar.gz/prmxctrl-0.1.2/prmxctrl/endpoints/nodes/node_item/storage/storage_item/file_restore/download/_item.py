"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_File_Restore_DownloadGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_File_Restore_DownloadGETResponse  # type: ignore

class NodesStorageFile_RestoreDownloadEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/file-restore/download
    """



    async def get(self, params: Nodes_Node_Storage_Storage_File_Restore_DownloadGETRequest | None = None) -> Nodes_Node_Storage_Storage_File_Restore_DownloadGETResponse:
        """
        Extract a file or directory (as zip archive) from a PBS backup.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

