"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Network_IfaceDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Network_IfaceGETRequest
from prmxctrl.models.nodes import Nodes_Node_Network_IfaceGETResponse
from prmxctrl.models.nodes import Nodes_Node_Network_IfacePUTRequest  # type: ignore

class NodesNetworkEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/network/{iface}
    """



    async def delete(self, params: Nodes_Node_Network_IfaceDELETERequest | None = None) -> Any:
        """
        Delete network device configuration

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Nodes_Node_Network_IfaceGETRequest | None = None) -> Nodes_Node_Network_IfaceGETResponse:
        """
        Read network device configuration

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_network(self, params: Nodes_Node_Network_IfacePUTRequest | None = None) -> Any:
        """
        Update network device configuration

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

