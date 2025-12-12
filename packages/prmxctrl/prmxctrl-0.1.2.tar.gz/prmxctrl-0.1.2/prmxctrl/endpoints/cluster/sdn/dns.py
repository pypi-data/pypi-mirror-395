"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .dns_item._item import ClusterSdnDnsEndpoints1
from prmxctrl.models.cluster import Cluster_Sdn_DnsGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_DnsGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_DnsPOSTRequest  # type: ignore

class ClusterSdnDnsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/sdn/dns
    """


    def __call__(self, dns: str) -> ClusterSdnDnsEndpoints1:
        """Access specific dns"""
        from .dns_item._item import ClusterSdnDnsEndpoints1  # type: ignore
        return ClusterSdnDnsEndpoints1(
            self._client,
            self._build_path(str(dns))
        )


    async def list(self, params: Cluster_Sdn_DnsGETRequest | None = None) -> Cluster_Sdn_DnsGETResponse:
        """
        SDN dns index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Sdn_DnsPOSTRequest | None = None) -> Any:
        """
        Create a new sdn dns object.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

