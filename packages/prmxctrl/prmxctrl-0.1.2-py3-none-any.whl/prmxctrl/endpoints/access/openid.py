"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..openid.auth_url import AccessOpenidAuth_UrlEndpoints
from ..openid.login import AccessOpenidLoginEndpoints
from prmxctrl.models.access import Access_OpenidGETResponse  # type: ignore

class AccessOpenidEndpoints(EndpointBase):
    """
    Endpoint class for /access/openid
    """

    # Sub-endpoint properties
    @property
    def auth_url(self) -> AccessOpenidAuth_UrlEndpoints:
        """Access auth-url endpoints"""
        from ..openid.auth_url import AccessOpenidAuth_UrlEndpoints  # type: ignore
        return AccessOpenidAuth_UrlEndpoints(self._client, self._build_path("auth-url"))
    @property
    def login(self) -> AccessOpenidLoginEndpoints:
        """Access login endpoints"""
        from ..openid.login import AccessOpenidLoginEndpoints  # type: ignore
        return AccessOpenidLoginEndpoints(self._client, self._build_path("login"))



    async def list(self, ) -> Access_OpenidGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get()

