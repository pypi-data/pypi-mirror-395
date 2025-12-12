"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Move_VolumePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Move_VolumePOSTResponse  # type: ignore

class NodesLxcMove_VolumeEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/move_volume
    """



    async def move_volume(self, params: Nodes_Node_Lxc_Vmid_Move_VolumePOSTRequest | None = None) -> Nodes_Node_Lxc_Vmid_Move_VolumePOSTResponse:
        """
        Move a rootfs-/mp-volume to a different storage or to a different container.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

