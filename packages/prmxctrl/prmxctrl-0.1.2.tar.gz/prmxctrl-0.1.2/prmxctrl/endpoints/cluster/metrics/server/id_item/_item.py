"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Metrics_Server_IdDELETERequest
from prmxctrl.models.cluster import Cluster_Metrics_Server_IdGETRequest
from prmxctrl.models.cluster import Cluster_Metrics_Server_IdGETResponse
from prmxctrl.models.cluster import Cluster_Metrics_Server_IdPOSTRequest
from prmxctrl.models.cluster import Cluster_Metrics_Server_IdPUTRequest  # type: ignore

class ClusterMetricsServerEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/metrics/server/{id}
    """



    async def delete(self, params: Cluster_Metrics_Server_IdDELETERequest | None = None) -> Any:
        """
        Remove Metric server.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Metrics_Server_IdGETRequest | None = None) -> Cluster_Metrics_Server_IdGETResponse:
        """
        Read metric server configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Cluster_Metrics_Server_IdPOSTRequest | None = None) -> Any:
        """
        Create a new external metric server config

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Metrics_Server_IdPUTRequest | None = None) -> Any:
        """
        Update metric server configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

