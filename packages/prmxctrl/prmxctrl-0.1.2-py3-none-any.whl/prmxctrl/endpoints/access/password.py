"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_PasswordPUTRequest  # type: ignore

class AccessPasswordEndpoints(EndpointBase):
    """
    Endpoint class for /access/password
    """



    async def change_password(self, params: Access_PasswordPUTRequest | None = None) -> Any:
        """
        Change user password.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

