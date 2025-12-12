"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mds_NameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mds_NameDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mds_NamePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Mds_NamePOSTResponse  # type: ignore

class NodesCephMdsEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/mds/{name}
    """



    async def delete(self, params: Nodes_Node_Ceph_Mds_NameDELETERequest | None = None) -> Nodes_Node_Ceph_Mds_NameDELETEResponse:
        """
        Destroy Ceph Metadata Server

        HTTP Method: DELETE
        """
        return await self._delete()

    async def createmds(self, params: Nodes_Node_Ceph_Mds_NamePOSTRequest | None = None) -> Nodes_Node_Ceph_Mds_NamePOSTResponse:
        """
        Create Ceph Metadata Server (MDS)

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

