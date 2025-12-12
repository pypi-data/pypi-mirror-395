"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .fsfreeze_freeze._item import NodesQemuAgentFsfreeze_FreezeEndpoints
from .fsfreeze_status._item import NodesQemuAgentFsfreeze_StatusEndpoints
from .fsfreeze_thaw._item import NodesQemuAgentFsfreeze_ThawEndpoints
from .fstrim._item import NodesQemuAgentFstrimEndpoints
from .get_fsinfo._item import NodesQemuAgentGet_FsinfoEndpoints
from .get_host_name._item import NodesQemuAgentGet_Host_NameEndpoints
from .get_memory_block_info._item import NodesQemuAgentGet_Memory_Block_InfoEndpoints
from .get_memory_blocks._item import NodesQemuAgentGet_Memory_BlocksEndpoints
from .get_osinfo._item import NodesQemuAgentGet_OsinfoEndpoints
from .get_time._item import NodesQemuAgentGet_TimeEndpoints
from .get_timezone._item import NodesQemuAgentGet_TimezoneEndpoints
from .get_users._item import NodesQemuAgentGet_UsersEndpoints
from .get_vcpus._item import NodesQemuAgentGet_VcpusEndpoints
from .info._item import NodesQemuAgentInfoEndpoints
from .network_get_interfaces._item import NodesQemuAgentNetwork_Get_InterfacesEndpoints
from .ping._item import NodesQemuAgentPingEndpoints
from .shutdown._item import NodesQemuAgentShutdownEndpoints
from .suspend_disk._item import NodesQemuAgentSuspend_DiskEndpoints
from .suspend_hybrid._item import NodesQemuAgentSuspend_HybridEndpoints
from .suspend_ram._item import NodesQemuAgentSuspend_RamEndpoints
from .set_user_password._item import NodesQemuAgentSet_User_PasswordEndpoints
from .exec._item import NodesQemuAgentExecEndpoints
from .exec_status._item import NodesQemuAgentExec_StatusEndpoints
from .file_read._item import NodesQemuAgentFile_ReadEndpoints
from .file_write._item import NodesQemuAgentFile_WriteEndpoints
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_AgentGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_AgentGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_AgentPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_AgentPOSTResponse  # type: ignore

class NodesQemuAgentEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent
    """

    # Sub-endpoint properties
    @property
    def fsfreeze_freeze(self) -> NodesQemuAgentFsfreeze_FreezeEndpoints:
        """Access fsfreeze-freeze endpoints"""
        from .fsfreeze_freeze._item import NodesQemuAgentFsfreeze_FreezeEndpoints  # type: ignore
        return NodesQemuAgentFsfreeze_FreezeEndpoints(self._client, self._build_path("fsfreeze-freeze"))
    @property
    def fsfreeze_status(self) -> NodesQemuAgentFsfreeze_StatusEndpoints:
        """Access fsfreeze-status endpoints"""
        from .fsfreeze_status._item import NodesQemuAgentFsfreeze_StatusEndpoints  # type: ignore
        return NodesQemuAgentFsfreeze_StatusEndpoints(self._client, self._build_path("fsfreeze-status"))
    @property
    def fsfreeze_thaw(self) -> NodesQemuAgentFsfreeze_ThawEndpoints:
        """Access fsfreeze-thaw endpoints"""
        from .fsfreeze_thaw._item import NodesQemuAgentFsfreeze_ThawEndpoints  # type: ignore
        return NodesQemuAgentFsfreeze_ThawEndpoints(self._client, self._build_path("fsfreeze-thaw"))
    @property
    def fstrim(self) -> NodesQemuAgentFstrimEndpoints:
        """Access fstrim endpoints"""
        from .fstrim._item import NodesQemuAgentFstrimEndpoints  # type: ignore
        return NodesQemuAgentFstrimEndpoints(self._client, self._build_path("fstrim"))
    @property
    def get_fsinfo(self) -> NodesQemuAgentGet_FsinfoEndpoints:
        """Access get-fsinfo endpoints"""
        from .get_fsinfo._item import NodesQemuAgentGet_FsinfoEndpoints  # type: ignore
        return NodesQemuAgentGet_FsinfoEndpoints(self._client, self._build_path("get-fsinfo"))
    @property
    def get_host_name(self) -> NodesQemuAgentGet_Host_NameEndpoints:
        """Access get-host-name endpoints"""
        from .get_host_name._item import NodesQemuAgentGet_Host_NameEndpoints  # type: ignore
        return NodesQemuAgentGet_Host_NameEndpoints(self._client, self._build_path("get-host-name"))
    @property
    def get_memory_block_info(self) -> NodesQemuAgentGet_Memory_Block_InfoEndpoints:
        """Access get-memory-block-info endpoints"""
        from .get_memory_block_info._item import NodesQemuAgentGet_Memory_Block_InfoEndpoints  # type: ignore
        return NodesQemuAgentGet_Memory_Block_InfoEndpoints(self._client, self._build_path("get-memory-block-info"))
    @property
    def get_memory_blocks(self) -> NodesQemuAgentGet_Memory_BlocksEndpoints:
        """Access get-memory-blocks endpoints"""
        from .get_memory_blocks._item import NodesQemuAgentGet_Memory_BlocksEndpoints  # type: ignore
        return NodesQemuAgentGet_Memory_BlocksEndpoints(self._client, self._build_path("get-memory-blocks"))
    @property
    def get_osinfo(self) -> NodesQemuAgentGet_OsinfoEndpoints:
        """Access get-osinfo endpoints"""
        from .get_osinfo._item import NodesQemuAgentGet_OsinfoEndpoints  # type: ignore
        return NodesQemuAgentGet_OsinfoEndpoints(self._client, self._build_path("get-osinfo"))
    @property
    def get_time(self) -> NodesQemuAgentGet_TimeEndpoints:
        """Access get-time endpoints"""
        from .get_time._item import NodesQemuAgentGet_TimeEndpoints  # type: ignore
        return NodesQemuAgentGet_TimeEndpoints(self._client, self._build_path("get-time"))
    @property
    def get_timezone(self) -> NodesQemuAgentGet_TimezoneEndpoints:
        """Access get-timezone endpoints"""
        from .get_timezone._item import NodesQemuAgentGet_TimezoneEndpoints  # type: ignore
        return NodesQemuAgentGet_TimezoneEndpoints(self._client, self._build_path("get-timezone"))
    @property
    def get_users(self) -> NodesQemuAgentGet_UsersEndpoints:
        """Access get-users endpoints"""
        from .get_users._item import NodesQemuAgentGet_UsersEndpoints  # type: ignore
        return NodesQemuAgentGet_UsersEndpoints(self._client, self._build_path("get-users"))
    @property
    def get_vcpus(self) -> NodesQemuAgentGet_VcpusEndpoints:
        """Access get-vcpus endpoints"""
        from .get_vcpus._item import NodesQemuAgentGet_VcpusEndpoints  # type: ignore
        return NodesQemuAgentGet_VcpusEndpoints(self._client, self._build_path("get-vcpus"))
    @property
    def info(self) -> NodesQemuAgentInfoEndpoints:
        """Access info endpoints"""
        from .info._item import NodesQemuAgentInfoEndpoints  # type: ignore
        return NodesQemuAgentInfoEndpoints(self._client, self._build_path("info"))
    @property
    def network_get_interfaces(self) -> NodesQemuAgentNetwork_Get_InterfacesEndpoints:
        """Access network-get-interfaces endpoints"""
        from .network_get_interfaces._item import NodesQemuAgentNetwork_Get_InterfacesEndpoints  # type: ignore
        return NodesQemuAgentNetwork_Get_InterfacesEndpoints(self._client, self._build_path("network-get-interfaces"))
    @property
    def ping(self) -> NodesQemuAgentPingEndpoints:
        """Access ping endpoints"""
        from .ping._item import NodesQemuAgentPingEndpoints  # type: ignore
        return NodesQemuAgentPingEndpoints(self._client, self._build_path("ping"))
    @property
    def shutdown(self) -> NodesQemuAgentShutdownEndpoints:
        """Access shutdown endpoints"""
        from .shutdown._item import NodesQemuAgentShutdownEndpoints  # type: ignore
        return NodesQemuAgentShutdownEndpoints(self._client, self._build_path("shutdown"))
    @property
    def suspend_disk(self) -> NodesQemuAgentSuspend_DiskEndpoints:
        """Access suspend-disk endpoints"""
        from .suspend_disk._item import NodesQemuAgentSuspend_DiskEndpoints  # type: ignore
        return NodesQemuAgentSuspend_DiskEndpoints(self._client, self._build_path("suspend-disk"))
    @property
    def suspend_hybrid(self) -> NodesQemuAgentSuspend_HybridEndpoints:
        """Access suspend-hybrid endpoints"""
        from .suspend_hybrid._item import NodesQemuAgentSuspend_HybridEndpoints  # type: ignore
        return NodesQemuAgentSuspend_HybridEndpoints(self._client, self._build_path("suspend-hybrid"))
    @property
    def suspend_ram(self) -> NodesQemuAgentSuspend_RamEndpoints:
        """Access suspend-ram endpoints"""
        from .suspend_ram._item import NodesQemuAgentSuspend_RamEndpoints  # type: ignore
        return NodesQemuAgentSuspend_RamEndpoints(self._client, self._build_path("suspend-ram"))
    @property
    def set_user_password(self) -> NodesQemuAgentSet_User_PasswordEndpoints:
        """Access set-user-password endpoints"""
        from .set_user_password._item import NodesQemuAgentSet_User_PasswordEndpoints  # type: ignore
        return NodesQemuAgentSet_User_PasswordEndpoints(self._client, self._build_path("set-user-password"))
    @property
    def exec(self) -> NodesQemuAgentExecEndpoints:
        """Access exec endpoints"""
        from .exec._item import NodesQemuAgentExecEndpoints  # type: ignore
        return NodesQemuAgentExecEndpoints(self._client, self._build_path("exec"))
    @property
    def exec_status(self) -> NodesQemuAgentExec_StatusEndpoints:
        """Access exec-status endpoints"""
        from .exec_status._item import NodesQemuAgentExec_StatusEndpoints  # type: ignore
        return NodesQemuAgentExec_StatusEndpoints(self._client, self._build_path("exec-status"))
    @property
    def file_read(self) -> NodesQemuAgentFile_ReadEndpoints:
        """Access file-read endpoints"""
        from .file_read._item import NodesQemuAgentFile_ReadEndpoints  # type: ignore
        return NodesQemuAgentFile_ReadEndpoints(self._client, self._build_path("file-read"))
    @property
    def file_write(self) -> NodesQemuAgentFile_WriteEndpoints:
        """Access file-write endpoints"""
        from .file_write._item import NodesQemuAgentFile_WriteEndpoints  # type: ignore
        return NodesQemuAgentFile_WriteEndpoints(self._client, self._build_path("file-write"))



    async def list(self, params: Nodes_Node_Qemu_Vmid_AgentGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_AgentGETResponse:
        """
        QEMU Guest Agent command index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def agent(self, params: Nodes_Node_Qemu_Vmid_AgentPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_AgentPOSTResponse:
        """
        Execute QEMU Guest Agent commands.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

