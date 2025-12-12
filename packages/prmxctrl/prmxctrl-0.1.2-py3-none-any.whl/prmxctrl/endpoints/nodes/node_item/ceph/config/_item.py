"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_ConfigGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_ConfigGETResponse  # type: ignore

class NodesCephConfigEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/config
    """



    async def get(self, params: Nodes_Node_Ceph_ConfigGETRequest | None = None) -> Nodes_Node_Ceph_ConfigGETResponse:
        """
        Get the Ceph configuration file. Deprecated, please use `/nodes/{node}/ceph/cfg/raw.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

