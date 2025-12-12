"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .lvm._item import NodesDisksLvmEndpoints
from .lvmthin._item import NodesDisksLvmthinEndpoints
from .directory._item import NodesDisksDirectoryEndpoints
from .zfs._item import NodesDisksZfsEndpoints
from .list._item import NodesDisksListEndpoints
from .smart._item import NodesDisksSmartEndpoints
from .initgpt._item import NodesDisksInitgptEndpoints
from .wipedisk._item import NodesDisksWipediskEndpoints
from prmxctrl.models.nodes import Nodes_Node_DisksGETRequest
from prmxctrl.models.nodes import Nodes_Node_DisksGETResponse  # type: ignore

class NodesDisksEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks
    """

    # Sub-endpoint properties
    @property
    def lvm(self) -> NodesDisksLvmEndpoints:
        """Access lvm endpoints"""
        from .lvm._item import NodesDisksLvmEndpoints  # type: ignore
        return NodesDisksLvmEndpoints(self._client, self._build_path("lvm"))
    @property
    def lvmthin(self) -> NodesDisksLvmthinEndpoints:
        """Access lvmthin endpoints"""
        from .lvmthin._item import NodesDisksLvmthinEndpoints  # type: ignore
        return NodesDisksLvmthinEndpoints(self._client, self._build_path("lvmthin"))
    @property
    def directory(self) -> NodesDisksDirectoryEndpoints:
        """Access directory endpoints"""
        from .directory._item import NodesDisksDirectoryEndpoints  # type: ignore
        return NodesDisksDirectoryEndpoints(self._client, self._build_path("directory"))
    @property
    def zfs(self) -> NodesDisksZfsEndpoints:
        """Access zfs endpoints"""
        from .zfs._item import NodesDisksZfsEndpoints  # type: ignore
        return NodesDisksZfsEndpoints(self._client, self._build_path("zfs"))
    @property
    def list(self) -> NodesDisksListEndpoints:
        """Access list endpoints"""
        from .list._item import NodesDisksListEndpoints  # type: ignore
        return NodesDisksListEndpoints(self._client, self._build_path("list"))
    @property
    def smart(self) -> NodesDisksSmartEndpoints:
        """Access smart endpoints"""
        from .smart._item import NodesDisksSmartEndpoints  # type: ignore
        return NodesDisksSmartEndpoints(self._client, self._build_path("smart"))
    @property
    def initgpt(self) -> NodesDisksInitgptEndpoints:
        """Access initgpt endpoints"""
        from .initgpt._item import NodesDisksInitgptEndpoints  # type: ignore
        return NodesDisksInitgptEndpoints(self._client, self._build_path("initgpt"))
    @property
    def wipedisk(self) -> NodesDisksWipediskEndpoints:
        """Access wipedisk endpoints"""
        from .wipedisk._item import NodesDisksWipediskEndpoints  # type: ignore
        return NodesDisksWipediskEndpoints(self._client, self._build_path("wipedisk"))



    async def get(self, params: Nodes_Node_DisksGETRequest | None = None) -> Nodes_Node_DisksGETResponse:
        """
        Node index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

