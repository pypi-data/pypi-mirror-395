"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Ceph_MetadataGETRequest
from prmxctrl.models.cluster import Cluster_Ceph_MetadataGETResponse  # type: ignore

class ClusterCephMetadataEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/ceph/metadata
    """



    async def get(self, params: Cluster_Ceph_MetadataGETRequest | None = None) -> Cluster_Ceph_MetadataGETResponse:
        """
        Get ceph metadata.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

