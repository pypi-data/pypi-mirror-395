"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_MtunnelPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_MtunnelPOSTResponse  # type: ignore

class NodesLxcMtunnelEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/mtunnel
    """



    async def mtunnel(self, params: Nodes_Node_Lxc_Vmid_MtunnelPOSTRequest | None = None) -> Nodes_Node_Lxc_Vmid_MtunnelPOSTResponse:
        """
        Migration tunnel endpoint - only for internal use by CT migration.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

