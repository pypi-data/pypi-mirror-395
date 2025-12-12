"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .node_item._item import ClusterConfigNodesEndpoints1
from prmxctrl.models.cluster import Cluster_Config_NodesGETResponse  # type: ignore

class ClusterConfigNodesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/config/nodes
    """


    def __call__(self, node: str) -> ClusterConfigNodesEndpoints1:
        """Access specific node"""
        from .node_item._item import ClusterConfigNodesEndpoints1  # type: ignore
        return ClusterConfigNodesEndpoints1(
            self._client,
            self._build_path(str(node))
        )


    async def list(self, ) -> Cluster_Config_NodesGETResponse:
        """
        Corosync node list.

        HTTP Method: GET
        """
        return await self._get()

