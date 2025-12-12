"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .sid_item._item import ClusterHaResourcesEndpoints1
from prmxctrl.models.cluster import Cluster_Ha_ResourcesGETRequest
from prmxctrl.models.cluster import Cluster_Ha_ResourcesGETResponse
from prmxctrl.models.cluster import Cluster_Ha_ResourcesPOSTRequest  # type: ignore

class ClusterHaResourcesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha/resources
    """


    def __call__(self, sid: int) -> ClusterHaResourcesEndpoints1:
        """Access specific sid"""
        from .sid_item._item import ClusterHaResourcesEndpoints1  # type: ignore
        return ClusterHaResourcesEndpoints1(
            self._client,
            self._build_path(str(sid))
        )


    async def list(self, params: Cluster_Ha_ResourcesGETRequest | None = None) -> Cluster_Ha_ResourcesGETResponse:
        """
        List HA resources.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Ha_ResourcesPOSTRequest | None = None) -> Any:
        """
        Create a new HA resource.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

