"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_OptionsGETResponse
from prmxctrl.models.cluster import Cluster_OptionsPUTRequest  # type: ignore

class ClusterOptionsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/options
    """



    async def get(self, ) -> Cluster_OptionsGETResponse:
        """
        Get datacenter options. Without 'Sys.Audit' on '/' not all options are returned.

        HTTP Method: GET
        """
        return await self._get()

    async def set_options(self, params: Cluster_OptionsPUTRequest | None = None) -> Any:
        """
        Set datacenter options.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

