"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_ExecutePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_ExecutePOSTResponse  # type: ignore

class NodesExecuteEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/execute
    """



    async def execute(self, params: Nodes_Node_ExecutePOSTRequest | None = None) -> Nodes_Node_ExecutePOSTResponse:
        """
        Execute multiple commands in order.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

