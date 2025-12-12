"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Certificates_Acme_CertificateDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Certificates_Acme_CertificateDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Certificates_Acme_CertificatePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Certificates_Acme_CertificatePOSTResponse
from prmxctrl.models.nodes import Nodes_Node_Certificates_Acme_CertificatePUTRequest
from prmxctrl.models.nodes import Nodes_Node_Certificates_Acme_CertificatePUTResponse  # type: ignore

class NodesCertificatesAcmeCertificateEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/certificates/acme/certificate
    """



    async def delete(self, params: Nodes_Node_Certificates_Acme_CertificateDELETERequest | None = None) -> Nodes_Node_Certificates_Acme_CertificateDELETEResponse:
        """
        Revoke existing certificate from CA.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def new_certificate(self, params: Nodes_Node_Certificates_Acme_CertificatePOSTRequest | None = None) -> Nodes_Node_Certificates_Acme_CertificatePOSTResponse:
        """
        Order a new certificate from ACME-compatible CA.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def renew_certificate(self, params: Nodes_Node_Certificates_Acme_CertificatePUTRequest | None = None) -> Nodes_Node_Certificates_Acme_CertificatePUTResponse:
        """
        Renew existing certificate from CA.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

