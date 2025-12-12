"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..firewall.groups import ClusterFirewallGroupsEndpoints
from ..firewall.rules import ClusterFirewallRulesEndpoints
from ..firewall.ipset import ClusterFirewallIpsetEndpoints
from ..firewall.aliases import ClusterFirewallAliasesEndpoints
from ..firewall.options import ClusterFirewallOptionsEndpoints
from ..firewall.macros import ClusterFirewallMacrosEndpoints
from ..firewall.refs import ClusterFirewallRefsEndpoints
from prmxctrl.models.cluster import Cluster_FirewallGETResponse  # type: ignore

class ClusterFirewallEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall
    """

    # Sub-endpoint properties
    @property
    def groups(self) -> ClusterFirewallGroupsEndpoints:
        """Access groups endpoints"""
        from ..firewall.groups import ClusterFirewallGroupsEndpoints  # type: ignore
        return ClusterFirewallGroupsEndpoints(self._client, self._build_path("groups"))
    @property
    def rules(self) -> ClusterFirewallRulesEndpoints:
        """Access rules endpoints"""
        from ..firewall.rules import ClusterFirewallRulesEndpoints  # type: ignore
        return ClusterFirewallRulesEndpoints(self._client, self._build_path("rules"))
    @property
    def ipset(self) -> ClusterFirewallIpsetEndpoints:
        """Access ipset endpoints"""
        from ..firewall.ipset import ClusterFirewallIpsetEndpoints  # type: ignore
        return ClusterFirewallIpsetEndpoints(self._client, self._build_path("ipset"))
    @property
    def aliases(self) -> ClusterFirewallAliasesEndpoints:
        """Access aliases endpoints"""
        from ..firewall.aliases import ClusterFirewallAliasesEndpoints  # type: ignore
        return ClusterFirewallAliasesEndpoints(self._client, self._build_path("aliases"))
    @property
    def options(self) -> ClusterFirewallOptionsEndpoints:
        """Access options endpoints"""
        from ..firewall.options import ClusterFirewallOptionsEndpoints  # type: ignore
        return ClusterFirewallOptionsEndpoints(self._client, self._build_path("options"))
    @property
    def macros(self) -> ClusterFirewallMacrosEndpoints:
        """Access macros endpoints"""
        from ..firewall.macros import ClusterFirewallMacrosEndpoints  # type: ignore
        return ClusterFirewallMacrosEndpoints(self._client, self._build_path("macros"))
    @property
    def refs(self) -> ClusterFirewallRefsEndpoints:
        """Access refs endpoints"""
        from ..firewall.refs import ClusterFirewallRefsEndpoints  # type: ignore
        return ClusterFirewallRefsEndpoints(self._client, self._build_path("refs"))



    async def list(self, ) -> Cluster_FirewallGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get()

