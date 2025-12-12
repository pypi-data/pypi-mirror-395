"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Acme_TosGETRequest
from prmxctrl.models.cluster import Cluster_Acme_TosGETResponse  # type: ignore

class ClusterAcmeTosEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/acme/tos
    """



    async def get(self, params: Cluster_Acme_TosGETRequest | None = None) -> Cluster_Acme_TosGETResponse:
        """
        Retrieve ACME TermsOfService URL from CA.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

