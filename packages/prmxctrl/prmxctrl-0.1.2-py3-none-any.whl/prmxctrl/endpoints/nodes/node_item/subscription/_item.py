"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_SubscriptionDELETERequest
from prmxctrl.models.nodes import Nodes_Node_SubscriptionGETRequest
from prmxctrl.models.nodes import Nodes_Node_SubscriptionGETResponse
from prmxctrl.models.nodes import Nodes_Node_SubscriptionPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_SubscriptionPUTRequest  # type: ignore

class NodesSubscriptionEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/subscription
    """



    async def delete(self, params: Nodes_Node_SubscriptionDELETERequest | None = None) -> Any:
        """
        Delete subscription key of this node.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Nodes_Node_SubscriptionGETRequest | None = None) -> Nodes_Node_SubscriptionGETResponse:
        """
        Read subscription info.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Nodes_Node_SubscriptionPOSTRequest | None = None) -> Any:
        """
        Update subscription info.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def set(self, params: Nodes_Node_SubscriptionPUTRequest | None = None) -> Any:
        """
        Set subscription key.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

