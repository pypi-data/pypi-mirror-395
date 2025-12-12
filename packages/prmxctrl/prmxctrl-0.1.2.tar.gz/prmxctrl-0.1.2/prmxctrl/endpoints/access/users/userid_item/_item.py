"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .tfa._item import AccessUsersTfaEndpoints
from .token._item import AccessUsersTokenEndpoints
from prmxctrl.models.access import Access_Users_UseridDELETERequest
from prmxctrl.models.access import Access_Users_UseridGETRequest
from prmxctrl.models.access import Access_Users_UseridGETResponse
from prmxctrl.models.access import Access_Users_UseridPUTRequest  # type: ignore

class AccessUsersEndpoints1(EndpointBase):
    """
    Endpoint class for /access/users/{userid}
    """

    # Sub-endpoint properties
    @property
    def tfa(self) -> AccessUsersTfaEndpoints:
        """Access tfa endpoints"""
        from .tfa._item import AccessUsersTfaEndpoints  # type: ignore
        return AccessUsersTfaEndpoints(self._client, self._build_path("tfa"))
    @property
    def token(self) -> AccessUsersTokenEndpoints:
        """Access token endpoints"""
        from .token._item import AccessUsersTokenEndpoints  # type: ignore
        return AccessUsersTokenEndpoints(self._client, self._build_path("token"))



    async def delete(self, params: Access_Users_UseridDELETERequest | None = None) -> Any:
        """
        Delete user.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Access_Users_UseridGETRequest | None = None) -> Access_Users_UseridGETResponse:
        """
        Get user configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_user(self, params: Access_Users_UseridPUTRequest | None = None) -> Any:
        """
        Update user configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

