"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mon_MonidDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mon_MonidDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mon_MonidPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mon_MonidPOSTResponse  # type: ignore

class NodesCephMonEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/mon/{monid}
    """



    async def delete(self, params: Nodes_Node_Ceph_Mon_MonidDELETERequest | None = None) -> Nodes_Node_Ceph_Mon_MonidDELETEResponse:
        """
        Destroy Ceph Monitor and Manager.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def createmon(self, params: Nodes_Node_Ceph_Mon_MonidPOSTRequest | None = None) -> Nodes_Node_Ceph_Mon_MonidPOSTResponse:
        """
        Create Ceph Monitor and Manager

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

