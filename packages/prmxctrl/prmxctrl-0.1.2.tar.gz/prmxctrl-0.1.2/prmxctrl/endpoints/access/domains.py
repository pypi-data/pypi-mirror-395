"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .realm_item._item import AccessDomainsEndpoints1
from prmxctrl.models.access import Access_DomainsGETResponse
from prmxctrl.models.access import Access_DomainsPOSTRequest  # type: ignore

class AccessDomainsEndpoints(EndpointBase):
    """
    Endpoint class for /access/domains
    """


    def __call__(self, realm: str) -> AccessDomainsEndpoints1:
        """Access specific realm"""
        from .realm_item._item import AccessDomainsEndpoints1  # type: ignore
        return AccessDomainsEndpoints1(
            self._client,
            self._build_path(str(realm))
        )


    async def list(self, ) -> Access_DomainsGETResponse:
        """
        Authentication domain index.

        HTTP Method: GET
        """
        return await self._get()

    async def create(self, params: Access_DomainsPOSTRequest | None = None) -> Any:
        """
        Add an authentication server.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

