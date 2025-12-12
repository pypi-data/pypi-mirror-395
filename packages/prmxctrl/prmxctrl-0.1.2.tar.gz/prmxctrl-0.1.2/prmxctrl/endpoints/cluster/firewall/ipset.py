"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import ClusterFirewallIpsetEndpoints1
from prmxctrl.models.cluster import Cluster_Firewall_IpsetGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_IpsetPOSTRequest  # type: ignore

class ClusterFirewallIpsetEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall/ipset
    """


    def __call__(self, name: str) -> ClusterFirewallIpsetEndpoints1:
        """Access specific name"""
        from .name_item._item import ClusterFirewallIpsetEndpoints1  # type: ignore
        return ClusterFirewallIpsetEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, ) -> Cluster_Firewall_IpsetGETResponse:
        """
        List IPSets

        HTTP Method: GET
        """
        return await self._get()

    async def create_ipset(self, params: Cluster_Firewall_IpsetPOSTRequest | None = None) -> Any:
        """
        Create new IPSet

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

