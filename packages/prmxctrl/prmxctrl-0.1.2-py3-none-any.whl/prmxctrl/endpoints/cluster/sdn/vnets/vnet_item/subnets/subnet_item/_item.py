"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_Vnet_Subnets_SubnetDELETERequest
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_Vnet_Subnets_SubnetGETRequest
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_Vnet_Subnets_SubnetGETResponse
from prmxctrl.models.cluster import Cluster_Sdn_Vnets_Vnet_Subnets_SubnetPUTRequest  # type: ignore

class ClusterSdnVnetsSubnetsEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/sdn/vnets/{vnet}/subnets/{subnet}
    """



    async def delete(self, params: Cluster_Sdn_Vnets_Vnet_Subnets_SubnetDELETERequest | None = None) -> Any:
        """
        Delete sdn subnet object configuration.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Sdn_Vnets_Vnet_Subnets_SubnetGETRequest | None = None) -> Cluster_Sdn_Vnets_Vnet_Subnets_SubnetGETResponse:
        """
        Read sdn subnet configuration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update(self, params: Cluster_Sdn_Vnets_Vnet_Subnets_SubnetPUTRequest | None = None) -> Any:
        """
        Update sdn subnet object configuration.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

