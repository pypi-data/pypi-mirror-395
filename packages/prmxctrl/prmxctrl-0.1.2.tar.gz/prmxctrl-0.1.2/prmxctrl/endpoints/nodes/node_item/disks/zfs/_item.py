"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesDisksZfsEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Disks_ZfsGETRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_ZfsGETResponse
from prmxctrl.models.nodes import Nodes_Node_Disks_ZfsPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_ZfsPOSTResponse  # type: ignore

class NodesDisksZfsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/zfs
    """


    def __call__(self, name: str) -> NodesDisksZfsEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesDisksZfsEndpoints1  # type: ignore
        return NodesDisksZfsEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Disks_ZfsGETRequest | None = None) -> Nodes_Node_Disks_ZfsGETResponse:
        """
        List Zpools.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Nodes_Node_Disks_ZfsPOSTRequest | None = None) -> Nodes_Node_Disks_ZfsPOSTResponse:
        """
        Create a ZFS pool.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

