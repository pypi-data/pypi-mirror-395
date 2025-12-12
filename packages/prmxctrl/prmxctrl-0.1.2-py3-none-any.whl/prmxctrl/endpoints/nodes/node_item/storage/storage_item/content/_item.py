"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .volume_item._item import NodesStorageContentEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_ContentGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_ContentGETResponse
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_ContentPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_ContentPOSTResponse  # type: ignore

class NodesStorageContentEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/content
    """


    def __call__(self, volume: str) -> NodesStorageContentEndpoints1:
        """Access specific volume"""
        from .volume_item._item import NodesStorageContentEndpoints1  # type: ignore
        return NodesStorageContentEndpoints1(
            self._client,
            self._build_path(str(volume))
        )


    async def list(self, params: Nodes_Node_Storage_Storage_ContentGETRequest | None = None) -> Nodes_Node_Storage_Storage_ContentGETResponse:
        """
        List storage content.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Nodes_Node_Storage_Storage_ContentPOSTRequest | None = None) -> Nodes_Node_Storage_Storage_ContentPOSTResponse:
        """
        Allocate disk images.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

