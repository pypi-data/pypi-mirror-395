"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.cluster import Cluster_Jobs_Schedule_AnalyzeGETRequest
from prmxctrl.models.cluster import Cluster_Jobs_Schedule_AnalyzeGETResponse  # type: ignore

class ClusterJobsSchedule_AnalyzeEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/jobs/schedule-analyze
    """



    async def list(self, params: Cluster_Jobs_Schedule_AnalyzeGETRequest | None = None) -> Cluster_Jobs_Schedule_AnalyzeGETResponse:
        """
        Returns a list of future schedule runtimes.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

