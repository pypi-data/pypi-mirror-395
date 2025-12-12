"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_NextidGETRequest
from prmxctrl.models.cluster import Cluster_NextidGETResponse  # type: ignore

class ClusterNextidEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/nextid
    """



    async def get(self, params: Cluster_NextidGETRequest | None = None) -> Cluster_NextidGETResponse:
        """
        Get next free VMID. Pass a VMID to assert that its free (at time of check).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

