"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Disks_Zfs_NameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Disks_Zfs_NameDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Disks_Zfs_NameGETRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_Zfs_NameGETResponse  # type: ignore

class NodesDisksZfsEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/zfs/{name}
    """



    async def delete(self, params: Nodes_Node_Disks_Zfs_NameDELETERequest | None = None) -> Nodes_Node_Disks_Zfs_NameDELETEResponse:
        """
        Destroy a ZFS pool.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Nodes_Node_Disks_Zfs_NameGETRequest | None = None) -> Nodes_Node_Disks_Zfs_NameGETResponse:
        """
        Get details about a zpool.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

