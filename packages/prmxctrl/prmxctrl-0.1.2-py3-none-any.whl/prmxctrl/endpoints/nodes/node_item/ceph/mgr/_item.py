"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .id_item._item import NodesCephMgrEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Ceph_MgrGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_MgrGETResponse  # type: ignore

class NodesCephMgrEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/mgr
    """


    def __call__(self, id: int) -> NodesCephMgrEndpoints1:
        """Access specific id"""
        from .id_item._item import NodesCephMgrEndpoints1  # type: ignore
        return NodesCephMgrEndpoints1(
            self._client,
            self._build_path(str(id))
        )


    async def list(self, params: Nodes_Node_Ceph_MgrGETRequest | None = None) -> Nodes_Node_Ceph_MgrGETResponse:
        """
        MGR directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

