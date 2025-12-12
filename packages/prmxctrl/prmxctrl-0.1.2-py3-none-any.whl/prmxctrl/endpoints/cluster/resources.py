"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_ResourcesGETRequest
from prmxctrl.models.cluster import Cluster_ResourcesGETResponse  # type: ignore

class ClusterResourcesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/resources
    """



    async def list(self, params: Cluster_ResourcesGETRequest | None = None) -> Cluster_ResourcesGETResponse:
        """
        Resources index (cluster wide).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

