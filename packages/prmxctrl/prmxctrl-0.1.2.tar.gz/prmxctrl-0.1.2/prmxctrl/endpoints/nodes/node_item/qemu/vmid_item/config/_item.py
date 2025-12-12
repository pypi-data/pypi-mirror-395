"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_ConfigGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_ConfigGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_ConfigPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_ConfigPOSTResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_ConfigPUTRequest  # type: ignore

class NodesQemuConfigEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/config
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_ConfigGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_ConfigGETResponse:
        """
        Get the virtual machine configuration with pending configuration changes applied. Set the 'current' parameter to get the current configuration instead.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_vm_async(self, params: Nodes_Node_Qemu_Vmid_ConfigPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_ConfigPOSTResponse:
        """
        Set virtual machine options (asynchrounous API).

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_vm(self, params: Nodes_Node_Qemu_Vmid_ConfigPUTRequest | None = None) -> Any:
        """
        Set virtual machine options (synchrounous API) - You should consider using the POST method instead for any actions involving hotplug or storage allocation.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

