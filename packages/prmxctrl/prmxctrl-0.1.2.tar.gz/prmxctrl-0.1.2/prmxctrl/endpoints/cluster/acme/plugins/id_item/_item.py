"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Acme_Plugins_IdDELETERequest
from prmxctrl.models.cluster import Cluster_Acme_Plugins_IdGETRequest
from prmxctrl.models.cluster import Cluster_Acme_Plugins_IdGETResponse
from prmxctrl.models.cluster import Cluster_Acme_Plugins_IdPUTRequest  # type: ignore

class ClusterAcmePluginsEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/acme/plugins/{id}
    """



    async def delete(self, params: Cluster_Acme_Plugins_IdDELETERequest | None = None) -> Any:
        """
        Delete ACME plugin configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Acme_Plugins_IdGETRequest | None = None) -> Cluster_Acme_Plugins_IdGETResponse:
        """
        Get ACME plugin configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_plugin(self, params: Cluster_Acme_Plugins_IdPUTRequest | None = None) -> Any:
        """
        Update ACME plugin configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

