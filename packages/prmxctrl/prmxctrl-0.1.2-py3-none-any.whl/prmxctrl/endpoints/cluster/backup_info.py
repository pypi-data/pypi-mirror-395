"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..backup_info.not_backed_up import ClusterBackup_InfoNot_Backed_UpEndpoints
from prmxctrl.models.cluster import Cluster_Backup_InfoGETResponse  # type: ignore

class ClusterBackup_InfoEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/backup-info
    """

    # Sub-endpoint properties
    @property
    def not_backed_up(self) -> ClusterBackup_InfoNot_Backed_UpEndpoints:
        """Access not-backed-up endpoints"""
        from ..backup_info.not_backed_up import ClusterBackup_InfoNot_Backed_UpEndpoints  # type: ignore
        return ClusterBackup_InfoNot_Backed_UpEndpoints(self._client, self._build_path("not-backed-up"))



    async def list(self, ) -> Cluster_Backup_InfoGETResponse:
        """
        Index for backup info related endpoints

        HTTP Method: GET
        """
        return await self._get()

