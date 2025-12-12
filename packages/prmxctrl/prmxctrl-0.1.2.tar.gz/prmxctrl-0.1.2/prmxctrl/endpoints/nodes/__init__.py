"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .node_item._item import NodesEndpoints1
from prmxctrl.models.nodes import NodesGETResponse  # type: ignore

class NodesEndpoints(EndpointBase):
    """
    Root endpoint class for nodes API endpoints.
    """


    def __call__(self, node: str) -> NodesEndpoints1:
        """Access specific node"""
        from .node_item._item import NodesEndpoints1  # type: ignore
        return NodesEndpoints1(
            self._client,
            self._build_path(str(node))
        )


    async def list(self, ) -> NodesGETResponse:
        """
        Cluster node index.

        HTTP Method: GET
        """
        return await self._get()

