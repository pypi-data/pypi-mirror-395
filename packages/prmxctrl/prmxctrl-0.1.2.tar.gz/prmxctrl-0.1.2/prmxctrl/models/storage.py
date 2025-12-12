"""
Pydantic models for storage API endpoints.

This module contains auto-generated Pydantic v2 models for request and response
validation in the storage API endpoints.
"""

from ..base.types import ProxmoxNode, ProxmoxVMID
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Literal

class StorageGETRequest(BaseModel):
    """
    Request model for /storage GET
    """
    type: str | None = Field(
        description="Only list storage of specific type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class StorageGETResponse(BaseModel):
    """
    Response model for /storage GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class StoragePOSTRequest(BaseModel):
    """
    Request model for /storage POST
    """
    authsupported: str | None = Field(
        description="Authsupported.",
    )
    base: str | None = Field(
        description="Base volume. This volume is automatically activated.",
    )
    blocksize: str | None = Field(
        description="block size",
    )
    bwlimit: str | None = Field(
        description="Set bandwidth/io limits various operations.",
    )
    comstar_hg: str | None = Field(
        description="host group for comstar views",
    )
    comstar_tg: str | None = Field(
        description="target group for comstar views",
    )
    content: str | None = Field(
        description="Allowed content types.\n\nNOTE: the value \u0027rootdir\u0027 is used for Containers, and value \u0027images\u0027 for VMs.\n",
    )
    content_dirs: str | None = Field(
        description="Overrides for default content type directories.",
        serialization_alias="content-dirs",
    )
    data_pool: str | None = Field(
        description="Data Pool (for erasure coding only)",
        serialization_alias="data-pool",
    )
    datastore: str | None = Field(
        description="Proxmox Backup Server datastore name.",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable the storage.",
    )
    domain: str | None = Field(
        max_length=256,
        description="CIFS domain.",
    )
    encryption_key: str | None = Field(
        description="Encryption key. Use \u0027autogen\u0027 to generate one automatically without passphrase.",
        serialization_alias="encryption-key",
    )
    export: str | None = Field(
        description="NFS export path.",
    )
    fingerprint: str | None = Field(
        description="Certificate SHA 256 fingerprint.",
    )
    format: str | None = Field(
        description="Default image format.",
    )
    fs_name: str | None = Field(
        description="The Ceph filesystem name.",
        serialization_alias="fs-name",
    )
    fuse: bool | int | str | None = Field(
        description="Mount CephFS through FUSE.",
    )
    is_mountpoint: str | None = Field(
        default="no",
        description="Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.",
    )
    iscsiprovider: str | None = Field(
        description="iscsi provider",
    )
    keyring: str | None = Field(
        description="Client keyring contents (for external clusters).",
    )
    krbd: bool | int | str | None = Field(
        description="Always access rbd through krbd kernel module.",
    )
    lio_tpg: str | None = Field(
        description="target portal group for Linux LIO targets",
    )
    master_pubkey: str | None = Field(
        description="Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.",
        serialization_alias="master-pubkey",
    )
    max_protected_backups: int | str | None = Field(
        default="Unlimited for users with Datastore.Allocate privilege, 5 for other users",
        ge=-1,
        description="Maximal number of protected backups per guest. Use \u0027-1\u0027 for unlimited.",
        serialization_alias="max-protected-backups",
    )
    maxfiles: int | str | None = Field(
        ge=0,
        description="Deprecated: use \u0027prune-backups\u0027 instead. Maximal number of backup files per VM. Use \u00270\u0027 for unlimited.",
    )
    mkdir: bool | int | str | None = Field(
        default="yes",
        description="Create the directory if it doesn\u0027t exist.",
    )
    monhost: str | None = Field(
        description="IP addresses of monitors (for external clusters).",
    )
    mountpoint: str | None = Field(
        description="mount point",
    )
    namespace: str | None = Field(
        description="Namespace.",
    )
    nocow: bool | int | str | None = Field(
        default=0,
        description="Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.",
    )
    nodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    nowritecache: bool | int | str | None = Field(
        description="disable write caching on the target",
    )
    options: str | None = Field(
        description="NFS mount options (see \u0027man nfs\u0027)",
    )
    password: str | None = Field(
        max_length=256,
        description="Password for accessing the share/datastore.",
    )
    path: str | None = Field(
        description="File system path.",
    )
    pool: str | None = Field(
        description="Pool.",
    )
    port: int | str | None = Field(
        default=8007,
        ge=1,
        le=65535,
        description="For non default port.",
    )
    portal: str | None = Field(
        description="iSCSI portal (IP or DNS name with optional port).",
    )
    preallocation: Literal["falloc", "full", "metadata", "off"] | None = Field(
        default="metadata",
        description="Preallocation mode for raw and qcow2 images. Using \u0027metadata\u0027 on raw images results in preallocation=off.",
    )
    prune_backups: str | None = Field(
        description="The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.",
        serialization_alias="prune-backups",
    )
    saferemove: bool | int | str | None = Field(
        description="Zero-out data when removing LVs.",
    )
    saferemove_throughput: str | None = Field(
        description="Wipe throughput (cstream -t parameter value).",
    )
    server: str | None = Field(
        description="Server IP or DNS name.",
    )
    server2: str | None = Field(
        description="Backup volfile server IP or DNS name.",
    )
    share: str | None = Field(
        description="CIFS share.",
    )
    shared: bool | int | str | None = Field(
        description="Mark storage as shared.",
    )
    smbversion: Literal["2.0", "2.1", "3", "3.0", "3.11", "default"] | None = Field(
        default="default",
        description="SMB protocol version. \u0027default\u0027 if not set, negotiates the highest SMB2+ version supported by both the client and server.",
    )
    sparse: bool | int | str | None = Field(
        description="use sparse volumes",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    subdir: str | None = Field(
        description="Subdir to mount.",
    )
    tagged_only: bool | int | str | None = Field(
        description="Only use logical volumes tagged with \u0027pve-vm-ID\u0027.",
    )
    target: str | None = Field(
        description="iSCSI target.",
    )
    thinpool: str | None = Field(
        description="LVM thin pool LV name.",
    )
    transport: Literal["rdma", "tcp", "unix"] | None = Field(
        description="Gluster transport: tcp or rdma",
    )
    type: str = Field(
        description="Storage type.",
    )
    username: str | None = Field(
        description="RBD Id.",
    )
    vgname: str | None = Field(
        description="Volume group name.",
    )
    volume: str | None = Field(
        description="Glusterfs Volume.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class StoragePOSTResponse(BaseModel):
    """
    Response model for /storage POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Storage_StorageDELETERequest(BaseModel):
    """
    Request model for /storage/{storage} DELETE
    """
    storage: str = Field(
        description="The storage identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Storage_StorageGETRequest(BaseModel):
    """
    Request model for /storage/{storage} GET
    """
    storage: str = Field(
        description="The storage identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Storage_StorageGETResponse(BaseModel):
    """
    Response model for /storage/{storage} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Storage_StoragePUTRequest(BaseModel):
    """
    Request model for /storage/{storage} PUT
    """
    blocksize: str | None = Field(
        description="block size",
    )
    bwlimit: str | None = Field(
        description="Set bandwidth/io limits various operations.",
    )
    comstar_hg: str | None = Field(
        description="host group for comstar views",
    )
    comstar_tg: str | None = Field(
        description="target group for comstar views",
    )
    content: str | None = Field(
        description="Allowed content types.\n\nNOTE: the value \u0027rootdir\u0027 is used for Containers, and value \u0027images\u0027 for VMs.\n",
    )
    content_dirs: str | None = Field(
        description="Overrides for default content type directories.",
        serialization_alias="content-dirs",
    )
    data_pool: str | None = Field(
        description="Data Pool (for erasure coding only)",
        serialization_alias="data-pool",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable the storage.",
    )
    domain: str | None = Field(
        max_length=256,
        description="CIFS domain.",
    )
    encryption_key: str | None = Field(
        description="Encryption key. Use \u0027autogen\u0027 to generate one automatically without passphrase.",
        serialization_alias="encryption-key",
    )
    fingerprint: str | None = Field(
        description="Certificate SHA 256 fingerprint.",
    )
    format: str | None = Field(
        description="Default image format.",
    )
    fs_name: str | None = Field(
        description="The Ceph filesystem name.",
        serialization_alias="fs-name",
    )
    fuse: bool | int | str | None = Field(
        description="Mount CephFS through FUSE.",
    )
    is_mountpoint: str | None = Field(
        default="no",
        description="Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.",
    )
    keyring: str | None = Field(
        description="Client keyring contents (for external clusters).",
    )
    krbd: bool | int | str | None = Field(
        description="Always access rbd through krbd kernel module.",
    )
    lio_tpg: str | None = Field(
        description="target portal group for Linux LIO targets",
    )
    master_pubkey: str | None = Field(
        description="Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.",
        serialization_alias="master-pubkey",
    )
    max_protected_backups: int | str | None = Field(
        default="Unlimited for users with Datastore.Allocate privilege, 5 for other users",
        ge=-1,
        description="Maximal number of protected backups per guest. Use \u0027-1\u0027 for unlimited.",
        serialization_alias="max-protected-backups",
    )
    maxfiles: int | str | None = Field(
        ge=0,
        description="Deprecated: use \u0027prune-backups\u0027 instead. Maximal number of backup files per VM. Use \u00270\u0027 for unlimited.",
    )
    mkdir: bool | int | str | None = Field(
        default="yes",
        description="Create the directory if it doesn\u0027t exist.",
    )
    monhost: str | None = Field(
        description="IP addresses of monitors (for external clusters).",
    )
    mountpoint: str | None = Field(
        description="mount point",
    )
    namespace: str | None = Field(
        description="Namespace.",
    )
    nocow: bool | int | str | None = Field(
        default=0,
        description="Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.",
    )
    nodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    nowritecache: bool | int | str | None = Field(
        description="disable write caching on the target",
    )
    options: str | None = Field(
        description="NFS mount options (see \u0027man nfs\u0027)",
    )
    password: str | None = Field(
        max_length=256,
        description="Password for accessing the share/datastore.",
    )
    pool: str | None = Field(
        description="Pool.",
    )
    port: int | str | None = Field(
        default=8007,
        ge=1,
        le=65535,
        description="For non default port.",
    )
    preallocation: Literal["falloc", "full", "metadata", "off"] | None = Field(
        default="metadata",
        description="Preallocation mode for raw and qcow2 images. Using \u0027metadata\u0027 on raw images results in preallocation=off.",
    )
    prune_backups: str | None = Field(
        description="The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.",
        serialization_alias="prune-backups",
    )
    saferemove: bool | int | str | None = Field(
        description="Zero-out data when removing LVs.",
    )
    saferemove_throughput: str | None = Field(
        description="Wipe throughput (cstream -t parameter value).",
    )
    server: str | None = Field(
        description="Server IP or DNS name.",
    )
    server2: str | None = Field(
        description="Backup volfile server IP or DNS name.",
    )
    shared: bool | int | str | None = Field(
        description="Mark storage as shared.",
    )
    smbversion: Literal["2.0", "2.1", "3", "3.0", "3.11", "default"] | None = Field(
        default="default",
        description="SMB protocol version. \u0027default\u0027 if not set, negotiates the highest SMB2+ version supported by both the client and server.",
    )
    sparse: bool | int | str | None = Field(
        description="use sparse volumes",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    subdir: str | None = Field(
        description="Subdir to mount.",
    )
    tagged_only: bool | int | str | None = Field(
        description="Only use logical volumes tagged with \u0027pve-vm-ID\u0027.",
    )
    transport: Literal["rdma", "tcp", "unix"] | None = Field(
        description="Gluster transport: tcp or rdma",
    )
    username: str | None = Field(
        description="RBD Id.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Storage_StoragePUTResponse(BaseModel):
    """
    Response model for /storage/{storage} PUT
    """
    data: dict[str, Any] = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

