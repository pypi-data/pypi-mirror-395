"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .service_item._item import NodesServicesEndpoints1
from prmxctrl.models.nodes import Nodes_Node_ServicesGETRequest
from prmxctrl.models.nodes import Nodes_Node_ServicesGETResponse  # type: ignore

class NodesServicesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/services
    """


    def __call__(self, service: str) -> NodesServicesEndpoints1:
        """Access specific service"""
        from .service_item._item import NodesServicesEndpoints1  # type: ignore
        return NodesServicesEndpoints1(
            self._client,
            self._build_path(str(service))
        )


    async def list(self, params: Nodes_Node_ServicesGETRequest | None = None) -> Nodes_Node_ServicesGETResponse:
        """
        Service list.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

