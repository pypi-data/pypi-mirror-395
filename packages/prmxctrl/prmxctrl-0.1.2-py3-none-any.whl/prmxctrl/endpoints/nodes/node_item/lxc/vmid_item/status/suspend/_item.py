"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Status_SuspendPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Status_SuspendPOSTResponse  # type: ignore

class NodesLxcStatusSuspendEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/status/suspend
    """



    async def vm_suspend(self, params: Nodes_Node_Lxc_Vmid_Status_SuspendPOSTRequest | None = None) -> Nodes_Node_Lxc_Vmid_Status_SuspendPOSTResponse:
        """
        Suspend the container. This is experimental.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

