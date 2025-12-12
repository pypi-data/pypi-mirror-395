"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Scan_IscsiGETRequest
from prmxctrl.models.nodes import Nodes_Node_Scan_IscsiGETResponse  # type: ignore

class NodesScanIscsiEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/scan/iscsi
    """



    async def list(self, params: Nodes_Node_Scan_IscsiGETRequest | None = None) -> Nodes_Node_Scan_IscsiGETResponse:
        """
        Scan remote iSCSI server.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

