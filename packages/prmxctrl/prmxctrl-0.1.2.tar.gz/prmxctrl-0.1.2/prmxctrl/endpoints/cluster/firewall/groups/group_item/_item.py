"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Firewall_Groups_GroupDELETERequest
from prmxctrl.models.cluster import Cluster_Firewall_Groups_GroupGETRequest
from prmxctrl.models.cluster import Cluster_Firewall_Groups_GroupGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_Groups_GroupPOSTRequest  # type: ignore

class ClusterFirewallGroupsEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/firewall/groups/{group}
    """



    async def delete(self, params: Cluster_Firewall_Groups_GroupDELETERequest | None = None) -> Any:
        """
        Delete security group.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Cluster_Firewall_Groups_GroupGETRequest | None = None) -> Cluster_Firewall_Groups_GroupGETResponse:
        """
        List rules.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_rule(self, params: Cluster_Firewall_Groups_GroupPOSTRequest | None = None) -> Any:
        """
        Create new rule.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

