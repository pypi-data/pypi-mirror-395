"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .migrate._item import ClusterHaResourcesMigrateEndpoints
from .relocate._item import ClusterHaResourcesRelocateEndpoints
from prmxctrl.models.cluster import Cluster_Ha_Resources_SidDELETERequest
from prmxctrl.models.cluster import Cluster_Ha_Resources_SidGETRequest
from prmxctrl.models.cluster import Cluster_Ha_Resources_SidGETResponse
from prmxctrl.models.cluster import Cluster_Ha_Resources_SidPUTRequest  # type: ignore

class ClusterHaResourcesEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/ha/resources/{sid}
    """

    # Sub-endpoint properties
    @property
    def migrate(self) -> ClusterHaResourcesMigrateEndpoints:
        """Access migrate endpoints"""
        from .migrate._item import ClusterHaResourcesMigrateEndpoints  # type: ignore
        return ClusterHaResourcesMigrateEndpoints(self._client, self._build_path("migrate"))
    @property
    def relocate(self) -> ClusterHaResourcesRelocateEndpoints:
        """Access relocate endpoints"""
        from .relocate._item import ClusterHaResourcesRelocateEndpoints  # type: ignore
        return ClusterHaResourcesRelocateEndpoints(self._client, self._build_path("relocate"))



    async def delete(self, params: Cluster_Ha_Resources_SidDELETERequest | None = None) -> Any:
        """
        Delete resource configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Ha_Resources_SidGETRequest | None = None) -> Cluster_Ha_Resources_SidGETResponse:
        """
        Read resource configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Ha_Resources_SidPUTRequest | None = None) -> Any:
        """
        Update resource configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

