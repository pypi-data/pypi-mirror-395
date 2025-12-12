"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Disks_Lvm_NameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Disks_Lvm_NameDELETEResponse  # type: ignore

class NodesDisksLvmEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/lvm/{name}
    """



    async def delete(self, params: Nodes_Node_Disks_Lvm_NameDELETERequest | None = None) -> Nodes_Node_Disks_Lvm_NameDELETEResponse:
        """
        Remove an LVM Volume Group.

        HTTP Method: DELETE
        """
        return await self._delete()

