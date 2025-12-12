"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Config_Nodes_NodeDELETERequest
from prmxctrl.models.cluster import Cluster_Config_Nodes_NodePOSTRequest
from prmxctrl.models.cluster import Cluster_Config_Nodes_NodePOSTResponse  # type: ignore

class ClusterConfigNodesEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/config/nodes/{node}
    """



    async def delete(self, params: Cluster_Config_Nodes_NodeDELETERequest | None = None) -> Any:
        """
        Removes a node from the cluster configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def addnode(self, params: Cluster_Config_Nodes_NodePOSTRequest | None = None) -> Cluster_Config_Nodes_NodePOSTResponse:
        """
        Adds a node to the cluster configuration. This call is for internal use.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

