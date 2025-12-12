"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_RrddataGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_RrddataGETResponse  # type: ignore

class NodesStorageRrddataEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/rrddata
    """



    async def list(self, params: Nodes_Node_Storage_Storage_RrddataGETRequest | None = None) -> Nodes_Node_Storage_Storage_RrddataGETResponse:
        """
        Read storage RRD statistics.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

