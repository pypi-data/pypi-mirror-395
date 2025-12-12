"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_LogGETRequest
from prmxctrl.models.cluster import Cluster_LogGETResponse  # type: ignore

class ClusterLogEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/log
    """



    async def list(self, params: Cluster_LogGETRequest | None = None) -> Cluster_LogGETResponse:
        """
        Read cluster log

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

