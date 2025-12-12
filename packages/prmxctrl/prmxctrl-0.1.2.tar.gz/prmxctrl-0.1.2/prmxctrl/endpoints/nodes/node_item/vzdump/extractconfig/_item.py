"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Vzdump_ExtractconfigGETRequest
from prmxctrl.models.nodes import Nodes_Node_Vzdump_ExtractconfigGETResponse  # type: ignore

class NodesVzdumpExtractconfigEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/vzdump/extractconfig
    """



    async def get(self, params: Nodes_Node_Vzdump_ExtractconfigGETRequest | None = None) -> Nodes_Node_Vzdump_ExtractconfigGETResponse:
        """
        Extract configuration from vzdump backup archive.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

