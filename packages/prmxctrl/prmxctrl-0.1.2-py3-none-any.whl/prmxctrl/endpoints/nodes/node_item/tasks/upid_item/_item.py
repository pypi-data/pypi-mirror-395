"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .log._item import NodesTasksLogEndpoints
from .status._item import NodesTasksStatusEndpoints
from prmxctrl.models.nodes import Nodes_Node_Tasks_UpidDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Tasks_UpidGETRequest
from prmxctrl.models.nodes import Nodes_Node_Tasks_UpidGETResponse  # type: ignore

class NodesTasksEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/tasks/{upid}
    """

    # Sub-endpoint properties
    @property
    def log(self) -> NodesTasksLogEndpoints:
        """Access log endpoints"""
        from .log._item import NodesTasksLogEndpoints  # type: ignore
        return NodesTasksLogEndpoints(self._client, self._build_path("log"))
    @property
    def status(self) -> NodesTasksStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesTasksStatusEndpoints  # type: ignore
        return NodesTasksStatusEndpoints(self._client, self._build_path("status"))



    async def delete(self, params: Nodes_Node_Tasks_UpidDELETERequest | None = None) -> Any:
        """
        Stop a task.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Tasks_UpidGETRequest | None = None) -> Nodes_Node_Tasks_UpidGETResponse:
        """
        GET operation

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

