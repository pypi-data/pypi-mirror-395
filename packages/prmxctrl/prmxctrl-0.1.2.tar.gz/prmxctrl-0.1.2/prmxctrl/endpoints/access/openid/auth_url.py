"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Openid_Auth_UrlPOSTRequest
from prmxctrl.models.access import Access_Openid_Auth_UrlPOSTResponse  # type: ignore

class AccessOpenidAuth_UrlEndpoints(EndpointBase):
    """
    Endpoint class for /access/openid/auth-url
    """



    async def auth_url(self, params: Access_Openid_Auth_UrlPOSTRequest | None = None) -> Access_Openid_Auth_UrlPOSTResponse:
        """
        Get the OpenId Authorization Url for the specified realm.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

