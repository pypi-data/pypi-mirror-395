"""
Generated Proxmox VE API Client.

This module contains the main ProxmoxClient class for accessing
the Proxmox VE API through type-safe, hierarchical endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Optional
from prmxctrl.base.http_client import HTTPClient

from prmxctrl.endpoints.cluster import ClusterEndpoints
from prmxctrl.endpoints.nodes import NodesEndpoints
from prmxctrl.endpoints.storage import StorageEndpoints
from prmxctrl.endpoints.access import AccessEndpoints
from prmxctrl.endpoints.pools import PoolsEndpoints
from prmxctrl.endpoints.version import VersionEndpoints


class ProxmoxClient(HTTPClient):
    """
    Main client for accessing the Proxmox VE API.

    This class provides hierarchical access to all Proxmox API endpoints
    with full type safety and async support.

    Example:
        async with ProxmoxClient(
            host="https://proxmox.example.com:8006",
            user="root@pam",
            password="secret"
        ) as client:
            # Access cluster endpoints
            status = await client.cluster.status.get()

            # Access node-specific endpoints
            nodes = await client.nodes.list()
            node_info = await client.nodes("pve1").status.get()

            # Access VM endpoints
            vm_config = await client.nodes("pve1").qemu(100).config.get()
    """

    def __init__(
        self,
        host: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        token_name: Optional[str] = None,
        token_value: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: float = 30.0,
    ):
        """
        Initialize the Proxmox API client.

        Args:
            host: Proxmox host URL (e.g., "https://proxmox:8006")
            user: Username for authentication (required for password auth)
            password: Password for authentication (required for password auth)
            token_name: API token name (required for token auth)
            token_value: API token value (required for token auth)
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
        """
        super().__init__(
            host=host,
            user=user,
            password=password,
            token_name=token_name,
            token_value=token_value,
            verify_ssl=verify_ssl,
            timeout=timeout,
        )

    @property
    def cluster(self) -> ClusterEndpoints:
        """Access cluster API endpoints."""
        return ClusterEndpoints(self, "/cluster")

    @property
    def nodes(self) -> NodesEndpoints:
        """Access nodes API endpoints."""
        return NodesEndpoints(self, "/nodes")

    @property
    def storage(self) -> StorageEndpoints:
        """Access storage API endpoints."""
        return StorageEndpoints(self, "/storage")

    @property
    def access(self) -> AccessEndpoints:
        """Access access API endpoints."""
        return AccessEndpoints(self, "/access")

    @property
    def pools(self) -> PoolsEndpoints:
        """Access pools API endpoints."""
        return PoolsEndpoints(self, "/pools")

    @property
    def version(self) -> VersionEndpoints:
        """Access version API endpoints."""
        return VersionEndpoints(self, "/version")

