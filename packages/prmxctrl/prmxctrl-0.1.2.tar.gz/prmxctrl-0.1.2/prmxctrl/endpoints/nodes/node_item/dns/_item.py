"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_DnsGETRequest
from prmxctrl.models.nodes import Nodes_Node_DnsGETResponse
from prmxctrl.models.nodes import Nodes_Node_DnsPUTRequest  # type: ignore

class NodesDnsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/dns
    """



    async def get(self, params: Nodes_Node_DnsGETRequest | None = None) -> Nodes_Node_DnsGETResponse:
        """
        Read DNS settings.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_dns(self, params: Nodes_Node_DnsPUTRequest | None = None) -> Any:
        """
        Write DNS settings.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

