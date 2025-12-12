"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Cloudinit_DumpGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Cloudinit_DumpGETResponse  # type: ignore

class NodesQemuCloudinitDumpEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/cloudinit/dump
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_Cloudinit_DumpGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Cloudinit_DumpGETResponse:
        """
        Get automatically generated cloudinit config.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

