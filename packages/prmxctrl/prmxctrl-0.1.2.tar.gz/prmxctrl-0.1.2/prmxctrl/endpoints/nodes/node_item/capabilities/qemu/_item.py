"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .cpu._item import NodesCapabilitiesQemuCpuEndpoints
from .machines._item import NodesCapabilitiesQemuMachinesEndpoints
from prmxctrl.models.nodes import Nodes_Node_Capabilities_QemuGETRequest
from prmxctrl.models.nodes import Nodes_Node_Capabilities_QemuGETResponse  # type: ignore

class NodesCapabilitiesQemuEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/capabilities/qemu
    """

    # Sub-endpoint properties
    @property
    def cpu(self) -> NodesCapabilitiesQemuCpuEndpoints:
        """Access cpu endpoints"""
        from .cpu._item import NodesCapabilitiesQemuCpuEndpoints  # type: ignore
        return NodesCapabilitiesQemuCpuEndpoints(self._client, self._build_path("cpu"))
    @property
    def machines(self) -> NodesCapabilitiesQemuMachinesEndpoints:
        """Access machines endpoints"""
        from .machines._item import NodesCapabilitiesQemuMachinesEndpoints  # type: ignore
        return NodesCapabilitiesQemuMachinesEndpoints(self._client, self._build_path("machines"))



    async def list(self, params: Nodes_Node_Capabilities_QemuGETRequest | None = None) -> Nodes_Node_Capabilities_QemuGETResponse:
        """
        QEMU capabilities index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

