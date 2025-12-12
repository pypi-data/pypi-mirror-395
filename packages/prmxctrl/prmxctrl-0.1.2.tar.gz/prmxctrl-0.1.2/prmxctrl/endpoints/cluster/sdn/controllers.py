"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .controller_item._item import ClusterSdnControllersEndpoints1
from prmxctrl.models.cluster import Cluster_Sdn_ControllersGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_ControllersGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_ControllersPOSTRequest  # type: ignore

class ClusterSdnControllersEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/sdn/controllers
    """


    def __call__(self, controller: str) -> ClusterSdnControllersEndpoints1:
        """Access specific controller"""
        from .controller_item._item import ClusterSdnControllersEndpoints1  # type: ignore
        return ClusterSdnControllersEndpoints1(
            self._client,
            self._build_path(str(controller))
        )


    async def list(self, params: Cluster_Sdn_ControllersGETRequest | None = None) -> Cluster_Sdn_ControllersGETResponse:
        """
        SDN controllers index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Sdn_ControllersPOSTRequest | None = None) -> Any:
        """
        Create a new sdn controller object.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

