"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Scan_LvmthinGETRequest
from prmxctrl.models.nodes import Nodes_Node_Scan_LvmthinGETResponse  # type: ignore

class NodesScanLvmthinEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/scan/lvmthin
    """



    async def list(self, params: Nodes_Node_Scan_LvmthinGETRequest | None = None) -> Nodes_Node_Scan_LvmthinGETResponse:
        """
        List local LVM Thin Pools.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

