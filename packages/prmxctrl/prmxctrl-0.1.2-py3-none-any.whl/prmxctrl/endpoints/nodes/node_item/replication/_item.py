"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .id_item._item import NodesReplicationEndpoints1
from prmxctrl.models.nodes import Nodes_Node_ReplicationGETRequest
from prmxctrl.models.nodes import Nodes_Node_ReplicationGETResponse  # type: ignore

class NodesReplicationEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/replication
    """


    def __call__(self, id: int) -> NodesReplicationEndpoints1:
        """Access specific id"""
        from .id_item._item import NodesReplicationEndpoints1  # type: ignore
        return NodesReplicationEndpoints1(
            self._client,
            self._build_path(str(id))
        )


    async def list(self, params: Nodes_Node_ReplicationGETRequest | None = None) -> Nodes_Node_ReplicationGETResponse:
        """
        List status of all replication jobs on this node.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

