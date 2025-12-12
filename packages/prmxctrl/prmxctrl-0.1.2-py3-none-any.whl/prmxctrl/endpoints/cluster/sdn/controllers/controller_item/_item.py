"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Sdn_Controllers_ControllerDELETERequest
from prmxctrl.models.cluster import Cluster_Sdn_Controllers_ControllerGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_Controllers_ControllerGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_Controllers_ControllerPUTRequest  # type: ignore

class ClusterSdnControllersEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/sdn/controllers/{controller}
    """



    async def delete(self, params: Cluster_Sdn_Controllers_ControllerDELETERequest | None = None) -> Any:
        """
        Delete sdn controller object configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Sdn_Controllers_ControllerGETRequest | None = None) -> Cluster_Sdn_Controllers_ControllerGETResponse:
        """
        Read sdn controller configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Sdn_Controllers_ControllerPUTRequest | None = None) -> Any:
        """
        Update sdn controller object configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

