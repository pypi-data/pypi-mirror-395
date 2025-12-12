"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .zone_item._item import NodesSdnZonesEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Sdn_ZonesGETRequest
from prmxctrl.models.nodes import Nodes_Node_Sdn_ZonesGETResponse  # type: ignore

class NodesSdnZonesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/sdn/zones
    """


    def __call__(self, zone: str) -> NodesSdnZonesEndpoints1:
        """Access specific zone"""
        from .zone_item._item import NodesSdnZonesEndpoints1  # type: ignore
        return NodesSdnZonesEndpoints1(
            self._client,
            self._build_path(str(zone))
        )


    async def list(self, params: Nodes_Node_Sdn_ZonesGETRequest | None = None) -> Nodes_Node_Sdn_ZonesGETResponse:
        """
        Get status for all zones.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

