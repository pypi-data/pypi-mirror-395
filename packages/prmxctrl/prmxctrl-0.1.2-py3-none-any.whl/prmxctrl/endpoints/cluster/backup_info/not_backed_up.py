"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Backup_Info_Not_Backed_UpGETResponse  # type: ignore

class ClusterBackup_InfoNot_Backed_UpEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/backup-info/not-backed-up
    """



    async def list(self, ) -> Cluster_Backup_Info_Not_Backed_UpGETResponse:
        """
        Shows all guests which are not covered by any backup job.

        HTTP Method: GET
        """
        return await self._get()

