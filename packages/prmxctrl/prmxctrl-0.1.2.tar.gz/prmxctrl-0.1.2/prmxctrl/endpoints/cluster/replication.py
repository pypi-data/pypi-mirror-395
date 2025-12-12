"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .id_item._item import ClusterReplicationEndpoints1
from prmxctrl.models.cluster import Cluster_ReplicationGETResponse
from prmxctrl.models.cluster import Cluster_ReplicationPOSTRequest  # type: ignore

class ClusterReplicationEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/replication
    """


    def __call__(self, id: int) -> ClusterReplicationEndpoints1:
        """Access specific id"""
        from .id_item._item import ClusterReplicationEndpoints1  # type: ignore
        return ClusterReplicationEndpoints1(
            self._client,
            self._build_path(str(id))
        )


    async def list(self, ) -> Cluster_ReplicationGETResponse:
        """
        List replication jobs.

        HTTP Method: GET
        """
        return await self._get()

    async def create(self, params: Cluster_ReplicationPOSTRequest | None = None) -> Any:
        """
        Create a new replication job

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

