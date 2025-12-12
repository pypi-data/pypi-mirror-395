"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Users_Userid_Token_TokenidDELETERequest
from prmxctrl.models.access import Access_Users_Userid_Token_TokenidGETRequest
from prmxctrl.models.access import Access_Users_Userid_Token_TokenidGETResponse
from prmxctrl.models.access import Access_Users_Userid_Token_TokenidPOSTRequest
from prmxctrl.models.access import Access_Users_Userid_Token_TokenidPOSTResponse
from prmxctrl.models.access import Access_Users_Userid_Token_TokenidPUTRequest
from prmxctrl.models.access import Access_Users_Userid_Token_TokenidPUTResponse  # type: ignore

class AccessUsersTokenEndpoints1(EndpointBase):
    """
    Endpoint class for /access/users/{userid}/token/{tokenid}
    """



    async def delete(self, params: Access_Users_Userid_Token_TokenidDELETERequest | None = None) -> Any:
        """
        Remove API token for a specific user.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Access_Users_Userid_Token_TokenidGETRequest | None = None) -> Access_Users_Userid_Token_TokenidGETResponse:
        """
        Get specific API token information.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def generate_token(self, params: Access_Users_Userid_Token_TokenidPOSTRequest | None = None) -> Access_Users_Userid_Token_TokenidPOSTResponse:
        """
        Generate a new API token for a specific user. NOTE: returns API token value, which needs to be stored as it cannot be retrieved afterwards!

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_token_info(self, params: Access_Users_Userid_Token_TokenidPUTRequest | None = None) -> Access_Users_Userid_Token_TokenidPUTResponse:
        """
        Update API token for a specific user.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

