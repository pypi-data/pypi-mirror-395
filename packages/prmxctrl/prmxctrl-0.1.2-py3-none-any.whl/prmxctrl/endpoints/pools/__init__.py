"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .poolid_item._item import PoolsEndpoints1
from prmxctrl.models.pools import PoolsGETResponse
from prmxctrl.models.pools import PoolsPOSTRequest  # type: ignore

class PoolsEndpoints(EndpointBase):
    """
    Root endpoint class for pools API endpoints.
    """


    def __call__(self, poolid: int) -> PoolsEndpoints1:
        """Access specific poolid"""
        from .poolid_item._item import PoolsEndpoints1  # type: ignore
        return PoolsEndpoints1(
            self._client,
            self._build_path(str(poolid))
        )


    async def list(self, ) -> PoolsGETResponse:
        """
        Pool index.

        HTTP Method: GET
        """
        return await self._get()

    async def create_pool(self, params: PoolsPOSTRequest | None = None) -> Any:
        """
        Create new pool.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

