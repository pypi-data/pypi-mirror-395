"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .dump._item import NodesQemuCloudinitDumpEndpoints
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_CloudinitGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_CloudinitGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_CloudinitPUTRequest  # type: ignore

class NodesQemuCloudinitEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/cloudinit
    """

    # Sub-endpoint properties
    @property
    def dump(self) -> NodesQemuCloudinitDumpEndpoints:
        """Access dump endpoints"""
        from .dump._item import NodesQemuCloudinitDumpEndpoints  # type: ignore
        return NodesQemuCloudinitDumpEndpoints(self._client, self._build_path("dump"))



    async def list(self, params: Nodes_Node_Qemu_Vmid_CloudinitGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_CloudinitGETResponse:
        """
        Get the cloudinit configuration with both current and pending values.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def cloudinit_update(self, params: Nodes_Node_Qemu_Vmid_CloudinitPUTRequest | None = None) -> Any:
        """
        Regenerate and change cloudinit config drive.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

