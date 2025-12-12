"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .acme._item import NodesCertificatesAcmeEndpoints
from .info._item import NodesCertificatesInfoEndpoints
from .custom._item import NodesCertificatesCustomEndpoints
from prmxctrl.models.nodes import Nodes_Node_CertificatesGETRequest
from prmxctrl.models.nodes import Nodes_Node_CertificatesGETResponse  # type: ignore

class NodesCertificatesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/certificates
    """

    # Sub-endpoint properties
    @property
    def acme(self) -> NodesCertificatesAcmeEndpoints:
        """Access acme endpoints"""
        from .acme._item import NodesCertificatesAcmeEndpoints  # type: ignore
        return NodesCertificatesAcmeEndpoints(self._client, self._build_path("acme"))
    @property
    def info(self) -> NodesCertificatesInfoEndpoints:
        """Access info endpoints"""
        from .info._item import NodesCertificatesInfoEndpoints  # type: ignore
        return NodesCertificatesInfoEndpoints(self._client, self._build_path("info"))
    @property
    def custom(self) -> NodesCertificatesCustomEndpoints:
        """Access custom endpoints"""
        from .custom._item import NodesCertificatesCustomEndpoints  # type: ignore
        return NodesCertificatesCustomEndpoints(self._client, self._build_path("custom"))



    async def list(self, params: Nodes_Node_CertificatesGETRequest | None = None) -> Nodes_Node_CertificatesGETResponse:
        """
        Node index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

