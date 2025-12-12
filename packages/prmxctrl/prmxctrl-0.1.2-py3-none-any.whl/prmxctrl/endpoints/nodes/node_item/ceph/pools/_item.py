"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesCephPoolsEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolsGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolsGETResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolsPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_PoolsPOSTResponse  # type: ignore

class NodesCephPoolsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/pools
    """


    def __call__(self, name: str) -> NodesCephPoolsEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesCephPoolsEndpoints1  # type: ignore
        return NodesCephPoolsEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Ceph_PoolsGETRequest | None = None) -> Nodes_Node_Ceph_PoolsGETResponse:
        """
        List all pools. Deprecated, please use `/nodes/{node}/ceph/pool`.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def createpool(self, params: Nodes_Node_Ceph_PoolsPOSTRequest | None = None) -> Nodes_Node_Ceph_PoolsPOSTResponse:
        """
        Create Ceph pool. Deprecated, please use `/nodes/{node}/ceph/pool`.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

