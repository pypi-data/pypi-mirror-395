"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_ConfigdbGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_ConfigdbGETResponse  # type: ignore

class NodesCephConfigdbEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/configdb
    """



    async def list(self, params: Nodes_Node_Ceph_ConfigdbGETRequest | None = None) -> Nodes_Node_Ceph_ConfigdbGETResponse:
        """
        Get the Ceph configuration database. Deprecated, please use `/nodes/{node}/ceph/cfg/db.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

