"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_StatusGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_StatusGETResponse  # type: ignore

class NodesStorageStatusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/status
    """



    async def get(self, params: Nodes_Node_Storage_Storage_StatusGETRequest | None = None) -> Nodes_Node_Storage_Storage_StatusGETResponse:
        """
        Read storage status.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

