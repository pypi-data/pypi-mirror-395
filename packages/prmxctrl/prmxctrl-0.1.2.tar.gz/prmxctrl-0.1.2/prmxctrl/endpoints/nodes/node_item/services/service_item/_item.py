"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .state._item import NodesServicesStateEndpoints
from .start._item import NodesServicesStartEndpoints
from .stop._item import NodesServicesStopEndpoints
from .restart._item import NodesServicesRestartEndpoints
from .reload._item import NodesServicesReloadEndpoints
from prmxctrl.models.nodes import Nodes_Node_Services_ServiceGETRequest
from prmxctrl.models.nodes import Nodes_Node_Services_ServiceGETResponse  # type: ignore

class NodesServicesEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/services/{service}
    """

    # Sub-endpoint properties
    @property
    def state(self) -> NodesServicesStateEndpoints:
        """Access state endpoints"""
        from .state._item import NodesServicesStateEndpoints  # type: ignore
        return NodesServicesStateEndpoints(self._client, self._build_path("state"))
    @property
    def start(self) -> NodesServicesStartEndpoints:
        """Access start endpoints"""
        from .start._item import NodesServicesStartEndpoints  # type: ignore
        return NodesServicesStartEndpoints(self._client, self._build_path("start"))
    @property
    def stop(self) -> NodesServicesStopEndpoints:
        """Access stop endpoints"""
        from .stop._item import NodesServicesStopEndpoints  # type: ignore
        return NodesServicesStopEndpoints(self._client, self._build_path("stop"))
    @property
    def restart(self) -> NodesServicesRestartEndpoints:
        """Access restart endpoints"""
        from .restart._item import NodesServicesRestartEndpoints  # type: ignore
        return NodesServicesRestartEndpoints(self._client, self._build_path("restart"))
    @property
    def reload(self) -> NodesServicesReloadEndpoints:
        """Access reload endpoints"""
        from .reload._item import NodesServicesReloadEndpoints  # type: ignore
        return NodesServicesReloadEndpoints(self._client, self._build_path("reload"))



    async def list(self, params: Nodes_Node_Services_ServiceGETRequest | None = None) -> Nodes_Node_Services_ServiceGETResponse:
        """
        Directory index

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

