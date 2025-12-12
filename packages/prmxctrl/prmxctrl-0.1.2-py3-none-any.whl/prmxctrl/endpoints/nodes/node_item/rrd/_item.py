"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_RrdGETRequest
from prmxctrl.models.nodes import Nodes_Node_RrdGETResponse  # type: ignore

class NodesRrdEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/rrd
    """



    async def get(self, params: Nodes_Node_RrdGETRequest | None = None) -> Nodes_Node_RrdGETResponse:
        """
        Read node RRD statistics (returns PNG)

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

