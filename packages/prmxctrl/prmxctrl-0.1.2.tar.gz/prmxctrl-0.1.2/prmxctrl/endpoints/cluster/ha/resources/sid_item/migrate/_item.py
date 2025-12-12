"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ha_Resources_Sid_MigratePOSTRequest  # type: ignore

class ClusterHaResourcesMigrateEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha/resources/{sid}/migrate
    """



    async def migrate(self, params: Cluster_Ha_Resources_Sid_MigratePOSTRequest | None = None) -> Any:
        """
        Request resource migration (online) to another node.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

