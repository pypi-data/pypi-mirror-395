"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Cfg_RawGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Cfg_RawGETResponse  # type: ignore

class NodesCephCfgRawEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/cfg/raw
    """



    async def get(self, params: Nodes_Node_Ceph_Cfg_RawGETRequest | None = None) -> Nodes_Node_Ceph_Cfg_RawGETResponse:
        """
        Get the Ceph configuration file.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

