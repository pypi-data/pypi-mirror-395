"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.pools import Pools_PoolidDELETERequest
from prmxctrl.models.pools import Pools_PoolidGETRequest
from prmxctrl.models.pools import Pools_PoolidGETResponse
from prmxctrl.models.pools import Pools_PoolidPUTRequest  # type: ignore

class PoolsEndpoints1(EndpointBase):
    """
    Endpoint class for /pools/{poolid}
    """



    async def delete(self, params: Pools_PoolidDELETERequest | None = None) -> Any:
        """
        Delete pool.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Pools_PoolidGETRequest | None = None) -> Pools_PoolidGETResponse:
        """
        Get pool configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_pool(self, params: Pools_PoolidPUTRequest | None = None) -> Any:
        """
        Update pool data.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

