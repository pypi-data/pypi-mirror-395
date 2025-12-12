"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .firewall._item import NodesQemuFirewallEndpoints
from .agent._item import NodesQemuAgentEndpoints
from .rrd._item import NodesQemuRrdEndpoints
from .rrddata._item import NodesQemuRrddataEndpoints
from .config._item import NodesQemuConfigEndpoints
from .pending._item import NodesQemuPendingEndpoints
from .cloudinit._item import NodesQemuCloudinitEndpoints
from .unlink._item import NodesQemuUnlinkEndpoints
from .vncproxy._item import NodesQemuVncproxyEndpoints
from .termproxy._item import NodesQemuTermproxyEndpoints
from .vncwebsocket._item import NodesQemuVncwebsocketEndpoints
from .spiceproxy._item import NodesQemuSpiceproxyEndpoints
from .status._item import NodesQemuStatusEndpoints
from .sendkey._item import NodesQemuSendkeyEndpoints
from .feature._item import NodesQemuFeatureEndpoints
from .clone._item import NodesQemuCloneEndpoints
from .move_disk._item import NodesQemuMove_DiskEndpoints
from .migrate._item import NodesQemuMigrateEndpoints
from .remote_migrate._item import NodesQemuRemote_MigrateEndpoints
from .monitor._item import NodesQemuMonitorEndpoints
from .resize._item import NodesQemuResizeEndpoints
from .snapshot._item import NodesQemuSnapshotEndpoints
from .template._item import NodesQemuTemplateEndpoints
from .mtunnel._item import NodesQemuMtunnelEndpoints
from .mtunnelwebsocket._item import NodesQemuMtunnelwebsocketEndpoints
from prmxctrl.models.nodes import Nodes_Node_Qemu_VmidDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_VmidDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_VmidGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_VmidGETResponse  # type: ignore

class NodesQemuEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}
    """

    # Sub-endpoint properties
    @property
    def firewall(self) -> NodesQemuFirewallEndpoints:
        """Access firewall endpoints"""
        from .firewall._item import NodesQemuFirewallEndpoints  # type: ignore
        return NodesQemuFirewallEndpoints(self._client, self._build_path("firewall"))
    @property
    def agent(self) -> NodesQemuAgentEndpoints:
        """Access agent endpoints"""
        from .agent._item import NodesQemuAgentEndpoints  # type: ignore
        return NodesQemuAgentEndpoints(self._client, self._build_path("agent"))
    @property
    def rrd(self) -> NodesQemuRrdEndpoints:
        """Access rrd endpoints"""
        from .rrd._item import NodesQemuRrdEndpoints  # type: ignore
        return NodesQemuRrdEndpoints(self._client, self._build_path("rrd"))
    @property
    def rrddata(self) -> NodesQemuRrddataEndpoints:
        """Access rrddata endpoints"""
        from .rrddata._item import NodesQemuRrddataEndpoints  # type: ignore
        return NodesQemuRrddataEndpoints(self._client, self._build_path("rrddata"))
    @property
    def config(self) -> NodesQemuConfigEndpoints:
        """Access config endpoints"""
        from .config._item import NodesQemuConfigEndpoints  # type: ignore
        return NodesQemuConfigEndpoints(self._client, self._build_path("config"))
    @property
    def pending(self) -> NodesQemuPendingEndpoints:
        """Access pending endpoints"""
        from .pending._item import NodesQemuPendingEndpoints  # type: ignore
        return NodesQemuPendingEndpoints(self._client, self._build_path("pending"))
    @property
    def cloudinit(self) -> NodesQemuCloudinitEndpoints:
        """Access cloudinit endpoints"""
        from .cloudinit._item import NodesQemuCloudinitEndpoints  # type: ignore
        return NodesQemuCloudinitEndpoints(self._client, self._build_path("cloudinit"))
    @property
    def unlink(self) -> NodesQemuUnlinkEndpoints:
        """Access unlink endpoints"""
        from .unlink._item import NodesQemuUnlinkEndpoints  # type: ignore
        return NodesQemuUnlinkEndpoints(self._client, self._build_path("unlink"))
    @property
    def vncproxy(self) -> NodesQemuVncproxyEndpoints:
        """Access vncproxy endpoints"""
        from .vncproxy._item import NodesQemuVncproxyEndpoints  # type: ignore
        return NodesQemuVncproxyEndpoints(self._client, self._build_path("vncproxy"))
    @property
    def termproxy(self) -> NodesQemuTermproxyEndpoints:
        """Access termproxy endpoints"""
        from .termproxy._item import NodesQemuTermproxyEndpoints  # type: ignore
        return NodesQemuTermproxyEndpoints(self._client, self._build_path("termproxy"))
    @property
    def vncwebsocket(self) -> NodesQemuVncwebsocketEndpoints:
        """Access vncwebsocket endpoints"""
        from .vncwebsocket._item import NodesQemuVncwebsocketEndpoints  # type: ignore
        return NodesQemuVncwebsocketEndpoints(self._client, self._build_path("vncwebsocket"))
    @property
    def spiceproxy(self) -> NodesQemuSpiceproxyEndpoints:
        """Access spiceproxy endpoints"""
        from .spiceproxy._item import NodesQemuSpiceproxyEndpoints  # type: ignore
        return NodesQemuSpiceproxyEndpoints(self._client, self._build_path("spiceproxy"))
    @property
    def status(self) -> NodesQemuStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesQemuStatusEndpoints  # type: ignore
        return NodesQemuStatusEndpoints(self._client, self._build_path("status"))
    @property
    def sendkey(self) -> NodesQemuSendkeyEndpoints:
        """Access sendkey endpoints"""
        from .sendkey._item import NodesQemuSendkeyEndpoints  # type: ignore
        return NodesQemuSendkeyEndpoints(self._client, self._build_path("sendkey"))
    @property
    def feature(self) -> NodesQemuFeatureEndpoints:
        """Access feature endpoints"""
        from .feature._item import NodesQemuFeatureEndpoints  # type: ignore
        return NodesQemuFeatureEndpoints(self._client, self._build_path("feature"))
    @property
    def clone(self) -> NodesQemuCloneEndpoints:
        """Access clone endpoints"""
        from .clone._item import NodesQemuCloneEndpoints  # type: ignore
        return NodesQemuCloneEndpoints(self._client, self._build_path("clone"))
    @property
    def move_disk(self) -> NodesQemuMove_DiskEndpoints:
        """Access move_disk endpoints"""
        from .move_disk._item import NodesQemuMove_DiskEndpoints  # type: ignore
        return NodesQemuMove_DiskEndpoints(self._client, self._build_path("move_disk"))
    @property
    def migrate(self) -> NodesQemuMigrateEndpoints:
        """Access migrate endpoints"""
        from .migrate._item import NodesQemuMigrateEndpoints  # type: ignore
        return NodesQemuMigrateEndpoints(self._client, self._build_path("migrate"))
    @property
    def remote_migrate(self) -> NodesQemuRemote_MigrateEndpoints:
        """Access remote_migrate endpoints"""
        from .remote_migrate._item import NodesQemuRemote_MigrateEndpoints  # type: ignore
        return NodesQemuRemote_MigrateEndpoints(self._client, self._build_path("remote_migrate"))
    @property
    def monitor(self) -> NodesQemuMonitorEndpoints:
        """Access monitor endpoints"""
        from .monitor._item import NodesQemuMonitorEndpoints  # type: ignore
        return NodesQemuMonitorEndpoints(self._client, self._build_path("monitor"))
    @property
    def resize(self) -> NodesQemuResizeEndpoints:
        """Access resize endpoints"""
        from .resize._item import NodesQemuResizeEndpoints  # type: ignore
        return NodesQemuResizeEndpoints(self._client, self._build_path("resize"))
    @property
    def snapshot(self) -> NodesQemuSnapshotEndpoints:
        """Access snapshot endpoints"""
        from .snapshot._item import NodesQemuSnapshotEndpoints  # type: ignore
        return NodesQemuSnapshotEndpoints(self._client, self._build_path("snapshot"))
    @property
    def template(self) -> NodesQemuTemplateEndpoints:
        """Access template endpoints"""
        from .template._item import NodesQemuTemplateEndpoints  # type: ignore
        return NodesQemuTemplateEndpoints(self._client, self._build_path("template"))
    @property
    def mtunnel(self) -> NodesQemuMtunnelEndpoints:
        """Access mtunnel endpoints"""
        from .mtunnel._item import NodesQemuMtunnelEndpoints  # type: ignore
        return NodesQemuMtunnelEndpoints(self._client, self._build_path("mtunnel"))
    @property
    def mtunnelwebsocket(self) -> NodesQemuMtunnelwebsocketEndpoints:
        """Access mtunnelwebsocket endpoints"""
        from .mtunnelwebsocket._item import NodesQemuMtunnelwebsocketEndpoints  # type: ignore
        return NodesQemuMtunnelwebsocketEndpoints(self._client, self._build_path("mtunnelwebsocket"))



    async def delete(self, params: Nodes_Node_Qemu_VmidDELETERequest | None = None) -> Nodes_Node_Qemu_VmidDELETEResponse:
        """
        Destroy the VM and  all used/owned volumes. Removes any VM specific permissions and firewall rules

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Qemu_VmidGETRequest | None = None) -> Nodes_Node_Qemu_VmidGETResponse:
        """
        Directory index

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

