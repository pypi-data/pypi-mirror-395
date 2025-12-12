"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Tasks_Upid_StatusGETRequest
from prmxctrl.models.nodes import Nodes_Node_Tasks_Upid_StatusGETResponse  # type: ignore

class NodesTasksStatusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/tasks/{upid}/status
    """



    async def get(self, params: Nodes_Node_Tasks_Upid_StatusGETRequest | None = None) -> Nodes_Node_Tasks_Upid_StatusGETResponse:
        """
        Read task status.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

