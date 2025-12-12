"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .rules._item import NodesQemuFirewallRulesEndpoints
from .aliases._item import NodesQemuFirewallAliasesEndpoints
from .ipset._item import NodesQemuFirewallIpsetEndpoints
from .options._item import NodesQemuFirewallOptionsEndpoints
from .log._item import NodesQemuFirewallLogEndpoints
from .refs._item import NodesQemuFirewallRefsEndpoints
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_FirewallGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_FirewallGETResponse  # type: ignore

class NodesQemuFirewallEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/firewall
    """

    # Sub-endpoint properties
    @property
    def rules(self) -> NodesQemuFirewallRulesEndpoints:
        """Access rules endpoints"""
        from .rules._item import NodesQemuFirewallRulesEndpoints  # type: ignore
        return NodesQemuFirewallRulesEndpoints(self._client, self._build_path("rules"))
    @property
    def aliases(self) -> NodesQemuFirewallAliasesEndpoints:
        """Access aliases endpoints"""
        from .aliases._item import NodesQemuFirewallAliasesEndpoints  # type: ignore
        return NodesQemuFirewallAliasesEndpoints(self._client, self._build_path("aliases"))
    @property
    def ipset(self) -> NodesQemuFirewallIpsetEndpoints:
        """Access ipset endpoints"""
        from .ipset._item import NodesQemuFirewallIpsetEndpoints  # type: ignore
        return NodesQemuFirewallIpsetEndpoints(self._client, self._build_path("ipset"))
    @property
    def options(self) -> NodesQemuFirewallOptionsEndpoints:
        """Access options endpoints"""
        from .options._item import NodesQemuFirewallOptionsEndpoints  # type: ignore
        return NodesQemuFirewallOptionsEndpoints(self._client, self._build_path("options"))
    @property
    def log(self) -> NodesQemuFirewallLogEndpoints:
        """Access log endpoints"""
        from .log._item import NodesQemuFirewallLogEndpoints  # type: ignore
        return NodesQemuFirewallLogEndpoints(self._client, self._build_path("log"))
    @property
    def refs(self) -> NodesQemuFirewallRefsEndpoints:
        """Access refs endpoints"""
        from .refs._item import NodesQemuFirewallRefsEndpoints  # type: ignore
        return NodesQemuFirewallRefsEndpoints(self._client, self._build_path("refs"))



    async def list(self, params: Nodes_Node_Qemu_Vmid_FirewallGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_FirewallGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

