"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_StopallPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_StopallPOSTResponse  # type: ignore

class NodesStopallEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/stopall
    """



    async def stopall(self, params: Nodes_Node_StopallPOSTRequest | None = None) -> Nodes_Node_StopallPOSTResponse:
        """
        Stop all VMs and Containers.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

