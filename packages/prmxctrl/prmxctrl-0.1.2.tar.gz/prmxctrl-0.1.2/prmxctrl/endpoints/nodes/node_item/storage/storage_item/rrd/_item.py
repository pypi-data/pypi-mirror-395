"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_RrdGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_RrdGETResponse  # type: ignore

class NodesStorageRrdEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/rrd
    """



    async def get(self, params: Nodes_Node_Storage_Storage_RrdGETRequest | None = None) -> Nodes_Node_Storage_Storage_RrdGETResponse:
        """
        Read storage RRD statistics (returns PNG).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

