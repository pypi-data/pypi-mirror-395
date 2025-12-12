"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .storage_item._item import NodesStorageEndpoints1
from prmxctrl.models.nodes import Nodes_Node_StorageGETRequest
from prmxctrl.models.nodes import Nodes_Node_StorageGETResponse  # type: ignore

class NodesStorageEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage
    """


    def __call__(self, storage: str) -> NodesStorageEndpoints1:
        """Access specific storage"""
        from .storage_item._item import NodesStorageEndpoints1  # type: ignore
        return NodesStorageEndpoints1(
            self._client,
            self._build_path(str(storage))
        )


    async def list(self, params: Nodes_Node_StorageGETRequest | None = None) -> Nodes_Node_StorageGETResponse:
        """
        Get status for all datastores.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

