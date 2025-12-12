"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Scan_ZfsGETRequest
from prmxctrl.models.nodes import Nodes_Node_Scan_ZfsGETResponse  # type: ignore

class NodesScanZfsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/scan/zfs
    """



    async def list(self, params: Nodes_Node_Scan_ZfsGETRequest | None = None) -> Nodes_Node_Scan_ZfsGETResponse:
        """
        Scan zfs pool list on local node.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

