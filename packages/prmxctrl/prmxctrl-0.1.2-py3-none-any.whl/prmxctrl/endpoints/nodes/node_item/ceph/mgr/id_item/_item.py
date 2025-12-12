"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mgr_IdDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mgr_IdDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mgr_IdPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mgr_IdPOSTResponse  # type: ignore

class NodesCephMgrEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/mgr/{id}
    """



    async def delete(self, params: Nodes_Node_Ceph_Mgr_IdDELETERequest | None = None) -> Nodes_Node_Ceph_Mgr_IdDELETEResponse:
        """
        Destroy Ceph Manager.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def createmgr(self, params: Nodes_Node_Ceph_Mgr_IdPOSTRequest | None = None) -> Nodes_Node_Ceph_Mgr_IdPOSTResponse:
        """
        Create Ceph Manager

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

