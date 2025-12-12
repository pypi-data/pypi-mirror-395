"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesDisksLvmthinEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmthinGETRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmthinGETResponse
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmthinPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_LvmthinPOSTResponse  # type: ignore

class NodesDisksLvmthinEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/lvmthin
    """


    def __call__(self, name: str) -> NodesDisksLvmthinEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesDisksLvmthinEndpoints1  # type: ignore
        return NodesDisksLvmthinEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Disks_LvmthinGETRequest | None = None) -> Nodes_Node_Disks_LvmthinGETResponse:
        """
        List LVM thinpools

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Nodes_Node_Disks_LvmthinPOSTRequest | None = None) -> Nodes_Node_Disks_LvmthinPOSTResponse:
        """
        Create an LVM thinpool

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

