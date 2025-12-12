"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_HostsGETRequest
from prmxctrl.models.nodes import Nodes_Node_HostsGETResponse
from prmxctrl.models.nodes import Nodes_Node_HostsPOSTRequest  # type: ignore

class NodesHostsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/hosts
    """



    async def get(self, params: Nodes_Node_HostsGETRequest | None = None) -> Nodes_Node_HostsGETResponse:
        """
        Get the content of /etc/hosts.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def write_etc_hosts(self, params: Nodes_Node_HostsPOSTRequest | None = None) -> Any:
        """
        Write /etc/hosts.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

