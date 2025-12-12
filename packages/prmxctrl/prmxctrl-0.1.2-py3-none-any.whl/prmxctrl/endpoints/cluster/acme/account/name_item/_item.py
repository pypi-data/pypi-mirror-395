"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Acme_Account_NameDELETERequest
from prmxctrl.models.cluster import Cluster_Acme_Account_NameDELETEResponse
from prmxctrl.models.cluster import Cluster_Acme_Account_NameGETRequest
from prmxctrl.models.cluster import Cluster_Acme_Account_NameGETResponse
from prmxctrl.models.cluster import Cluster_Acme_Account_NamePUTRequest
from prmxctrl.models.cluster import Cluster_Acme_Account_NamePUTResponse  # type: ignore

class ClusterAcmeAccountEndpoints1(EndpointBase):
    """
    Endpoint class for /cluster/acme/account/{name}
    """



    async def delete(self, params: Cluster_Acme_Account_NameDELETERequest | None = None) -> Cluster_Acme_Account_NameDELETEResponse:
        """
        Deactivate existing ACME account at CA.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Cluster_Acme_Account_NameGETRequest | None = None) -> Cluster_Acme_Account_NameGETResponse:
        """
        Return existing ACME account information.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_account(self, params: Cluster_Acme_Account_NamePUTRequest | None = None) -> Cluster_Acme_Account_NamePUTResponse:
        """
        Update existing ACME account information with CA. Note: not specifying any new account information triggers a refresh.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

