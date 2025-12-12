"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Openid_LoginPOSTRequest
from prmxctrl.models.access import Access_Openid_LoginPOSTResponse  # type: ignore

class AccessOpenidLoginEndpoints(EndpointBase):
    """
    Endpoint class for /access/openid/login
    """



    async def login(self, params: Access_Openid_LoginPOSTRequest | None = None) -> Access_Openid_LoginPOSTResponse:
        """
         Verify OpenID authorization code and create a ticket.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

