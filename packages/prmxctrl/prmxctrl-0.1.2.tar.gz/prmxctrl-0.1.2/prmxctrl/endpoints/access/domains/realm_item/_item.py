"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .sync._item import AccessDomainsSyncEndpoints
from prmxctrl.models.access import Access_Domains_RealmDELETERequest
from prmxctrl.models.access import Access_Domains_RealmGETRequest
from prmxctrl.models.access import Access_Domains_RealmGETResponse
from prmxctrl.models.access import Access_Domains_RealmPUTRequest  # type: ignore

class AccessDomainsEndpoints1(EndpointBase):
    """
    Endpoint class for /access/domains/{realm}
    """

    # Sub-endpoint properties
    @property
    def sync(self) -> AccessDomainsSyncEndpoints:
        """Access sync endpoints"""
        from .sync._item import AccessDomainsSyncEndpoints  # type: ignore
        return AccessDomainsSyncEndpoints(self._client, self._build_path("sync"))



    async def delete(self, params: Access_Domains_RealmDELETERequest | None = None) -> Any:
        """
        Delete an authentication server.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Access_Domains_RealmGETRequest | None = None) -> Access_Domains_RealmGETResponse:
        """
        Get auth server configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Access_Domains_RealmPUTRequest | None = None) -> Any:
        """
        Update authentication server settings.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

