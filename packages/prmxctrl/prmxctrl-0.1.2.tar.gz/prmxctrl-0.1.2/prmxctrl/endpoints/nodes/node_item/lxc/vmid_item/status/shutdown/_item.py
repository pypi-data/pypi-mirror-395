"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Status_ShutdownPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Status_ShutdownPOSTResponse  # type: ignore

class NodesLxcStatusShutdownEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/status/shutdown
    """



    async def vm_shutdown(self, params: Nodes_Node_Lxc_Vmid_Status_ShutdownPOSTRequest | None = None) -> Nodes_Node_Lxc_Vmid_Status_ShutdownPOSTResponse:
        """
        Shutdown the container. This will trigger a clean shutdown of the container, see lxc-stop(1) for details.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

