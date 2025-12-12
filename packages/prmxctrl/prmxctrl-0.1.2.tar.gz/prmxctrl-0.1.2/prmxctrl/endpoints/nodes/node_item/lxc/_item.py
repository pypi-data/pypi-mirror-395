"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .vmid_item._item import NodesLxcEndpoints1
from prmxctrl.models.nodes import Nodes_Node_LxcGETRequest
from prmxctrl.models.nodes import Nodes_Node_LxcGETResponse
from prmxctrl.models.nodes import Nodes_Node_LxcPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_LxcPOSTResponse  # type: ignore

class NodesLxcEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc
    """


    def __call__(self, vmid: int) -> NodesLxcEndpoints1:
        """Access specific vmid"""
        from .vmid_item._item import NodesLxcEndpoints1  # type: ignore
        return NodesLxcEndpoints1(
            self._client,
            self._build_path(str(vmid))
        )


    async def list(self, params: Nodes_Node_LxcGETRequest | None = None) -> Nodes_Node_LxcGETResponse:
        """
        LXC container index (per node).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create_vm(self, params: Nodes_Node_LxcPOSTRequest | None = None) -> Nodes_Node_LxcPOSTResponse:
        """
        Create or restore a container.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

