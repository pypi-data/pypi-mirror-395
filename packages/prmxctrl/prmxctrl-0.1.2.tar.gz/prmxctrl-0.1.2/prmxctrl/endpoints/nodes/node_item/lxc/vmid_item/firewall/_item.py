"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .rules._item import NodesLxcFirewallRulesEndpoints
from .aliases._item import NodesLxcFirewallAliasesEndpoints
from .ipset._item import NodesLxcFirewallIpsetEndpoints
from .options._item import NodesLxcFirewallOptionsEndpoints
from .log._item import NodesLxcFirewallLogEndpoints
from .refs._item import NodesLxcFirewallRefsEndpoints
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_FirewallGETRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_FirewallGETResponse  # type: ignore

class NodesLxcFirewallEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/firewall
    """

    # Sub-endpoint properties
    @property
    def rules(self) -> NodesLxcFirewallRulesEndpoints:
        """Access rules endpoints"""
        from .rules._item import NodesLxcFirewallRulesEndpoints  # type: ignore
        return NodesLxcFirewallRulesEndpoints(self._client, self._build_path("rules"))
    @property
    def aliases(self) -> NodesLxcFirewallAliasesEndpoints:
        """Access aliases endpoints"""
        from .aliases._item import NodesLxcFirewallAliasesEndpoints  # type: ignore
        return NodesLxcFirewallAliasesEndpoints(self._client, self._build_path("aliases"))
    @property
    def ipset(self) -> NodesLxcFirewallIpsetEndpoints:
        """Access ipset endpoints"""
        from .ipset._item import NodesLxcFirewallIpsetEndpoints  # type: ignore
        return NodesLxcFirewallIpsetEndpoints(self._client, self._build_path("ipset"))
    @property
    def options(self) -> NodesLxcFirewallOptionsEndpoints:
        """Access options endpoints"""
        from .options._item import NodesLxcFirewallOptionsEndpoints  # type: ignore
        return NodesLxcFirewallOptionsEndpoints(self._client, self._build_path("options"))
    @property
    def log(self) -> NodesLxcFirewallLogEndpoints:
        """Access log endpoints"""
        from .log._item import NodesLxcFirewallLogEndpoints  # type: ignore
        return NodesLxcFirewallLogEndpoints(self._client, self._build_path("log"))
    @property
    def refs(self) -> NodesLxcFirewallRefsEndpoints:
        """Access refs endpoints"""
        from .refs._item import NodesLxcFirewallRefsEndpoints  # type: ignore
        return NodesLxcFirewallRefsEndpoints(self._client, self._build_path("refs"))



    async def list(self, params: Nodes_Node_Lxc_Vmid_FirewallGETRequest | None = None) -> Nodes_Node_Lxc_Vmid_FirewallGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

