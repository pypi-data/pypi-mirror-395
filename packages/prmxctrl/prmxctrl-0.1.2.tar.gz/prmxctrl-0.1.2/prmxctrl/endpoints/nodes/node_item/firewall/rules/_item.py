"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .pos_item._item import NodesFirewallRulesEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Firewall_RulesGETRequest
from prmxctrl.models.nodes import Nodes_Node_Firewall_RulesGETResponse
from prmxctrl.models.nodes import Nodes_Node_Firewall_RulesPOSTRequest  # type: ignore

class NodesFirewallRulesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/firewall/rules
    """


    def __call__(self, pos: str) -> NodesFirewallRulesEndpoints1:
        """Access specific pos"""
        from .pos_item._item import NodesFirewallRulesEndpoints1  # type: ignore
        return NodesFirewallRulesEndpoints1(
            self._client,
            self._build_path(str(pos))
        )


    async def list(self, params: Nodes_Node_Firewall_RulesGETRequest | None = None) -> Nodes_Node_Firewall_RulesGETResponse:
        """
        List rules.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_rule(self, params: Nodes_Node_Firewall_RulesPOSTRequest | None = None) -> Any:
        """
        Create new rule.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

