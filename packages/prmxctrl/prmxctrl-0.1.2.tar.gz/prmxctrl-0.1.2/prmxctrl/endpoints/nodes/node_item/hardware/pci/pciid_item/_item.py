"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .mdev._item import NodesHardwarePciMdevEndpoints
from prmxctrl.models.nodes import Nodes_Node_Hardware_Pci_PciidGETRequest
from prmxctrl.models.nodes import Nodes_Node_Hardware_Pci_PciidGETResponse  # type: ignore

class NodesHardwarePciEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/hardware/pci/{pciid}
    """

    # Sub-endpoint properties
    @property
    def mdev(self) -> NodesHardwarePciMdevEndpoints:
        """Access mdev endpoints"""
        from .mdev._item import NodesHardwarePciMdevEndpoints  # type: ignore
        return NodesHardwarePciMdevEndpoints(self._client, self._build_path("mdev"))



    async def list(self, params: Nodes_Node_Hardware_Pci_PciidGETRequest | None = None) -> Nodes_Node_Hardware_Pci_PciidGETResponse:
        """
        Index of available pci methods

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

