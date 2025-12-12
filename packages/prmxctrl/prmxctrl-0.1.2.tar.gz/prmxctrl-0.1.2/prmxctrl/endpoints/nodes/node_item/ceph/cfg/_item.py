"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .raw._item import NodesCephCfgRawEndpoints
from .db._item import NodesCephCfgDbEndpoints
from prmxctrl.models.nodes import Nodes_Node_Ceph_CfgGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_CfgGETResponse  # type: ignore

class NodesCephCfgEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/cfg
    """

    # Sub-endpoint properties
    @property
    def raw(self) -> NodesCephCfgRawEndpoints:
        """Access raw endpoints"""
        from .raw._item import NodesCephCfgRawEndpoints  # type: ignore
        return NodesCephCfgRawEndpoints(self._client, self._build_path("raw"))
    @property
    def db(self) -> NodesCephCfgDbEndpoints:
        """Access db endpoints"""
        from .db._item import NodesCephCfgDbEndpoints  # type: ignore
        return NodesCephCfgDbEndpoints(self._client, self._build_path("db"))



    async def list(self, params: Nodes_Node_Ceph_CfgGETRequest | None = None) -> Nodes_Node_Ceph_CfgGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

