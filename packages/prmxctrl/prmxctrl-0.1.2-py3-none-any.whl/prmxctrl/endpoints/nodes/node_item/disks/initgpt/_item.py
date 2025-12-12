"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Disks_InitgptPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_InitgptPOSTResponse  # type: ignore

class NodesDisksInitgptEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/initgpt
    """



    async def initgpt(self, params: Nodes_Node_Disks_InitgptPOSTRequest | None = None) -> Nodes_Node_Disks_InitgptPOSTResponse:
        """
        Initialize Disk with GPT

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

