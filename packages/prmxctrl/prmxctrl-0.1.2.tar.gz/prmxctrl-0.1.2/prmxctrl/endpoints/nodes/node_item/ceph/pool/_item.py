"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesCephPoolEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolGETResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolPOSTResponse  # type: ignore

class NodesCephPoolEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/pool
    """


    def __call__(self, name: str) -> NodesCephPoolEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesCephPoolEndpoints1  # type: ignore
        return NodesCephPoolEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Ceph_PoolGETRequest | None = None) -> Nodes_Node_Ceph_PoolGETResponse:
        """
        List all pools and their settings (which are settable by the POST/PUT endpoints).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def createpool(self, params: Nodes_Node_Ceph_PoolPOSTRequest | None = None) -> Nodes_Node_Ceph_PoolPOSTResponse:
        """
        Create Ceph pool

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

