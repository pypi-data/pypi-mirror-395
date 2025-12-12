"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_ReportGETRequest
from prmxctrl.models.nodes import Nodes_Node_ReportGETResponse  # type: ignore

class NodesReportEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/report
    """



    async def get(self, params: Nodes_Node_ReportGETRequest | None = None) -> Nodes_Node_ReportGETResponse:
        """
        Gather various systems information about a node

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

