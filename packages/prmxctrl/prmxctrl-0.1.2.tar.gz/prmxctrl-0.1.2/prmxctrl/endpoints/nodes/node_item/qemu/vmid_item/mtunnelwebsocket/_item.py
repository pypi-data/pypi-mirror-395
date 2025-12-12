"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_MtunnelwebsocketGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_MtunnelwebsocketGETResponse  # type: ignore

class NodesQemuMtunnelwebsocketEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/mtunnelwebsocket
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_MtunnelwebsocketGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_MtunnelwebsocketGETResponse:
        """
        Migration tunnel endpoint for websocket upgrade - only for internal use by VM migration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

