"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Vzdump_DefaultsGETRequest
from prmxctrl.models.nodes import Nodes_Node_Vzdump_DefaultsGETResponse  # type: ignore

class NodesVzdumpDefaultsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/vzdump/defaults
    """



    async def get(self, params: Nodes_Node_Vzdump_DefaultsGETRequest | None = None) -> Nodes_Node_Vzdump_DefaultsGETResponse:
        """
        Get the currently configured vzdump defaults.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

