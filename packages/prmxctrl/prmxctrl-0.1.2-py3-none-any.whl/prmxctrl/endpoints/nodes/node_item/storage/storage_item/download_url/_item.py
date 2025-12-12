"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Download_UrlPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Download_UrlPOSTResponse  # type: ignore

class NodesStorageDownload_UrlEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/download-url
    """



    async def download_url(self, params: Nodes_Node_Storage_Storage_Download_UrlPOSTRequest | None = None) -> Nodes_Node_Storage_Storage_Download_UrlPOSTResponse:
        """
        Download templates and ISO images by using an URL.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

