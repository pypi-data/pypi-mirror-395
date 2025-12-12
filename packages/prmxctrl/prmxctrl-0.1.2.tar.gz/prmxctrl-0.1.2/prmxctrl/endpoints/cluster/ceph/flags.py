"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .flag_item._item import ClusterCephFlagsEndpoints1
from prmxctrl.models.cluster import Cluster_Ceph_FlagsGETResponse
from prmxctrl.models.cluster import Cluster_Ceph_FlagsPUTRequest
from prmxctrl.models.cluster import Cluster_Ceph_FlagsPUTResponse  # type: ignore

class ClusterCephFlagsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ceph/flags
    """


    def __call__(self, flag: str) -> ClusterCephFlagsEndpoints1:
        """Access specific flag"""
        from .flag_item._item import ClusterCephFlagsEndpoints1  # type: ignore
        return ClusterCephFlagsEndpoints1(
            self._client,
            self._build_path(str(flag))
        )


    async def list(self, ) -> Cluster_Ceph_FlagsGETResponse:
        """
        get the status of all ceph flags

        HTTP Method: GET
        """
        return await self._get()

    async def set_flags(self, params: Cluster_Ceph_FlagsPUTRequest | None = None) -> Cluster_Ceph_FlagsPUTResponse:
        """
        Set/Unset multiple ceph flags at once.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

