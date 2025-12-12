"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..config.apiversion import ClusterConfigApiversionEndpoints
from ..config.nodes import ClusterConfigNodesEndpoints
from ..config.join import ClusterConfigJoinEndpoints
from ..config.totem import ClusterConfigTotemEndpoints
from ..config.qdevice import ClusterConfigQdeviceEndpoints
from prmxctrl.models.cluster import Cluster_ConfigGETResponse
from prmxctrl.models.cluster import Cluster_ConfigPOSTRequest
from prmxctrl.models.cluster import Cluster_ConfigPOSTResponse  # type: ignore

class ClusterConfigEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/config
    """

    # Sub-endpoint properties
    @property
    def apiversion(self) -> ClusterConfigApiversionEndpoints:
        """Access apiversion endpoints"""
        from ..config.apiversion import ClusterConfigApiversionEndpoints  # type: ignore
        return ClusterConfigApiversionEndpoints(self._client, self._build_path("apiversion"))
    @property
    def nodes(self) -> ClusterConfigNodesEndpoints:
        """Access nodes endpoints"""
        from ..config.nodes import ClusterConfigNodesEndpoints  # type: ignore
        return ClusterConfigNodesEndpoints(self._client, self._build_path("nodes"))
    @property
    def join(self) -> ClusterConfigJoinEndpoints:
        """Access join endpoints"""
        from ..config.join import ClusterConfigJoinEndpoints  # type: ignore
        return ClusterConfigJoinEndpoints(self._client, self._build_path("join"))
    @property
    def totem(self) -> ClusterConfigTotemEndpoints:
        """Access totem endpoints"""
        from ..config.totem import ClusterConfigTotemEndpoints  # type: ignore
        return ClusterConfigTotemEndpoints(self._client, self._build_path("totem"))
    @property
    def qdevice(self) -> ClusterConfigQdeviceEndpoints:
        """Access qdevice endpoints"""
        from ..config.qdevice import ClusterConfigQdeviceEndpoints  # type: ignore
        return ClusterConfigQdeviceEndpoints(self._client, self._build_path("qdevice"))



    async def list(self, ) -> Cluster_ConfigGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get()

    async def create(self, params: Cluster_ConfigPOSTRequest | None = None) -> Cluster_ConfigPOSTResponse:
        """
        Generate new cluster configuration. If no links given, default to local IP address as link0.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

