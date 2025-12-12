"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrPUTRequest  # type: ignore

class NodesQemuFirewallIpsetEndpoints2(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr}
    """



    async def delete(self, params: Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrDELETERequest | None = None) -> Any:
        """
        Remove IP or Network from IPSet.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrGETResponse:
        """
        Read IP or Network settings from IPSet.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_ip(self, params: Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrPUTRequest | None = None) -> Any:
        """
        Update IP or Network settings

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

