"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .storage_item._item import StorageEndpoints1
from prmxctrl.models.storage import StorageGETRequest
from prmxctrl.models.storage import StorageGETResponse
from prmxctrl.models.storage import StoragePOSTRequest
from prmxctrl.models.storage import StoragePOSTResponse  # type: ignore

class StorageEndpoints(EndpointBase):
    """
    Root endpoint class for storage API endpoints.
    """


    def __call__(self, storage: str) -> StorageEndpoints1:
        """Access specific storage"""
        from .storage_item._item import StorageEndpoints1  # type: ignore
        return StorageEndpoints1(
            self._client,
            self._build_path(str(storage))
        )


    async def list(self, params: StorageGETRequest | None = None) -> StorageGETResponse:
        """
        Storage index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: StoragePOSTRequest | None = None) -> StoragePOSTResponse:
        """
        Create a new storage.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

