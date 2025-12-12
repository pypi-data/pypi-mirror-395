"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Set_User_PasswordPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Agent_Set_User_PasswordPOSTResponse  # type: ignore

class NodesQemuAgentSet_User_PasswordEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/agent/set-user-password
    """



    async def set_user_password(self, params: Nodes_Node_Qemu_Vmid_Agent_Set_User_PasswordPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Agent_Set_User_PasswordPOSTResponse:
        """
        Sets the password for the given user to the given password

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

