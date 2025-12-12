"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .status._item import NodesCephPoolStatusEndpoints
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pool_NameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pool_NameDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pool_NameGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pool_NameGETResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pool_NamePUTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pool_NamePUTResponse  # type: ignore

class NodesCephPoolEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/pool/{name}
    """

    # Sub-endpoint properties
    @property
    def status(self) -> NodesCephPoolStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesCephPoolStatusEndpoints  # type: ignore
        return NodesCephPoolStatusEndpoints(self._client, self._build_path("status"))



    async def delete(self, params: Nodes_Node_Ceph_Pool_NameDELETERequest | None = None) -> Nodes_Node_Ceph_Pool_NameDELETEResponse:
        """
        Destroy pool

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Ceph_Pool_NameGETRequest | None = None) -> Nodes_Node_Ceph_Pool_NameGETResponse:
        """
        Pool index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def setpool(self, params: Nodes_Node_Ceph_Pool_NamePUTRequest | None = None) -> Nodes_Node_Ceph_Pool_NamePUTResponse:
        """
        Change POOL settings

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

