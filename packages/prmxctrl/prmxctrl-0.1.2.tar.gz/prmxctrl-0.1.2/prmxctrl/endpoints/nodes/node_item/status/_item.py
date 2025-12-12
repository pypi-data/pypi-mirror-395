"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_StatusGETRequest
from prmxctrl.models.nodes import Nodes_Node_StatusGETResponse
from prmxctrl.models.nodes import Nodes_Node_StatusPOSTRequest  # type: ignore

class NodesStatusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/status
    """



    async def get(self, params: Nodes_Node_StatusGETRequest | None = None) -> Nodes_Node_StatusGETResponse:
        """
        Read node status

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def node_cmd(self, params: Nodes_Node_StatusPOSTRequest | None = None) -> Any:
        """
        Reboot or shutdown a node.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

