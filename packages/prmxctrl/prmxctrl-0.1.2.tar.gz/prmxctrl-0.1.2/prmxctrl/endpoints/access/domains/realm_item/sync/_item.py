"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_Domains_Realm_SyncPOSTRequest
from prmxctrl.models.access import Access_Domains_Realm_SyncPOSTResponse  # type: ignore

class AccessDomainsSyncEndpoints(EndpointBase):
    """
    Endpoint class for /access/domains/{realm}/sync
    """



    async def sync(self, params: Access_Domains_Realm_SyncPOSTRequest | None = None) -> Access_Domains_Realm_SyncPOSTResponse:
        """
        Syncs users and/or groups from the configured LDAP to user.cfg. NOTE: Synced groups will have the name 'name-$realm', so make sure those groups do not exist to prevent overwriting.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

