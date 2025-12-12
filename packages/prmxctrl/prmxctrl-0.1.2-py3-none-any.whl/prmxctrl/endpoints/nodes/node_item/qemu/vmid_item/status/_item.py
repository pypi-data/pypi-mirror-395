"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .current._item import NodesQemuStatusCurrentEndpoints
from .start._item import NodesQemuStatusStartEndpoints
from .stop._item import NodesQemuStatusStopEndpoints
from .reset._item import NodesQemuStatusResetEndpoints
from .shutdown._item import NodesQemuStatusShutdownEndpoints
from .reboot._item import NodesQemuStatusRebootEndpoints
from .suspend._item import NodesQemuStatusSuspendEndpoints
from .resume._item import NodesQemuStatusResumeEndpoints
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_StatusGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_StatusGETResponse  # type: ignore

class NodesQemuStatusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/status
    """

    # Sub-endpoint properties
    @property
    def current(self) -> NodesQemuStatusCurrentEndpoints:
        """Access current endpoints"""
        from .current._item import NodesQemuStatusCurrentEndpoints  # type: ignore
        return NodesQemuStatusCurrentEndpoints(self._client, self._build_path("current"))
    @property
    def start(self) -> NodesQemuStatusStartEndpoints:
        """Access start endpoints"""
        from .start._item import NodesQemuStatusStartEndpoints  # type: ignore
        return NodesQemuStatusStartEndpoints(self._client, self._build_path("start"))
    @property
    def stop(self) -> NodesQemuStatusStopEndpoints:
        """Access stop endpoints"""
        from .stop._item import NodesQemuStatusStopEndpoints  # type: ignore
        return NodesQemuStatusStopEndpoints(self._client, self._build_path("stop"))
    @property
    def reset(self) -> NodesQemuStatusResetEndpoints:
        """Access reset endpoints"""
        from .reset._item import NodesQemuStatusResetEndpoints  # type: ignore
        return NodesQemuStatusResetEndpoints(self._client, self._build_path("reset"))
    @property
    def shutdown(self) -> NodesQemuStatusShutdownEndpoints:
        """Access shutdown endpoints"""
        from .shutdown._item import NodesQemuStatusShutdownEndpoints  # type: ignore
        return NodesQemuStatusShutdownEndpoints(self._client, self._build_path("shutdown"))
    @property
    def reboot(self) -> NodesQemuStatusRebootEndpoints:
        """Access reboot endpoints"""
        from .reboot._item import NodesQemuStatusRebootEndpoints  # type: ignore
        return NodesQemuStatusRebootEndpoints(self._client, self._build_path("reboot"))
    @property
    def suspend(self) -> NodesQemuStatusSuspendEndpoints:
        """Access suspend endpoints"""
        from .suspend._item import NodesQemuStatusSuspendEndpoints  # type: ignore
        return NodesQemuStatusSuspendEndpoints(self._client, self._build_path("suspend"))
    @property
    def resume(self) -> NodesQemuStatusResumeEndpoints:
        """Access resume endpoints"""
        from .resume._item import NodesQemuStatusResumeEndpoints  # type: ignore
        return NodesQemuStatusResumeEndpoints(self._client, self._build_path("resume"))



    async def list(self, params: Nodes_Node_Qemu_Vmid_StatusGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_StatusGETResponse:
        """
        Directory index

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

