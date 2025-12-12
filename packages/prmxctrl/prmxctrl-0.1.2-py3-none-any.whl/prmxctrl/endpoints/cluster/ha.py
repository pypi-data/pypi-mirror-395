"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..ha.resources import ClusterHaResourcesEndpoints
from ..ha.groups import ClusterHaGroupsEndpoints
from ..ha.status import ClusterHaStatusEndpoints
from prmxctrl.models.cluster import Cluster_HaGETResponse  # type: ignore

class ClusterHaEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ha
    """

    # Sub-endpoint properties
    @property
    def resources(self) -> ClusterHaResourcesEndpoints:
        """Access resources endpoints"""
        from ..ha.resources import ClusterHaResourcesEndpoints  # type: ignore
        return ClusterHaResourcesEndpoints(self._client, self._build_path("resources"))
    @property
    def groups(self) -> ClusterHaGroupsEndpoints:
        """Access groups endpoints"""
        from ..ha.groups import ClusterHaGroupsEndpoints  # type: ignore
        return ClusterHaGroupsEndpoints(self._client, self._build_path("groups"))
    @property
    def status(self) -> ClusterHaStatusEndpoints:
        """Access status endpoints"""
        from ..ha.status import ClusterHaStatusEndpoints  # type: ignore
        return ClusterHaStatusEndpoints(self._client, self._build_path("status"))



    async def list(self, ) -> Cluster_HaGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get()

