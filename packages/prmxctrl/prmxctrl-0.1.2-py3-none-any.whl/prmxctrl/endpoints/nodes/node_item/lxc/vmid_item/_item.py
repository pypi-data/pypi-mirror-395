"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .config._item import NodesLxcConfigEndpoints
from .status._item import NodesLxcStatusEndpoints
from .snapshot._item import NodesLxcSnapshotEndpoints
from .firewall._item import NodesLxcFirewallEndpoints
from .rrd._item import NodesLxcRrdEndpoints
from .rrddata._item import NodesLxcRrddataEndpoints
from .vncproxy._item import NodesLxcVncproxyEndpoints
from .termproxy._item import NodesLxcTermproxyEndpoints
from .vncwebsocket._item import NodesLxcVncwebsocketEndpoints
from .spiceproxy._item import NodesLxcSpiceproxyEndpoints
from .remote_migrate._item import NodesLxcRemote_MigrateEndpoints
from .migrate._item import NodesLxcMigrateEndpoints
from .feature._item import NodesLxcFeatureEndpoints
from .template._item import NodesLxcTemplateEndpoints
from .clone._item import NodesLxcCloneEndpoints
from .resize._item import NodesLxcResizeEndpoints
from .move_volume._item import NodesLxcMove_VolumeEndpoints
from .pending._item import NodesLxcPendingEndpoints
from .mtunnel._item import NodesLxcMtunnelEndpoints
from .mtunnelwebsocket._item import NodesLxcMtunnelwebsocketEndpoints
from prmxctrl.models.nodes import Nodes_Node_Lxc_VmidDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_VmidDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Lxc_VmidGETRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_VmidGETResponse  # type: ignore

class NodesLxcEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}
    """

    # Sub-endpoint properties
    @property
    def config(self) -> NodesLxcConfigEndpoints:
        """Access config endpoints"""
        from .config._item import NodesLxcConfigEndpoints  # type: ignore
        return NodesLxcConfigEndpoints(self._client, self._build_path("config"))
    @property
    def status(self) -> NodesLxcStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesLxcStatusEndpoints  # type: ignore
        return NodesLxcStatusEndpoints(self._client, self._build_path("status"))
    @property
    def snapshot(self) -> NodesLxcSnapshotEndpoints:
        """Access snapshot endpoints"""
        from .snapshot._item import NodesLxcSnapshotEndpoints  # type: ignore
        return NodesLxcSnapshotEndpoints(self._client, self._build_path("snapshot"))
    @property
    def firewall(self) -> NodesLxcFirewallEndpoints:
        """Access firewall endpoints"""
        from .firewall._item import NodesLxcFirewallEndpoints  # type: ignore
        return NodesLxcFirewallEndpoints(self._client, self._build_path("firewall"))
    @property
    def rrd(self) -> NodesLxcRrdEndpoints:
        """Access rrd endpoints"""
        from .rrd._item import NodesLxcRrdEndpoints  # type: ignore
        return NodesLxcRrdEndpoints(self._client, self._build_path("rrd"))
    @property
    def rrddata(self) -> NodesLxcRrddataEndpoints:
        """Access rrddata endpoints"""
        from .rrddata._item import NodesLxcRrddataEndpoints  # type: ignore
        return NodesLxcRrddataEndpoints(self._client, self._build_path("rrddata"))
    @property
    def vncproxy(self) -> NodesLxcVncproxyEndpoints:
        """Access vncproxy endpoints"""
        from .vncproxy._item import NodesLxcVncproxyEndpoints  # type: ignore
        return NodesLxcVncproxyEndpoints(self._client, self._build_path("vncproxy"))
    @property
    def termproxy(self) -> NodesLxcTermproxyEndpoints:
        """Access termproxy endpoints"""
        from .termproxy._item import NodesLxcTermproxyEndpoints  # type: ignore
        return NodesLxcTermproxyEndpoints(self._client, self._build_path("termproxy"))
    @property
    def vncwebsocket(self) -> NodesLxcVncwebsocketEndpoints:
        """Access vncwebsocket endpoints"""
        from .vncwebsocket._item import NodesLxcVncwebsocketEndpoints  # type: ignore
        return NodesLxcVncwebsocketEndpoints(self._client, self._build_path("vncwebsocket"))
    @property
    def spiceproxy(self) -> NodesLxcSpiceproxyEndpoints:
        """Access spiceproxy endpoints"""
        from .spiceproxy._item import NodesLxcSpiceproxyEndpoints  # type: ignore
        return NodesLxcSpiceproxyEndpoints(self._client, self._build_path("spiceproxy"))
    @property
    def remote_migrate(self) -> NodesLxcRemote_MigrateEndpoints:
        """Access remote_migrate endpoints"""
        from .remote_migrate._item import NodesLxcRemote_MigrateEndpoints  # type: ignore
        return NodesLxcRemote_MigrateEndpoints(self._client, self._build_path("remote_migrate"))
    @property
    def migrate(self) -> NodesLxcMigrateEndpoints:
        """Access migrate endpoints"""
        from .migrate._item import NodesLxcMigrateEndpoints  # type: ignore
        return NodesLxcMigrateEndpoints(self._client, self._build_path("migrate"))
    @property
    def feature(self) -> NodesLxcFeatureEndpoints:
        """Access feature endpoints"""
        from .feature._item import NodesLxcFeatureEndpoints  # type: ignore
        return NodesLxcFeatureEndpoints(self._client, self._build_path("feature"))
    @property
    def template(self) -> NodesLxcTemplateEndpoints:
        """Access template endpoints"""
        from .template._item import NodesLxcTemplateEndpoints  # type: ignore
        return NodesLxcTemplateEndpoints(self._client, self._build_path("template"))
    @property
    def clone(self) -> NodesLxcCloneEndpoints:
        """Access clone endpoints"""
        from .clone._item import NodesLxcCloneEndpoints  # type: ignore
        return NodesLxcCloneEndpoints(self._client, self._build_path("clone"))
    @property
    def resize(self) -> NodesLxcResizeEndpoints:
        """Access resize endpoints"""
        from .resize._item import NodesLxcResizeEndpoints  # type: ignore
        return NodesLxcResizeEndpoints(self._client, self._build_path("resize"))
    @property
    def move_volume(self) -> NodesLxcMove_VolumeEndpoints:
        """Access move_volume endpoints"""
        from .move_volume._item import NodesLxcMove_VolumeEndpoints  # type: ignore
        return NodesLxcMove_VolumeEndpoints(self._client, self._build_path("move_volume"))
    @property
    def pending(self) -> NodesLxcPendingEndpoints:
        """Access pending endpoints"""
        from .pending._item import NodesLxcPendingEndpoints  # type: ignore
        return NodesLxcPendingEndpoints(self._client, self._build_path("pending"))
    @property
    def mtunnel(self) -> NodesLxcMtunnelEndpoints:
        """Access mtunnel endpoints"""
        from .mtunnel._item import NodesLxcMtunnelEndpoints  # type: ignore
        return NodesLxcMtunnelEndpoints(self._client, self._build_path("mtunnel"))
    @property
    def mtunnelwebsocket(self) -> NodesLxcMtunnelwebsocketEndpoints:
        """Access mtunnelwebsocket endpoints"""
        from .mtunnelwebsocket._item import NodesLxcMtunnelwebsocketEndpoints  # type: ignore
        return NodesLxcMtunnelwebsocketEndpoints(self._client, self._build_path("mtunnelwebsocket"))



    async def delete(self, params: Nodes_Node_Lxc_VmidDELETERequest | None = None) -> Nodes_Node_Lxc_VmidDELETEResponse:
        """
        Destroy the container (also delete all uses files).

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Lxc_VmidGETRequest | None = None) -> Nodes_Node_Lxc_VmidGETResponse:
        """
        Directory index

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

