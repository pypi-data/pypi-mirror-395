"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .nfs._item import NodesScanNfsEndpoints
from .cifs._item import NodesScanCifsEndpoints
from .pbs._item import NodesScanPbsEndpoints
from .glusterfs._item import NodesScanGlusterfsEndpoints
from .iscsi._item import NodesScanIscsiEndpoints
from .lvm._item import NodesScanLvmEndpoints
from .lvmthin._item import NodesScanLvmthinEndpoints
from .zfs._item import NodesScanZfsEndpoints
from prmxctrl.models.nodes import Nodes_Node_ScanGETRequest
from prmxctrl.models.nodes import Nodes_Node_ScanGETResponse  # type: ignore

class NodesScanEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/scan
    """

    # Sub-endpoint properties
    @property
    def nfs(self) -> NodesScanNfsEndpoints:
        """Access nfs endpoints"""
        from .nfs._item import NodesScanNfsEndpoints  # type: ignore
        return NodesScanNfsEndpoints(self._client, self._build_path("nfs"))
    @property
    def cifs(self) -> NodesScanCifsEndpoints:
        """Access cifs endpoints"""
        from .cifs._item import NodesScanCifsEndpoints  # type: ignore
        return NodesScanCifsEndpoints(self._client, self._build_path("cifs"))
    @property
    def pbs(self) -> NodesScanPbsEndpoints:
        """Access pbs endpoints"""
        from .pbs._item import NodesScanPbsEndpoints  # type: ignore
        return NodesScanPbsEndpoints(self._client, self._build_path("pbs"))
    @property
    def glusterfs(self) -> NodesScanGlusterfsEndpoints:
        """Access glusterfs endpoints"""
        from .glusterfs._item import NodesScanGlusterfsEndpoints  # type: ignore
        return NodesScanGlusterfsEndpoints(self._client, self._build_path("glusterfs"))
    @property
    def iscsi(self) -> NodesScanIscsiEndpoints:
        """Access iscsi endpoints"""
        from .iscsi._item import NodesScanIscsiEndpoints  # type: ignore
        return NodesScanIscsiEndpoints(self._client, self._build_path("iscsi"))
    @property
    def lvm(self) -> NodesScanLvmEndpoints:
        """Access lvm endpoints"""
        from .lvm._item import NodesScanLvmEndpoints  # type: ignore
        return NodesScanLvmEndpoints(self._client, self._build_path("lvm"))
    @property
    def lvmthin(self) -> NodesScanLvmthinEndpoints:
        """Access lvmthin endpoints"""
        from .lvmthin._item import NodesScanLvmthinEndpoints  # type: ignore
        return NodesScanLvmthinEndpoints(self._client, self._build_path("lvmthin"))
    @property
    def zfs(self) -> NodesScanZfsEndpoints:
        """Access zfs endpoints"""
        from .zfs._item import NodesScanZfsEndpoints  # type: ignore
        return NodesScanZfsEndpoints(self._client, self._build_path("zfs"))



    async def list(self, params: Nodes_Node_ScanGETRequest | None = None) -> Nodes_Node_ScanGETResponse:
        """
        Index of available scan methods

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

