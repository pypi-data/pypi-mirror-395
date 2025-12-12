"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_FeatureGETRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_FeatureGETResponse  # type: ignore

class NodesLxcFeatureEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/feature
    """



    async def get(self, params: Nodes_Node_Lxc_Vmid_FeatureGETRequest | None = None) -> Nodes_Node_Lxc_Vmid_FeatureGETResponse:
        """
        Check if feature for virtual machine is available.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

