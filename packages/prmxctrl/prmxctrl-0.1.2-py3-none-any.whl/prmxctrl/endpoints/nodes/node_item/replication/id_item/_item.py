"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .status._item import NodesReplicationStatusEndpoints
from .log._item import NodesReplicationLogEndpoints
from .schedule_now._item import NodesReplicationSchedule_NowEndpoints
from prmxctrl.models.nodes import Nodes_Node_Replication_IdGETRequest
from prmxctrl.models.nodes import Nodes_Node_Replication_IdGETResponse  # type: ignore

class NodesReplicationEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/replication/{id}
    """

    # Sub-endpoint properties
    @property
    def status(self) -> NodesReplicationStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesReplicationStatusEndpoints  # type: ignore
        return NodesReplicationStatusEndpoints(self._client, self._build_path("status"))
    @property
    def log(self) -> NodesReplicationLogEndpoints:
        """Access log endpoints"""
        from .log._item import NodesReplicationLogEndpoints  # type: ignore
        return NodesReplicationLogEndpoints(self._client, self._build_path("log"))
    @property
    def schedule_now(self) -> NodesReplicationSchedule_NowEndpoints:
        """Access schedule_now endpoints"""
        from .schedule_now._item import NodesReplicationSchedule_NowEndpoints  # type: ignore
        return NodesReplicationSchedule_NowEndpoints(self._client, self._build_path("schedule_now"))



    async def list(self, params: Nodes_Node_Replication_IdGETRequest | None = None) -> Nodes_Node_Replication_IdGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

