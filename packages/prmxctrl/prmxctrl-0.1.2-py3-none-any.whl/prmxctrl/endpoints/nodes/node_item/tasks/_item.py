"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .upid_item._item import NodesTasksEndpoints1
from prmxctrl.models.nodes import Nodes_Node_TasksGETRequest
from prmxctrl.models.nodes import Nodes_Node_TasksGETResponse  # type: ignore

class NodesTasksEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/tasks
    """


    def __call__(self, upid: int) -> NodesTasksEndpoints1:
        """Access specific upid"""
        from .upid_item._item import NodesTasksEndpoints1  # type: ignore
        return NodesTasksEndpoints1(
            self._client,
            self._build_path(str(upid))
        )


    async def list(self, params: Nodes_Node_TasksGETRequest | None = None) -> Nodes_Node_TasksGETResponse:
        """
        Read task list for one node (finished tasks).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

