"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Cfg_DbGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Cfg_DbGETResponse  # type: ignore

class NodesCephCfgDbEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/cfg/db
    """



    async def list(self, params: Nodes_Node_Ceph_Cfg_DbGETRequest | None = None) -> Nodes_Node_Ceph_Cfg_DbGETResponse:
        """
        Get the Ceph configuration database.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

