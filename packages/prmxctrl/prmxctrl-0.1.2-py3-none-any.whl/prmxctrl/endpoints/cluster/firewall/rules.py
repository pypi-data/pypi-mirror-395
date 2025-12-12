"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .pos_item._item import ClusterFirewallRulesEndpoints1
from prmxctrl.models.cluster import Cluster_Firewall_RulesGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_RulesPOSTRequest  # type: ignore

class ClusterFirewallRulesEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall/rules
    """


    def __call__(self, pos: str) -> ClusterFirewallRulesEndpoints1:
        """Access specific pos"""
        from .pos_item._item import ClusterFirewallRulesEndpoints1  # type: ignore
        return ClusterFirewallRulesEndpoints1(
            self._client,
            self._build_path(str(pos))
        )


    async def list(self, ) -> Cluster_Firewall_RulesGETResponse:
        """
        List rules.

        HTTP Method: GET
        """
        return await self._get()

    async def create_rule(self, params: Cluster_Firewall_RulesPOSTRequest | None = None) -> Any:
        """
        Create new rule.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

