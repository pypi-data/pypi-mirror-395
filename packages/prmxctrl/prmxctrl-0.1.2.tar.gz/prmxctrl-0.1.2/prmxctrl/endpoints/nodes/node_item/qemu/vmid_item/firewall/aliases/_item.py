"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesQemuFirewallAliasesEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_AliasesGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_AliasesGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_AliasesPOSTRequest  # type: ignore

class NodesQemuFirewallAliasesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/firewall/aliases
    """


    def __call__(self, name: str) -> NodesQemuFirewallAliasesEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesQemuFirewallAliasesEndpoints1  # type: ignore
        return NodesQemuFirewallAliasesEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Qemu_Vmid_Firewall_AliasesGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Firewall_AliasesGETResponse:
        """
        List aliases

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_alias(self, params: Nodes_Node_Qemu_Vmid_Firewall_AliasesPOSTRequest | None = None) -> Any:
        """
        Create IP or Network Alias.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

