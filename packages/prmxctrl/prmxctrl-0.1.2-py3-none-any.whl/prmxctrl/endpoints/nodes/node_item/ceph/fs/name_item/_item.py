"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Fs_NamePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Fs_NamePOSTResponse  # type: ignore

class NodesCephFsEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/fs/{name}
    """



    async def createfs(self, params: Nodes_Node_Ceph_Fs_NamePOSTRequest | None = None) -> Nodes_Node_Ceph_Fs_NamePOSTResponse:
        """
        Create a Ceph filesystem

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

