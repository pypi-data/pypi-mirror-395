"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .group_item._item import ClusterFirewallGroupsEndpoints1
from prmxctrl.models.cluster import Cluster_Firewall_GroupsGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_GroupsPOSTRequest  # type: ignore

class ClusterFirewallGroupsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall/groups
    """


    def __call__(self, group: str) -> ClusterFirewallGroupsEndpoints1:
        """Access specific group"""
        from .group_item._item import ClusterFirewallGroupsEndpoints1  # type: ignore
        return ClusterFirewallGroupsEndpoints1(
            self._client,
            self._build_path(str(group))
        )


    async def list(self, ) -> Cluster_Firewall_GroupsGETResponse:
        """
        List security groups.

        HTTP Method: GET
        """
        return await self._get()

    async def create_security_group(self, params: Cluster_Firewall_GroupsPOSTRequest | None = None) -> Any:
        """
        Create new security group.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

