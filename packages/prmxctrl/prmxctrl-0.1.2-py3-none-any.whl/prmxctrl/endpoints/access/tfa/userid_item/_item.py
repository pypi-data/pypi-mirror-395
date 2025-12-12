"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Tfa_UseridGETRequest
from prmxctrl.models.access import Access_Tfa_UseridGETResponse
from prmxctrl.models.access import Access_Tfa_UseridPOSTRequest
from prmxctrl.models.access import Access_Tfa_UseridPOSTResponse  # type: ignore

class AccessTfaEndpoints1(EndpointBase):
    """
    Endpoint class for /access/tfa/{userid}
    """



    async def list(self, params: Access_Tfa_UseridGETRequest | None = None) -> Access_Tfa_UseridGETResponse:
        """
        List TFA configurations of users.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def add_tfa_entry(self, params: Access_Tfa_UseridPOSTRequest | None = None) -> Access_Tfa_UseridPOSTResponse:
        """
        Add a TFA entry for a user.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

