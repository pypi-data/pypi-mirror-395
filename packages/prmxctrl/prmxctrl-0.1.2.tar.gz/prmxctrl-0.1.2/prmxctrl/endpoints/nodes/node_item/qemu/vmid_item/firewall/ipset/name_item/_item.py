"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_NamePOSTRequest  # type: ignore

class NodesQemuFirewallIpsetEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}
    """



    async def delete(self, params: Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameDELETERequest | None = None) -> Any:
        """
        Delete IPSet

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameGETResponse:
        """
        List IPSet content

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_ip(self, params: Nodes_Node_Qemu_Vmid_Firewall_Ipset_NamePOSTRequest | None = None) -> Any:
        """
        Add IP or Network to IPSet.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

