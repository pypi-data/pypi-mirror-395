"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Config_JoinGETRequest
from prmxctrl.models.cluster import Cluster_Config_JoinGETResponse
from prmxctrl.models.cluster import Cluster_Config_JoinPOSTRequest
from prmxctrl.models.cluster import Cluster_Config_JoinPOSTResponse  # type: ignore

class ClusterConfigJoinEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/config/join
    """



    async def get(self, params: Cluster_Config_JoinGETRequest | None = None) -> Cluster_Config_JoinGETResponse:
        """
        Get information needed to join this cluster over the connected node.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def join(self, params: Cluster_Config_JoinPOSTRequest | None = None) -> Cluster_Config_JoinPOSTResponse:
        """
        Joins this node into an existing cluster. If no links are given, default to IP resolved by node's hostname on single link (fallback fails for clusters with multiple links).

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

