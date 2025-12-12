"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .userid_item._item import AccessUsersEndpoints1
from prmxctrl.models.access import Access_UsersGETRequest
from prmxctrl.models.access import Access_UsersGETResponse
from prmxctrl.models.access import Access_UsersPOSTRequest  # type: ignore

class AccessUsersEndpoints(EndpointBase):
    """
    Endpoint class for /access/users
    """


    def __call__(self, userid: int) -> AccessUsersEndpoints1:
        """Access specific userid"""
        from .userid_item._item import AccessUsersEndpoints1  # type: ignore
        return AccessUsersEndpoints1(
            self._client,
            self._build_path(str(userid))
        )


    async def list(self, params: Access_UsersGETRequest | None = None) -> Access_UsersGETResponse:
        """
        User index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_user(self, params: Access_UsersPOSTRequest | None = None) -> Any:
        """
        Create new user.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

