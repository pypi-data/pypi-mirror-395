"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Users_Userid_TfaGETRequest
from prmxctrl.models.access import Access_Users_Userid_TfaGETResponse  # type: ignore

class AccessUsersTfaEndpoints(EndpointBase):
    """
    Endpoint class for /access/users/{userid}/tfa
    """



    async def get(self, params: Access_Users_Userid_TfaGETRequest | None = None) -> Access_Users_Userid_TfaGETResponse:
        """
        Get user TFA types (Personal and Realm).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

