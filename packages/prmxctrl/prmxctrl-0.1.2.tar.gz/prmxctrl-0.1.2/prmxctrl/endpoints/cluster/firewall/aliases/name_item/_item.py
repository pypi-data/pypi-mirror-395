"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Firewall_Aliases_NameDELETERequest
from prmxctrl.models.cluster import Cluster_Firewall_Aliases_NameGETRequest
from prmxctrl.models.cluster import Cluster_Firewall_Aliases_NameGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_Aliases_NamePUTRequest  # type: ignore

class ClusterFirewallAliasesEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/firewall/aliases/{name}
    """



    async def delete(self, params: Cluster_Firewall_Aliases_NameDELETERequest | None = None) -> Any:
        """
        Remove IP or Network alias.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Firewall_Aliases_NameGETRequest | None = None) -> Cluster_Firewall_Aliases_NameGETResponse:
        """
        Read alias.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_alias(self, params: Cluster_Firewall_Aliases_NamePUTRequest | None = None) -> Any:
        """
        Update IP or Network alias.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

