"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .id_item._item import ClusterBackupEndpoints1
from prmxctrl.models.cluster import Cluster_BackupGETResponse
from prmxctrl.models.cluster import Cluster_BackupPOSTRequest  # type: ignore

class ClusterBackupEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/backup
    """


    def __call__(self, id: int) -> ClusterBackupEndpoints1:
        """Access specific id"""
        from .id_item._item import ClusterBackupEndpoints1  # type: ignore
        return ClusterBackupEndpoints1(
            self._client,
            self._build_path(str(id))
        )


    async def list(self, ) -> Cluster_BackupGETResponse:
        """
        List vzdump backup schedule.

        HTTP Method: GET
        """
        return await self._get()

    async def create_job(self, params: Cluster_BackupPOSTRequest | None = None) -> Any:
        """
        Create new vzdump backup job.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

