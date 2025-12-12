"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesCephMdsEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Ceph_MdsGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_MdsGETResponse  # type: ignore

class NodesCephMdsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/mds
    """


    def __call__(self, name: str) -> NodesCephMdsEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesCephMdsEndpoints1  # type: ignore
        return NodesCephMdsEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Ceph_MdsGETRequest | None = None) -> Nodes_Node_Ceph_MdsGETResponse:
        """
        MDS directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

