"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Acme_Challenge_SchemaGETResponse  # type: ignore

class ClusterAcmeChallenge_SchemaEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/acme/challenge-schema
    """



    async def list(self, ) -> Cluster_Acme_Challenge_SchemaGETResponse:
        """
        Get schema of ACME challenge types.

        HTTP Method: GET
        """
        return await self._get()

