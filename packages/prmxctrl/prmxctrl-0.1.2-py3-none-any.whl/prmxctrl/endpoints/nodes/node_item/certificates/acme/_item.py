"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .certificate._item import NodesCertificatesAcmeCertificateEndpoints
from prmxctrl.models.nodes import Nodes_Node_Certificates_AcmeGETRequest
from prmxctrl.models.nodes import Nodes_Node_Certificates_AcmeGETResponse  # type: ignore

class NodesCertificatesAcmeEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/certificates/acme
    """

    # Sub-endpoint properties
    @property
    def certificate(self) -> NodesCertificatesAcmeCertificateEndpoints:
        """Access certificate endpoints"""
        from .certificate._item import NodesCertificatesAcmeCertificateEndpoints  # type: ignore
        return NodesCertificatesAcmeCertificateEndpoints(self._client, self._build_path("certificate"))



    async def list(self, params: Nodes_Node_Certificates_AcmeGETRequest | None = None) -> Nodes_Node_Certificates_AcmeGETResponse:
        """
        ACME index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

