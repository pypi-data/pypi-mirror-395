"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import ClusterFirewallAliasesEndpoints1
from prmxctrl.models.cluster import Cluster_Firewall_AliasesGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_AliasesPOSTRequest  # type: ignore

class ClusterFirewallAliasesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall/aliases
    """


    def __call__(self, name: str) -> ClusterFirewallAliasesEndpoints1:
        """Access specific name"""
        from .name_item._item import ClusterFirewallAliasesEndpoints1  # type: ignore
        return ClusterFirewallAliasesEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, ) -> Cluster_Firewall_AliasesGETResponse:
        """
        List aliases

        HTTP Method: GET
        """
        return await self._get()

    async def create_alias(self, params: Cluster_Firewall_AliasesPOSTRequest | None = None) -> Any:
        """
        Create IP or Network Alias.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

