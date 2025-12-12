"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_OptionsGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_OptionsGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_OptionsPUTRequest  # type: ignore

class NodesQemuFirewallOptionsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/firewall/options
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_Firewall_OptionsGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Firewall_OptionsGETResponse:
        """
        Get VM firewall options.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def set_options(self, params: Nodes_Node_Qemu_Vmid_Firewall_OptionsPUTRequest | None = None) -> Any:
        """
        Set Firewall options.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

