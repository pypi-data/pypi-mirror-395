"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .cfg._item import NodesCephCfgEndpoints
from .osd._item import NodesCephOsdEndpoints
from .mds._item import NodesCephMdsEndpoints
from .mgr._item import NodesCephMgrEndpoints
from .mon._item import NodesCephMonEndpoints
from .fs._item import NodesCephFsEndpoints
from .pool._item import NodesCephPoolEndpoints
from .pools._item import NodesCephPoolsEndpoints
from .config._item import NodesCephConfigEndpoints
from .configdb._item import NodesCephConfigdbEndpoints
from .init._item import NodesCephInitEndpoints
from .stop._item import NodesCephStopEndpoints
from .start._item import NodesCephStartEndpoints
from .restart._item import NodesCephRestartEndpoints
from .status._item import NodesCephStatusEndpoints
from .crush._item import NodesCephCrushEndpoints
from .log._item import NodesCephLogEndpoints
from .rules._item import NodesCephRulesEndpoints
from .cmd_safety._item import NodesCephCmd_SafetyEndpoints
from prmxctrl.models.nodes import Nodes_Node_CephGETRequest
from prmxctrl.models.nodes import Nodes_Node_CephGETResponse  # type: ignore

class NodesCephEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph
    """

    # Sub-endpoint properties
    @property
    def cfg(self) -> NodesCephCfgEndpoints:
        """Access cfg endpoints"""
        from .cfg._item import NodesCephCfgEndpoints  # type: ignore
        return NodesCephCfgEndpoints(self._client, self._build_path("cfg"))
    @property
    def osd(self) -> NodesCephOsdEndpoints:
        """Access osd endpoints"""
        from .osd._item import NodesCephOsdEndpoints  # type: ignore
        return NodesCephOsdEndpoints(self._client, self._build_path("osd"))
    @property
    def mds(self) -> NodesCephMdsEndpoints:
        """Access mds endpoints"""
        from .mds._item import NodesCephMdsEndpoints  # type: ignore
        return NodesCephMdsEndpoints(self._client, self._build_path("mds"))
    @property
    def mgr(self) -> NodesCephMgrEndpoints:
        """Access mgr endpoints"""
        from .mgr._item import NodesCephMgrEndpoints  # type: ignore
        return NodesCephMgrEndpoints(self._client, self._build_path("mgr"))
    @property
    def mon(self) -> NodesCephMonEndpoints:
        """Access mon endpoints"""
        from .mon._item import NodesCephMonEndpoints  # type: ignore
        return NodesCephMonEndpoints(self._client, self._build_path("mon"))
    @property
    def fs(self) -> NodesCephFsEndpoints:
        """Access fs endpoints"""
        from .fs._item import NodesCephFsEndpoints  # type: ignore
        return NodesCephFsEndpoints(self._client, self._build_path("fs"))
    @property
    def pool(self) -> NodesCephPoolEndpoints:
        """Access pool endpoints"""
        from .pool._item import NodesCephPoolEndpoints  # type: ignore
        return NodesCephPoolEndpoints(self._client, self._build_path("pool"))
    @property
    def pools(self) -> NodesCephPoolsEndpoints:
        """Access pools endpoints"""
        from .pools._item import NodesCephPoolsEndpoints  # type: ignore
        return NodesCephPoolsEndpoints(self._client, self._build_path("pools"))
    @property
    def config(self) -> NodesCephConfigEndpoints:
        """Access config endpoints"""
        from .config._item import NodesCephConfigEndpoints  # type: ignore
        return NodesCephConfigEndpoints(self._client, self._build_path("config"))
    @property
    def configdb(self) -> NodesCephConfigdbEndpoints:
        """Access configdb endpoints"""
        from .configdb._item import NodesCephConfigdbEndpoints  # type: ignore
        return NodesCephConfigdbEndpoints(self._client, self._build_path("configdb"))
    @property
    def init(self) -> NodesCephInitEndpoints:
        """Access init endpoints"""
        from .init._item import NodesCephInitEndpoints  # type: ignore
        return NodesCephInitEndpoints(self._client, self._build_path("init"))
    @property
    def stop(self) -> NodesCephStopEndpoints:
        """Access stop endpoints"""
        from .stop._item import NodesCephStopEndpoints  # type: ignore
        return NodesCephStopEndpoints(self._client, self._build_path("stop"))
    @property
    def start(self) -> NodesCephStartEndpoints:
        """Access start endpoints"""
        from .start._item import NodesCephStartEndpoints  # type: ignore
        return NodesCephStartEndpoints(self._client, self._build_path("start"))
    @property
    def restart(self) -> NodesCephRestartEndpoints:
        """Access restart endpoints"""
        from .restart._item import NodesCephRestartEndpoints  # type: ignore
        return NodesCephRestartEndpoints(self._client, self._build_path("restart"))
    @property
    def status(self) -> NodesCephStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesCephStatusEndpoints  # type: ignore
        return NodesCephStatusEndpoints(self._client, self._build_path("status"))
    @property
    def crush(self) -> NodesCephCrushEndpoints:
        """Access crush endpoints"""
        from .crush._item import NodesCephCrushEndpoints  # type: ignore
        return NodesCephCrushEndpoints(self._client, self._build_path("crush"))
    @property
    def log(self) -> NodesCephLogEndpoints:
        """Access log endpoints"""
        from .log._item import NodesCephLogEndpoints  # type: ignore
        return NodesCephLogEndpoints(self._client, self._build_path("log"))
    @property
    def rules(self) -> NodesCephRulesEndpoints:
        """Access rules endpoints"""
        from .rules._item import NodesCephRulesEndpoints  # type: ignore
        return NodesCephRulesEndpoints(self._client, self._build_path("rules"))
    @property
    def cmd_safety(self) -> NodesCephCmd_SafetyEndpoints:
        """Access cmd-safety endpoints"""
        from .cmd_safety._item import NodesCephCmd_SafetyEndpoints  # type: ignore
        return NodesCephCmd_SafetyEndpoints(self._client, self._build_path("cmd-safety"))



    async def list(self, params: Nodes_Node_CephGETRequest | None = None) -> Nodes_Node_CephGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

