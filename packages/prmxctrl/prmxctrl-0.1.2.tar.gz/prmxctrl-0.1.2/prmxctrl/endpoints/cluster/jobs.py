"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from ..jobs.schedule_analyze import ClusterJobsSchedule_AnalyzeEndpoints
from prmxctrl.models.cluster import Cluster_JobsGETResponse  # type: ignore

class ClusterJobsEndpoints(EndpointBase):
    """
    Endpoint class for /cluster/jobs
    """

    # Sub-endpoint properties
    @property
    def schedule_analyze(self) -> ClusterJobsSchedule_AnalyzeEndpoints:
        """Access schedule-analyze endpoints"""
        from ..jobs.schedule_analyze import ClusterJobsSchedule_AnalyzeEndpoints  # type: ignore
        return ClusterJobsSchedule_AnalyzeEndpoints(self._client, self._build_path("schedule-analyze"))



    async def list(self, ) -> Cluster_JobsGETResponse:
        """
        Index for jobs related endpoints.

        HTTP Method: GET
        """
        return await self._get()

