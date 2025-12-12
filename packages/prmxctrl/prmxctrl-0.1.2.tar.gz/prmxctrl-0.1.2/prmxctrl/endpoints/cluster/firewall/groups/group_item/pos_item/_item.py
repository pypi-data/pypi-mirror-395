"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Firewall_Groups_Group_PosDELETERequest
from prmxctrl.models.cluster import Cluster_Firewall_Groups_Group_PosGETRequest
from prmxctrl.models.cluster import Cluster_Firewall_Groups_Group_PosGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_Groups_Group_PosPUTRequest  # type: ignore

class ClusterFirewallGroupsEndpoints2(EndpointBase):
    """
    Endpoint class for /cluster/firewall/groups/{group}/{pos}
    """



    async def delete(self, params: Cluster_Firewall_Groups_Group_PosDELETERequest | None = None) -> Any:
        """
        Delete rule.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Firewall_Groups_Group_PosGETRequest | None = None) -> Cluster_Firewall_Groups_Group_PosGETResponse:
        """
        Get single rule data.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_rule(self, params: Cluster_Firewall_Groups_Group_PosPUTRequest | None = None) -> Any:
        """
        Modify rule data.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

