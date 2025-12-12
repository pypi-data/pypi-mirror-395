"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..ceph.metadata import ClusterCephMetadataEndpoints
from ..ceph.status import ClusterCephStatusEndpoints
from ..ceph.flags import ClusterCephFlagsEndpoints
from prmxctrl.models.cluster import Cluster_CephGETResponse  # type: ignore

class ClusterCephEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ceph
    """

    # Sub-endpoint properties
    @property
    def metadata(self) -> ClusterCephMetadataEndpoints:
        """Access metadata endpoints"""
        from ..ceph.metadata import ClusterCephMetadataEndpoints  # type: ignore
        return ClusterCephMetadataEndpoints(self._client, self._build_path("metadata"))
    @property
    def status(self) -> ClusterCephStatusEndpoints:
        """Access status endpoints"""
        from ..ceph.status import ClusterCephStatusEndpoints  # type: ignore
        return ClusterCephStatusEndpoints(self._client, self._build_path("status"))
    @property
    def flags(self) -> ClusterCephFlagsEndpoints:
        """Access flags endpoints"""
        from ..ceph.flags import ClusterCephFlagsEndpoints  # type: ignore
        return ClusterCephFlagsEndpoints(self._client, self._build_path("flags"))



    async def list(self, ) -> Cluster_CephGETResponse:
        """
        Cluster ceph index.

        HTTP Method: GET
        """
        return await self._get()

