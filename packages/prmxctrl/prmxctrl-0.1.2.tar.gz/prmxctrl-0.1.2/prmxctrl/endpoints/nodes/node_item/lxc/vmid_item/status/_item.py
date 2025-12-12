"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .current._item import NodesLxcStatusCurrentEndpoints
from .start._item import NodesLxcStatusStartEndpoints
from .stop._item import NodesLxcStatusStopEndpoints
from .shutdown._item import NodesLxcStatusShutdownEndpoints
from .suspend._item import NodesLxcStatusSuspendEndpoints
from .resume._item import NodesLxcStatusResumeEndpoints
from .reboot._item import NodesLxcStatusRebootEndpoints
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_StatusGETRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_StatusGETResponse  # type: ignore

class NodesLxcStatusEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/status
    """

    # Sub-endpoint properties
    @property
    def current(self) -> NodesLxcStatusCurrentEndpoints:
        """Access current endpoints"""
        from .current._item import NodesLxcStatusCurrentEndpoints  # type: ignore
        return NodesLxcStatusCurrentEndpoints(self._client, self._build_path("current"))
    @property
    def start(self) -> NodesLxcStatusStartEndpoints:
        """Access start endpoints"""
        from .start._item import NodesLxcStatusStartEndpoints  # type: ignore
        return NodesLxcStatusStartEndpoints(self._client, self._build_path("start"))
    @property
    def stop(self) -> NodesLxcStatusStopEndpoints:
        """Access stop endpoints"""
        from .stop._item import NodesLxcStatusStopEndpoints  # type: ignore
        return NodesLxcStatusStopEndpoints(self._client, self._build_path("stop"))
    @property
    def shutdown(self) -> NodesLxcStatusShutdownEndpoints:
        """Access shutdown endpoints"""
        from .shutdown._item import NodesLxcStatusShutdownEndpoints  # type: ignore
        return NodesLxcStatusShutdownEndpoints(self._client, self._build_path("shutdown"))
    @property
    def suspend(self) -> NodesLxcStatusSuspendEndpoints:
        """Access suspend endpoints"""
        from .suspend._item import NodesLxcStatusSuspendEndpoints  # type: ignore
        return NodesLxcStatusSuspendEndpoints(self._client, self._build_path("suspend"))
    @property
    def resume(self) -> NodesLxcStatusResumeEndpoints:
        """Access resume endpoints"""
        from .resume._item import NodesLxcStatusResumeEndpoints  # type: ignore
        return NodesLxcStatusResumeEndpoints(self._client, self._build_path("resume"))
    @property
    def reboot(self) -> NodesLxcStatusRebootEndpoints:
        """Access reboot endpoints"""
        from .reboot._item import NodesLxcStatusRebootEndpoints  # type: ignore
        return NodesLxcStatusRebootEndpoints(self._client, self._build_path("reboot"))



    async def list(self, params: Nodes_Node_Lxc_Vmid_StatusGETRequest | None = None) -> Nodes_Node_Lxc_Vmid_StatusGETResponse:
        """
        Directory index

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

