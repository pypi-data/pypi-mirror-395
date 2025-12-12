"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .pciid_item._item import NodesHardwarePciEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Hardware_PciGETRequest
from prmxctrl.models.nodes import Nodes_Node_Hardware_PciGETResponse  # type: ignore

class NodesHardwarePciEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/hardware/pci
    """


    def __call__(self, pciid: int) -> NodesHardwarePciEndpoints1:
        """Access specific pciid"""
        from .pciid_item._item import NodesHardwarePciEndpoints1  # type: ignore
        return NodesHardwarePciEndpoints1(
            self._client,
            self._build_path(str(pciid))
        )


    async def list(self, params: Nodes_Node_Hardware_PciGETRequest | None = None) -> Nodes_Node_Hardware_PciGETResponse:
        """
        List local PCI devices.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

