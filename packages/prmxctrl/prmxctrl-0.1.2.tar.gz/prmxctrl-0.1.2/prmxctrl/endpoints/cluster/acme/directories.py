"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Acme_DirectoriesGETResponse  # type: ignore

class ClusterAcmeDirectoriesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/acme/directories
    """



    async def list(self, ) -> Cluster_Acme_DirectoriesGETResponse:
        """
        Get named known ACME directory endpoints.

        HTTP Method: GET
        """
        return await self._get()

