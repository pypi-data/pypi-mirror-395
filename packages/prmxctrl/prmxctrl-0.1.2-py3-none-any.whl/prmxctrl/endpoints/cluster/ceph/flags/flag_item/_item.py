"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ceph_Flags_FlagGETRequest
from prmxctrl.models.cluster import Cluster_Ceph_Flags_FlagGETResponse
from prmxctrl.models.cluster import Cluster_Ceph_Flags_FlagPUTRequest  # type: ignore

class ClusterCephFlagsEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/ceph/flags/{flag}
    """



    async def get(self, params: Cluster_Ceph_Flags_FlagGETRequest | None = None) -> Cluster_Ceph_Flags_FlagGETResponse:
        """
        Get the status of a specific ceph flag.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_flag(self, params: Cluster_Ceph_Flags_FlagPUTRequest | None = None) -> Any:
        """
        Set or clear (unset) a specific ceph flag

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

