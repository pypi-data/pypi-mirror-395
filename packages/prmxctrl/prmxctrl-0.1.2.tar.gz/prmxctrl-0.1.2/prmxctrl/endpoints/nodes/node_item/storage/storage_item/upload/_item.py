"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_UploadPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_UploadPOSTResponse  # type: ignore

class NodesStorageUploadEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/upload
    """



    async def upload(self, params: Nodes_Node_Storage_Storage_UploadPOSTRequest | None = None) -> Nodes_Node_Storage_Storage_UploadPOSTResponse:
        """
        Upload templates and ISO images.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

