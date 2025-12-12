"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Backup_Id_Included_VolumesGETRequest
from prmxctrl.models.cluster import Cluster_Backup_Id_Included_VolumesGETResponse  # type: ignore

class ClusterBackupIncluded_VolumesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/backup/{id}/included_volumes
    """



    async def get(self, params: Cluster_Backup_Id_Included_VolumesGETRequest | None = None) -> Cluster_Backup_Id_Included_VolumesGETResponse:
        """
        Returns included guests and the backup status of their disks. Optimized to be used in ExtJS tree views.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

