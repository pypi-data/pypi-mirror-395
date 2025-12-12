"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_WakeonlanPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_WakeonlanPOSTResponse  # type: ignore

class NodesWakeonlanEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/wakeonlan
    """



    async def wakeonlan(self, params: Nodes_Node_WakeonlanPOSTRequest | None = None) -> Nodes_Node_WakeonlanPOSTResponse:
        """
        Try to wake a node via 'wake on LAN' network packet.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

