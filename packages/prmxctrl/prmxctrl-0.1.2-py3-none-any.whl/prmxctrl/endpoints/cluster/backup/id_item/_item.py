"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .included_volumes._item import ClusterBackupIncluded_VolumesEndpoints
from prmxctrl.models.cluster import Cluster_Backup_IdDELETERequest
from prmxctrl.models.cluster import Cluster_Backup_IdGETRequest
from prmxctrl.models.cluster import Cluster_Backup_IdGETResponse
from prmxctrl.models.cluster import Cluster_Backup_IdPUTRequest  # type: ignore

class ClusterBackupEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/backup/{id}
    """

    # Sub-endpoint properties
    @property
    def included_volumes(self) -> ClusterBackupIncluded_VolumesEndpoints:
        """Access included_volumes endpoints"""
        from .included_volumes._item import ClusterBackupIncluded_VolumesEndpoints  # type: ignore
        return ClusterBackupIncluded_VolumesEndpoints(self._client, self._build_path("included_volumes"))



    async def delete(self, params: Cluster_Backup_IdDELETERequest | None = None) -> Any:
        """
        Delete vzdump backup job definition.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Backup_IdGETRequest | None = None) -> Cluster_Backup_IdGETResponse:
        """
        Read vzdump backup job definition.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_job(self, params: Cluster_Backup_IdPUTRequest | None = None) -> Any:
        """
        Update vzdump backup job definition.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

