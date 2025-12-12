"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesDisksLvmEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmGETRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmGETResponse
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmPOSTResponse  # type: ignore

class NodesDisksLvmEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/lvm
    """


    def __call__(self, name: str) -> NodesDisksLvmEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesDisksLvmEndpoints1  # type: ignore
        return NodesDisksLvmEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def get(self, params: Nodes_Node_Disks_LvmGETRequest | None = None) -> Nodes_Node_Disks_LvmGETResponse:
        """
        List LVM Volume Groups

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Nodes_Node_Disks_LvmPOSTRequest | None = None) -> Nodes_Node_Disks_LvmPOSTResponse:
        """
        Create an LVM Volume Group

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

