"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Tfa_Userid_IdDELETERequest
from prmxctrl.models.access import Access_Tfa_Userid_IdGETRequest
from prmxctrl.models.access import Access_Tfa_Userid_IdGETResponse
from prmxctrl.models.access import Access_Tfa_Userid_IdPUTRequest  # type: ignore

class AccessTfaEndpoints2(EndpointBase):
    """
    Endpoint class for /access/tfa/{userid}/{id}
    """



    async def delete(self, params: Access_Tfa_Userid_IdDELETERequest | None = None) -> Any:
        """
        Delete a TFA entry by ID.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Access_Tfa_Userid_IdGETRequest | None = None) -> Access_Tfa_Userid_IdGETResponse:
        """
        Fetch a requested TFA entry if present.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_tfa_entry(self, params: Access_Tfa_Userid_IdPUTRequest | None = None) -> Any:
        """
        Add a TFA entry for a user.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

