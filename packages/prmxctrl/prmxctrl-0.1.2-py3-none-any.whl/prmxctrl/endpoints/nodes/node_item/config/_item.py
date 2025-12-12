"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_ConfigGETRequest
from prmxctrl.models.nodes import Nodes_Node_ConfigGETResponse
from prmxctrl.models.nodes import Nodes_Node_ConfigPUTRequest  # type: ignore

class NodesConfigEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/config
    """



    async def get(self, params: Nodes_Node_ConfigGETRequest | None = None) -> Nodes_Node_ConfigGETResponse:
        """
        Get node configuration options.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def set_options(self, params: Nodes_Node_ConfigPUTRequest | None = None) -> Any:
        """
        Set node configuration options.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

