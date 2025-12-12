"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_PendingGETRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_PendingGETResponse  # type: ignore

class NodesLxcPendingEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/pending
    """



    async def list(self, params: Nodes_Node_Lxc_Vmid_PendingGETRequest | None = None) -> Nodes_Node_Lxc_Vmid_PendingGETResponse:
        """
        Get container configuration, including pending changes.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

