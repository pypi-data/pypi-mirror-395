"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.storage import Storage_StorageDELETERequest
from prmxctrl.models.storage import Storage_StorageGETRequest
from prmxctrl.models.storage import Storage_StorageGETResponse
from prmxctrl.models.storage import Storage_StoragePUTRequest
from prmxctrl.models.storage import Storage_StoragePUTResponse  # type: ignore

class StorageEndpoints1(EndpointBase):
    """
    Endpoint class for /storage/{storage}
    """



    async def delete(self, params: Storage_StorageDELETERequest | None = None) -> Any:
        """
        Delete storage configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Storage_StorageGETRequest | None = None) -> Storage_StorageGETResponse:
        """
        Read storage configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Storage_StoragePUTRequest | None = None) -> Storage_StoragePUTResponse:
        """
        Update storage configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

