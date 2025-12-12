"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .rules._item import NodesFirewallRulesEndpoints
from .options._item import NodesFirewallOptionsEndpoints
from .log._item import NodesFirewallLogEndpoints
from prmxctrl.models.nodes import Nodes_Node_FirewallGETRequest
from prmxctrl.models.nodes import Nodes_Node_FirewallGETResponse  # type: ignore

class NodesFirewallEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/firewall
    """

    # Sub-endpoint properties
    @property
    def rules(self) -> NodesFirewallRulesEndpoints:
        """Access rules endpoints"""
        from .rules._item import NodesFirewallRulesEndpoints  # type: ignore
        return NodesFirewallRulesEndpoints(self._client, self._build_path("rules"))
    @property
    def options(self) -> NodesFirewallOptionsEndpoints:
        """Access options endpoints"""
        from .options._item import NodesFirewallOptionsEndpoints  # type: ignore
        return NodesFirewallOptionsEndpoints(self._client, self._build_path("options"))
    @property
    def log(self) -> NodesFirewallLogEndpoints:
        """Access log endpoints"""
        from .log._item import NodesFirewallLogEndpoints  # type: ignore
        return NodesFirewallLogEndpoints(self._client, self._build_path("log"))



    async def list(self, params: Nodes_Node_FirewallGETRequest | None = None) -> Nodes_Node_FirewallGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

