"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesQemuFirewallIpsetEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_IpsetGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_IpsetGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_IpsetPOSTRequest  # type: ignore

class NodesQemuFirewallIpsetEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/firewall/ipset
    """


    def __call__(self, name: str) -> NodesQemuFirewallIpsetEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesQemuFirewallIpsetEndpoints1  # type: ignore
        return NodesQemuFirewallIpsetEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Qemu_Vmid_Firewall_IpsetGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Firewall_IpsetGETResponse:
        """
        List IPSets

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_ipset(self, params: Nodes_Node_Qemu_Vmid_Firewall_IpsetPOSTRequest | None = None) -> Any:
        """
        Create new IPSet

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

