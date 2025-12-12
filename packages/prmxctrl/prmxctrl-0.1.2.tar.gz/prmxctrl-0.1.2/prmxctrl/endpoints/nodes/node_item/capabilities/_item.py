"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .qemu._item import NodesCapabilitiesQemuEndpoints
from prmxctrl.models.nodes import Nodes_Node_CapabilitiesGETRequest
from prmxctrl.models.nodes import Nodes_Node_CapabilitiesGETResponse  # type: ignore

class NodesCapabilitiesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/capabilities
    """

    # Sub-endpoint properties
    @property
    def qemu(self) -> NodesCapabilitiesQemuEndpoints:
        """Access qemu endpoints"""
        from .qemu._item import NodesCapabilitiesQemuEndpoints  # type: ignore
        return NodesCapabilitiesQemuEndpoints(self._client, self._build_path("qemu"))



    async def list(self, params: Nodes_Node_CapabilitiesGETRequest | None = None) -> Nodes_Node_CapabilitiesGETResponse:
        """
        Node capabilities index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

