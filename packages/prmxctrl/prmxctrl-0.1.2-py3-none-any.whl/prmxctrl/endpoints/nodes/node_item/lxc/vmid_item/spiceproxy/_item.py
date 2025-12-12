"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_SpiceproxyPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_SpiceproxyPOSTResponse  # type: ignore

class NodesLxcSpiceproxyEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/spiceproxy
    """



    async def spiceproxy(self, params: Nodes_Node_Lxc_Vmid_SpiceproxyPOSTRequest | None = None) -> Nodes_Node_Lxc_Vmid_SpiceproxyPOSTResponse:
        """
        Returns a SPICE configuration to connect to the CT.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

