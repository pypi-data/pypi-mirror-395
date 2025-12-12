"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .monid_item._item import NodesCephMonEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Ceph_MonGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_MonGETResponse  # type: ignore

class NodesCephMonEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/mon
    """


    def __call__(self, monid: int) -> NodesCephMonEndpoints1:
        """Access specific monid"""
        from .monid_item._item import NodesCephMonEndpoints1  # type: ignore
        return NodesCephMonEndpoints1(
            self._client,
            self._build_path(str(monid))
        )


    async def list(self, params: Nodes_Node_Ceph_MonGETRequest | None = None) -> Nodes_Node_Ceph_MonGETResponse:
        """
        Get Ceph monitor list.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

