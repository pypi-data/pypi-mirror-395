"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .tokenid_item._item import AccessUsersTokenEndpoints1
from prmxctrl.models.access import Access_Users_Userid_TokenGETRequest
from prmxctrl.models.access import Access_Users_Userid_TokenGETResponse  # type: ignore

class AccessUsersTokenEndpoints(EndpointBase):
    """
    Endpoint class for /access/users/{userid}/token
    """


    def __call__(self, tokenid: int) -> AccessUsersTokenEndpoints1:
        """Access specific tokenid"""
        from .tokenid_item._item import AccessUsersTokenEndpoints1  # type: ignore
        return AccessUsersTokenEndpoints1(
            self._client,
            self._build_path(str(tokenid))
        )


    async def list(self, params: Access_Users_Userid_TokenGETRequest | None = None) -> Access_Users_Userid_TokenGETResponse:
        """
        Get user API tokens.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

