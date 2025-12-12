"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pools_NameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pools_NameDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pools_NameGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pools_NameGETResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pools_NamePUTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Pools_NamePUTResponse  # type: ignore

class NodesCephPoolsEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/pools/{name}
    """



    async def delete(self, params: Nodes_Node_Ceph_Pools_NameDELETERequest | None = None) -> Nodes_Node_Ceph_Pools_NameDELETEResponse:
        """
        Destroy pool. Deprecated, please use `/nodes/{node}/ceph/pool/{name}`.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Nodes_Node_Ceph_Pools_NameGETRequest | None = None) -> Nodes_Node_Ceph_Pools_NameGETResponse:
        """
        List pool settings. Deprecated, please use `/nodes/{node}/ceph/pool/{pool}/status`.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def setpool(self, params: Nodes_Node_Ceph_Pools_NamePUTRequest | None = None) -> Nodes_Node_Ceph_Pools_NamePUTResponse:
        """
        Change POOL settings. Deprecated, please use `/nodes/{node}/ceph/pool/{name}`.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

