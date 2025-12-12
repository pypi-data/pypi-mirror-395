"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .id_item._item import ClusterAcmePluginsEndpoints1
from prmxctrl.models.cluster import Cluster_Acme_PluginsGETRequest
from prmxctrl.models.cluster import Cluster_Acme_PluginsGETResponse
from prmxctrl.models.cluster import Cluster_Acme_PluginsPOSTRequest  # type: ignore

class ClusterAcmePluginsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/acme/plugins
    """


    def __call__(self, id: int) -> ClusterAcmePluginsEndpoints1:
        """Access specific id"""
        from .id_item._item import ClusterAcmePluginsEndpoints1  # type: ignore
        return ClusterAcmePluginsEndpoints1(
            self._client,
            self._build_path(str(id))
        )


    async def list(self, params: Cluster_Acme_PluginsGETRequest | None = None) -> Cluster_Acme_PluginsGETResponse:
        """
        ACME plugin index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def add_plugin(self, params: Cluster_Acme_PluginsPOSTRequest | None = None) -> Any:
        """
        Add ACME plugin configuration.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

