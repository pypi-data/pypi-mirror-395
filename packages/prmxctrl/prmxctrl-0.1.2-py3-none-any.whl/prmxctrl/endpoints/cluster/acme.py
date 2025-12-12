"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..acme.plugins import ClusterAcmePluginsEndpoints
from ..acme.account import ClusterAcmeAccountEndpoints
from ..acme.tos import ClusterAcmeTosEndpoints
from ..acme.directories import ClusterAcmeDirectoriesEndpoints
from ..acme.challenge_schema import ClusterAcmeChallenge_SchemaEndpoints
from prmxctrl.models.cluster import Cluster_AcmeGETResponse  # type: ignore

class ClusterAcmeEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/acme
    """

    # Sub-endpoint properties
    @property
    def plugins(self) -> ClusterAcmePluginsEndpoints:
        """Access plugins endpoints"""
        from ..acme.plugins import ClusterAcmePluginsEndpoints  # type: ignore
        return ClusterAcmePluginsEndpoints(self._client, self._build_path("plugins"))
    @property
    def account(self) -> ClusterAcmeAccountEndpoints:
        """Access account endpoints"""
        from ..acme.account import ClusterAcmeAccountEndpoints  # type: ignore
        return ClusterAcmeAccountEndpoints(self._client, self._build_path("account"))
    @property
    def tos(self) -> ClusterAcmeTosEndpoints:
        """Access tos endpoints"""
        from ..acme.tos import ClusterAcmeTosEndpoints  # type: ignore
        return ClusterAcmeTosEndpoints(self._client, self._build_path("tos"))
    @property
    def directories(self) -> ClusterAcmeDirectoriesEndpoints:
        """Access directories endpoints"""
        from ..acme.directories import ClusterAcmeDirectoriesEndpoints  # type: ignore
        return ClusterAcmeDirectoriesEndpoints(self._client, self._build_path("directories"))
    @property
    def challenge_schema(self) -> ClusterAcmeChallenge_SchemaEndpoints:
        """Access challenge-schema endpoints"""
        from ..acme.challenge_schema import ClusterAcmeChallenge_SchemaEndpoints  # type: ignore
        return ClusterAcmeChallenge_SchemaEndpoints(self._client, self._build_path("challenge-schema"))



    async def list(self, ) -> Cluster_AcmeGETResponse:
        """
        ACMEAccount index.

        HTTP Method: GET
        """
        return await self._get()

