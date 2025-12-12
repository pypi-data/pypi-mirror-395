"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Replication_IdDELETERequest
from prmxctrl.models.cluster import Cluster_Replication_IdGETRequest
from prmxctrl.models.cluster import Cluster_Replication_IdGETResponse
from prmxctrl.models.cluster import Cluster_Replication_IdPUTRequest  # type: ignore

class ClusterReplicationEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/replication/{id}
    """



    async def delete(self, params: Cluster_Replication_IdDELETERequest | None = None) -> Any:
        """
        Mark replication job for removal.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Replication_IdGETRequest | None = None) -> Cluster_Replication_IdGETResponse:
        """
        Read replication job configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Replication_IdPUTRequest | None = None) -> Any:
        """
        Update replication job configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

