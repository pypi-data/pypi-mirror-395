"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Firewall_OptionsGETResponse
from prmxctrl.models.cluster import Cluster_Firewall_OptionsPUTRequest  # type: ignore

class ClusterFirewallOptionsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/firewall/options
    """



    async def get(self, ) -> Cluster_Firewall_OptionsGETResponse:
        """
        Get Firewall options.

        HTTP Method: GET
        """
        return await self._get()

    async def set_options(self, params: Cluster_Firewall_OptionsPUTRequest | None = None) -> Any:
        """
        Set Firewall options.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

