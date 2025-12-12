"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ha_Resources_Sid_RelocatePOSTRequest  # type: ignore

class ClusterHaResourcesRelocateEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha/resources/{sid}/relocate
    """



    async def relocate(self, params: Cluster_Ha_Resources_Sid_RelocatePOSTRequest | None = None) -> Any:
        """
        Request resource relocatzion to another node. This stops the service on the old node, and restarts it on the target node.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

