"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import ClusterAcmeAccountEndpoints1
from prmxctrl.models.cluster import Cluster_Acme_AccountGETResponse
from prmxctrl.models.cluster import Cluster_Acme_AccountPOSTRequest
from prmxctrl.models.cluster import Cluster_Acme_AccountPOSTResponse  # type: ignore

class ClusterAcmeAccountEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/acme/account
    """


    def __call__(self, name: str) -> ClusterAcmeAccountEndpoints1:
        """Access specific name"""
        from .name_item._item import ClusterAcmeAccountEndpoints1  # type: ignore
        return ClusterAcmeAccountEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, ) -> Cluster_Acme_AccountGETResponse:
        """
        ACMEAccount index.

        HTTP Method: GET
        """
        return await self._get()

    async def register_account(self, params: Cluster_Acme_AccountPOSTRequest | None = None) -> Cluster_Acme_AccountPOSTResponse:
        """
        Register a new ACME account with CA.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

