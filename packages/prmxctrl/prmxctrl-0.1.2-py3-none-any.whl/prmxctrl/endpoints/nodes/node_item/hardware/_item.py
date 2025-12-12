"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .pci._item import NodesHardwarePciEndpoints
from .usb._item import NodesHardwareUsbEndpoints
from prmxctrl.models.nodes import Nodes_Node_HardwareGETRequest
from prmxctrl.models.nodes import Nodes_Node_HardwareGETResponse  # type: ignore

class NodesHardwareEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/hardware
    """

    # Sub-endpoint properties
    @property
    def pci(self) -> NodesHardwarePciEndpoints:
        """Access pci endpoints"""
        from .pci._item import NodesHardwarePciEndpoints  # type: ignore
        return NodesHardwarePciEndpoints(self._client, self._build_path("pci"))
    @property
    def usb(self) -> NodesHardwareUsbEndpoints:
        """Access usb endpoints"""
        from .usb._item import NodesHardwareUsbEndpoints  # type: ignore
        return NodesHardwareUsbEndpoints(self._client, self._build_path("usb"))



    async def list(self, params: Nodes_Node_HardwareGETRequest | None = None) -> Nodes_Node_HardwareGETResponse:
        """
        Index of hardware types

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

