"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Disks_Lvmthin_NameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Disks_Lvmthin_NameDELETEResponse  # type: ignore

class NodesDisksLvmthinEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/lvmthin/{name}
    """



    async def delete(self, params: Nodes_Node_Disks_Lvmthin_NameDELETERequest | None = None) -> Nodes_Node_Disks_Lvmthin_NameDELETEResponse:
        """
        Remove an LVM thin pool.

        HTTP Method: DELETE
        """
        return await self._delete()

