"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Hardware_Pci_Pciid_MdevGETRequest
from prmxctrl.models.nodes import Nodes_Node_Hardware_Pci_Pciid_MdevGETResponse  # type: ignore

class NodesHardwarePciMdevEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/hardware/pci/{pciid}/mdev
    """



    async def list(self, params: Nodes_Node_Hardware_Pci_Pciid_MdevGETRequest | None = None) -> Nodes_Node_Hardware_Pci_Pciid_MdevGETResponse:
        """
        List mediated device types for given PCI device.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

