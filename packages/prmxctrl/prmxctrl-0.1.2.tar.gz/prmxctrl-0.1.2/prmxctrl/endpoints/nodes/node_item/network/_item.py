"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .iface_item._item import NodesNetworkEndpoints1
from prmxctrl.models.nodes import Nodes_Node_NetworkDELETERequest
from prmxctrl.models.nodes import Nodes_Node_NetworkGETRequest
from prmxctrl.models.nodes import Nodes_Node_NetworkGETResponse
from prmxctrl.models.nodes import Nodes_Node_NetworkPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_NetworkPUTRequest
from prmxctrl.models.nodes import Nodes_Node_NetworkPUTResponse  # type: ignore

class NodesNetworkEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/network
    """


    def __call__(self, iface: str) -> NodesNetworkEndpoints1:
        """Access specific iface"""
        from .iface_item._item import NodesNetworkEndpoints1  # type: ignore
        return NodesNetworkEndpoints1(
            self._client,
            self._build_path(str(iface))
        )


    async def delete(self, params: Nodes_Node_NetworkDELETERequest | None = None) -> Any:
        """
        Revert network configuration changes.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_NetworkGETRequest | None = None) -> Nodes_Node_NetworkGETResponse:
        """
        List available networks

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_network(self, params: Nodes_Node_NetworkPOSTRequest | None = None) -> Any:
        """
        Create network device configuration

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def reload_network_config(self, params: Nodes_Node_NetworkPUTRequest | None = None) -> Nodes_Node_NetworkPUTResponse:
        """
        Reload network configuration

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

