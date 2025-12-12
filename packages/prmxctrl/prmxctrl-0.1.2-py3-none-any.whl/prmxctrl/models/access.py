"""
Pydantic models for access API endpoints.

This module contains auto-generated Pydantic v2 models for request and response
validation in the access API endpoints.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Literal

class AccessGETResponse(BaseModel):
    """
    Response model for /access GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_UsersGETRequest(BaseModel):
    """
    Request model for /access/users GET
    """
    enabled: bool | int | str | None = Field(
        description="Optional filter for enable property.",
    )
    full: bool | int | str | None = Field(
        default=0,
        description="Include group and token information.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_UsersGETResponse(BaseModel):
    """
    Response model for /access/users GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_UsersPOSTRequest(BaseModel):
    """
    Request model for /access/users POST
    """
    comment: str | None = Field(
    )
    email: str | None = Field(
    )
    enable: bool | int | str | None = Field(
        default=1,
        description="Enable the account (default). You can set this to \u00270\u0027 to disable the account",
    )
    expire: int | str | None = Field(
        ge=0,
        description="Account expiration date (seconds since epoch). \u00270\u0027 means no expiration date.",
    )
    firstname: str | None = Field(
    )
    groups: str | None = Field(
    )
    keys: str | None = Field(
        description="Keys for two factor auth (yubico).",
    )
    lastname: str | None = Field(
    )
    password: str | None = Field(
        max_length=64,
        description="Initial password.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_UseridDELETERequest(BaseModel):
    """
    Request model for /access/users/{userid} DELETE
    """
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_UseridGETRequest(BaseModel):
    """
    Request model for /access/users/{userid} GET
    """
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_UseridGETResponse(BaseModel):
    """
    Response model for /access/users/{userid} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_UseridPUTRequest(BaseModel):
    """
    Request model for /access/users/{userid} PUT
    """
    append: bool | int | str | None = Field(
    )
    comment: str | None = Field(
    )
    email: str | None = Field(
    )
    enable: bool | int | str | None = Field(
        default=1,
        description="Enable the account (default). You can set this to \u00270\u0027 to disable the account",
    )
    expire: int | str | None = Field(
        ge=0,
        description="Account expiration date (seconds since epoch). \u00270\u0027 means no expiration date.",
    )
    firstname: str | None = Field(
    )
    groups: str | None = Field(
    )
    keys: str | None = Field(
        description="Keys for two factor auth (yubico).",
    )
    lastname: str | None = Field(
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_TfaGETRequest(BaseModel):
    """
    Request model for /access/users/{userid}/tfa GET
    """
    multiple: bool | int | str | None = Field(
        default=0,
        description="Request all entries as an array.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_TfaGETResponse(BaseModel):
    """
    Response model for /access/users/{userid}/tfa GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_TokenGETRequest(BaseModel):
    """
    Request model for /access/users/{userid}/token GET
    """
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_TokenGETResponse(BaseModel):
    """
    Response model for /access/users/{userid}/token GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_Token_TokenidDELETERequest(BaseModel):
    """
    Request model for /access/users/{userid}/token/{tokenid} DELETE
    """
    tokenid: str = Field(
        description="User-specific token identifier.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_Token_TokenidGETRequest(BaseModel):
    """
    Request model for /access/users/{userid}/token/{tokenid} GET
    """
    tokenid: str = Field(
        description="User-specific token identifier.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_Token_TokenidGETResponse(BaseModel):
    """
    Response model for /access/users/{userid}/token/{tokenid} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_Token_TokenidPOSTRequest(BaseModel):
    """
    Request model for /access/users/{userid}/token/{tokenid} POST
    """
    comment: str | None = Field(
    )
    expire: int | str | None = Field(
        default="same as user",
        ge=0,
        description="API token expiration date (seconds since epoch). \u00270\u0027 means no expiration date.",
    )
    privsep: bool | int | str | None = Field(
        default=1,
        description="Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.",
    )
    tokenid: str = Field(
        description="User-specific token identifier.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_Token_TokenidPOSTResponse(BaseModel):
    """
    Response model for /access/users/{userid}/token/{tokenid} POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_Token_TokenidPUTRequest(BaseModel):
    """
    Request model for /access/users/{userid}/token/{tokenid} PUT
    """
    comment: str | None = Field(
    )
    expire: int | str | None = Field(
        default="same as user",
        ge=0,
        description="API token expiration date (seconds since epoch). \u00270\u0027 means no expiration date.",
    )
    privsep: bool | int | str | None = Field(
        default=1,
        description="Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.",
    )
    tokenid: str = Field(
        description="User-specific token identifier.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Users_Userid_Token_TokenidPUTResponse(BaseModel):
    """
    Response model for /access/users/{userid}/token/{tokenid} PUT
    """
    data: dict[str, Any] = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_GroupsGETResponse(BaseModel):
    """
    Response model for /access/groups GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_GroupsPOSTRequest(BaseModel):
    """
    Request model for /access/groups POST
    """
    comment: str | None = Field(
    )
    groupid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Groups_GroupidDELETERequest(BaseModel):
    """
    Request model for /access/groups/{groupid} DELETE
    """
    groupid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Groups_GroupidGETRequest(BaseModel):
    """
    Request model for /access/groups/{groupid} GET
    """
    groupid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Groups_GroupidGETResponse(BaseModel):
    """
    Response model for /access/groups/{groupid} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Groups_GroupidPUTRequest(BaseModel):
    """
    Request model for /access/groups/{groupid} PUT
    """
    comment: str | None = Field(
    )
    groupid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_RolesGETResponse(BaseModel):
    """
    Response model for /access/roles GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_RolesPOSTRequest(BaseModel):
    """
    Request model for /access/roles POST
    """
    privs: str | None = Field(
    )
    roleid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Roles_RoleidDELETERequest(BaseModel):
    """
    Request model for /access/roles/{roleid} DELETE
    """
    roleid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Roles_RoleidGETRequest(BaseModel):
    """
    Request model for /access/roles/{roleid} GET
    """
    roleid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Roles_RoleidGETResponse(BaseModel):
    """
    Response model for /access/roles/{roleid} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Roles_RoleidPUTRequest(BaseModel):
    """
    Request model for /access/roles/{roleid} PUT
    """
    append: bool | int | str | None = Field(
    )
    privs: str | None = Field(
    )
    roleid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_AclGETResponse(BaseModel):
    """
    Response model for /access/acl GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_AclPUTRequest(BaseModel):
    """
    Request model for /access/acl PUT
    """
    delete: bool | int | str | None = Field(
        description="Remove permissions (instead of adding it).",
    )
    groups: str | None = Field(
        description="List of groups.",
    )
    path: str = Field(
        description="Access control path",
    )
    propagate: bool | int | str | None = Field(
        default=1,
        description="Allow to propagate (inherit) permissions.",
    )
    roles: str = Field(
        description="List of roles.",
    )
    tokens: str | None = Field(
        description="List of API tokens.",
    )
    users: str | None = Field(
        description="List of users.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_DomainsGETResponse(BaseModel):
    """
    Response model for /access/domains GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_DomainsPOSTRequest(BaseModel):
    """
    Request model for /access/domains POST
    """
    acr_values: str | None = Field(
        description="Specifies the Authentication Context Class Reference values that theAuthorization Server is being requested to use for the Auth Request.",
        serialization_alias="acr-values",
    )
    autocreate: bool | int | str | None = Field(
        default=0,
        description="Automatically create users if they do not exist.",
    )
    base_dn: str | None = Field(
        max_length=256,
        description="LDAP base domain name",
    )
    bind_dn: str | None = Field(
        max_length=256,
        description="LDAP bind domain name",
    )
    capath: str | None = Field(
        default="/etc/ssl/certs",
        description="Path to the CA certificate store",
    )
    case_sensitive: bool | int | str | None = Field(
        default=1,
        description="username is case-sensitive",
        serialization_alias="case-sensitive",
    )
    cert: str | None = Field(
        description="Path to the client certificate",
    )
    certkey: str | None = Field(
        description="Path to the client certificate key",
    )
    client_id: str | None = Field(
        max_length=256,
        description="OpenID Client ID",
        serialization_alias="client-id",
    )
    client_key: str | None = Field(
        max_length=256,
        description="OpenID Client Key",
        serialization_alias="client-key",
    )
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    default: bool | int | str | None = Field(
        description="Use this as default realm",
    )
    domain: str | None = Field(
        max_length=256,
        description="AD domain name",
    )
    filter: str | None = Field(
        max_length=2048,
        description="LDAP filter for user sync.",
    )
    group_classes: str | None = Field(
        default="groupOfNames, group, univentionGroup, ipausergroup",
        description="The objectclasses for groups.",
    )
    group_dn: str | None = Field(
        max_length=256,
        description="LDAP base domain name for group sync. If not set, the base_dn will be used.",
    )
    group_filter: str | None = Field(
        max_length=2048,
        description="LDAP filter for group sync.",
    )
    group_name_attr: str | None = Field(
        max_length=256,
        description="LDAP attribute representing a groups name. If not set or found, the first value of the DN will be used as name.",
    )
    issuer_url: str | None = Field(
        max_length=256,
        description="OpenID Issuer Url",
        serialization_alias="issuer-url",
    )
    mode: Literal["ldap", "ldap+starttls", "ldaps"] | None = Field(
        default="ldap",
        description="LDAP protocol mode.",
    )
    password: str | None = Field(
        description="LDAP bind password. Will be stored in \u0027/etc/pve/priv/realm/\u003cREALM\u003e.pw\u0027.",
    )
    port: int | str | None = Field(
        ge=1,
        le=65535,
        description="Server port.",
    )
    prompt: str | None = Field(
        description="Specifies whether the Authorization Server prompts the End-User for reauthentication and consent.",
    )
    realm: str = Field(
        max_length=32,
        description="Authentication domain ID",
    )
    scopes: str | None = Field(
        default="email profile",
        description="Specifies the scopes (user details) that should be authorized and returned, for example \u0027email\u0027 or \u0027profile\u0027.",
    )
    secure: bool | int | str | None = Field(
        description="Use secure LDAPS protocol. DEPRECATED: use \u0027mode\u0027 instead.",
    )
    server1: str | None = Field(
        max_length=256,
        description="Server IP address (or DNS name)",
    )
    server2: str | None = Field(
        max_length=256,
        description="Fallback Server IP address (or DNS name)",
    )
    sslversion: Literal["tlsv1", "tlsv1_1", "tlsv1_2", "tlsv1_3"] | None = Field(
        description="LDAPS TLS/SSL version. It\u0027s not recommended to use version older than 1.2!",
    )
    sync_defaults_options: str | None = Field(
        description="The default options for behavior of synchronizations.",
        serialization_alias="sync-defaults-options",
    )
    sync_attributes: str | None = Field(
        description="Comma separated list of key=value pairs for specifying which LDAP attributes map to which PVE user field. For example, to map the LDAP attribute \u0027mail\u0027 to PVEs \u0027email\u0027, write  \u0027email=mail\u0027. By default, each PVE user field is represented  by an LDAP attribute of the same name.",
    )
    tfa: str | None = Field(
        max_length=128,
        description="Use Two-factor authentication.",
    )
    type: Literal["ad", "ldap", "openid", "pam", "pve"] = Field(
        description="Realm type.",
    )
    user_attr: str | None = Field(
        max_length=256,
        description="LDAP user attribute name",
    )
    user_classes: str | None = Field(
        default="inetorgperson, posixaccount, person, user",
        description="The objectclasses for users.",
    )
    username_claim: str | None = Field(
        description="OpenID claim used to generate the unique username.",
        serialization_alias="username-claim",
    )
    verify: bool | int | str | None = Field(
        default=0,
        description="Verify the server\u0027s SSL certificate",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Domains_RealmDELETERequest(BaseModel):
    """
    Request model for /access/domains/{realm} DELETE
    """
    realm: str = Field(
        max_length=32,
        description="Authentication domain ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Domains_RealmGETRequest(BaseModel):
    """
    Request model for /access/domains/{realm} GET
    """
    realm: str = Field(
        max_length=32,
        description="Authentication domain ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Domains_RealmGETResponse(BaseModel):
    """
    Response model for /access/domains/{realm} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Domains_RealmPUTRequest(BaseModel):
    """
    Request model for /access/domains/{realm} PUT
    """
    acr_values: str | None = Field(
        description="Specifies the Authentication Context Class Reference values that theAuthorization Server is being requested to use for the Auth Request.",
        serialization_alias="acr-values",
    )
    autocreate: bool | int | str | None = Field(
        default=0,
        description="Automatically create users if they do not exist.",
    )
    base_dn: str | None = Field(
        max_length=256,
        description="LDAP base domain name",
    )
    bind_dn: str | None = Field(
        max_length=256,
        description="LDAP bind domain name",
    )
    capath: str | None = Field(
        default="/etc/ssl/certs",
        description="Path to the CA certificate store",
    )
    case_sensitive: bool | int | str | None = Field(
        default=1,
        description="username is case-sensitive",
        serialization_alias="case-sensitive",
    )
    cert: str | None = Field(
        description="Path to the client certificate",
    )
    certkey: str | None = Field(
        description="Path to the client certificate key",
    )
    client_id: str | None = Field(
        max_length=256,
        description="OpenID Client ID",
        serialization_alias="client-id",
    )
    client_key: str | None = Field(
        max_length=256,
        description="OpenID Client Key",
        serialization_alias="client-key",
    )
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    default: bool | int | str | None = Field(
        description="Use this as default realm",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    domain: str | None = Field(
        max_length=256,
        description="AD domain name",
    )
    filter: str | None = Field(
        max_length=2048,
        description="LDAP filter for user sync.",
    )
    group_classes: str | None = Field(
        default="groupOfNames, group, univentionGroup, ipausergroup",
        description="The objectclasses for groups.",
    )
    group_dn: str | None = Field(
        max_length=256,
        description="LDAP base domain name for group sync. If not set, the base_dn will be used.",
    )
    group_filter: str | None = Field(
        max_length=2048,
        description="LDAP filter for group sync.",
    )
    group_name_attr: str | None = Field(
        max_length=256,
        description="LDAP attribute representing a groups name. If not set or found, the first value of the DN will be used as name.",
    )
    issuer_url: str | None = Field(
        max_length=256,
        description="OpenID Issuer Url",
        serialization_alias="issuer-url",
    )
    mode: Literal["ldap", "ldap+starttls", "ldaps"] | None = Field(
        default="ldap",
        description="LDAP protocol mode.",
    )
    password: str | None = Field(
        description="LDAP bind password. Will be stored in \u0027/etc/pve/priv/realm/\u003cREALM\u003e.pw\u0027.",
    )
    port: int | str | None = Field(
        ge=1,
        le=65535,
        description="Server port.",
    )
    prompt: str | None = Field(
        description="Specifies whether the Authorization Server prompts the End-User for reauthentication and consent.",
    )
    realm: str = Field(
        max_length=32,
        description="Authentication domain ID",
    )
    scopes: str | None = Field(
        default="email profile",
        description="Specifies the scopes (user details) that should be authorized and returned, for example \u0027email\u0027 or \u0027profile\u0027.",
    )
    secure: bool | int | str | None = Field(
        description="Use secure LDAPS protocol. DEPRECATED: use \u0027mode\u0027 instead.",
    )
    server1: str | None = Field(
        max_length=256,
        description="Server IP address (or DNS name)",
    )
    server2: str | None = Field(
        max_length=256,
        description="Fallback Server IP address (or DNS name)",
    )
    sslversion: Literal["tlsv1", "tlsv1_1", "tlsv1_2", "tlsv1_3"] | None = Field(
        description="LDAPS TLS/SSL version. It\u0027s not recommended to use version older than 1.2!",
    )
    sync_defaults_options: str | None = Field(
        description="The default options for behavior of synchronizations.",
        serialization_alias="sync-defaults-options",
    )
    sync_attributes: str | None = Field(
        description="Comma separated list of key=value pairs for specifying which LDAP attributes map to which PVE user field. For example, to map the LDAP attribute \u0027mail\u0027 to PVEs \u0027email\u0027, write  \u0027email=mail\u0027. By default, each PVE user field is represented  by an LDAP attribute of the same name.",
    )
    tfa: str | None = Field(
        max_length=128,
        description="Use Two-factor authentication.",
    )
    user_attr: str | None = Field(
        max_length=256,
        description="LDAP user attribute name",
    )
    user_classes: str | None = Field(
        default="inetorgperson, posixaccount, person, user",
        description="The objectclasses for users.",
    )
    verify: bool | int | str | None = Field(
        default=0,
        description="Verify the server\u0027s SSL certificate",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Domains_Realm_SyncPOSTRequest(BaseModel):
    """
    Request model for /access/domains/{realm}/sync POST
    """
    dry_run: bool | int | str | None = Field(
        default=0,
        description="If set, does not write anything.",
        serialization_alias="dry-run",
    )
    enable_new: bool | int | str = Field(
        default="1",
        description="Enable newly synced users immediately.",
        serialization_alias="enable-new",
    )
    full: bool | int | str = Field(
        description="DEPRECATED: use \u0027remove-vanished\u0027 instead. If set, uses the LDAP Directory as source of truth, deleting users or groups not returned from the sync and removing all locally modified properties of synced users. If not set, only syncs information which is present in the synced data, and does not delete or modify anything else.",
    )
    purge: bool | int | str = Field(
        description="DEPRECATED: use \u0027remove-vanished\u0027 instead. Remove ACLs for users or groups which were removed from the config during a sync.",
    )
    realm: str = Field(
        max_length=32,
        description="Authentication domain ID",
    )
    remove_vanished: str = Field(
        default="none",
        description="A semicolon-seperated list of things to remove when they or the user vanishes during a sync. The following values are possible: \u0027entry\u0027 removes the user/group when not returned from the sync. \u0027properties\u0027 removes the set properties on existing user/group that do not appear in the source (even custom ones). \u0027acl\u0027 removes acls when the user/group is not returned from the sync. Instead of a list it also can be \u0027none\u0027 (the default).",
        serialization_alias="remove-vanished",
    )
    scope: Literal["both", "groups", "users"] = Field(
        description="Select what to sync.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Domains_Realm_SyncPOSTResponse(BaseModel):
    """
    Response model for /access/domains/{realm}/sync POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_OpenidGETResponse(BaseModel):
    """
    Response model for /access/openid GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Openid_Auth_UrlPOSTRequest(BaseModel):
    """
    Request model for /access/openid/auth-url POST
    """
    realm: str = Field(
        max_length=32,
        description="Authentication domain ID",
    )
    redirect_url: str = Field(
        max_length=255,
        description="Redirection Url. The client should set this to the used server url (location.origin).",
        serialization_alias="redirect-url",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Openid_Auth_UrlPOSTResponse(BaseModel):
    """
    Response model for /access/openid/auth-url POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Openid_LoginPOSTRequest(BaseModel):
    """
    Request model for /access/openid/login POST
    """
    code: str = Field(
        max_length=4096,
        description="OpenId authorization code.",
    )
    redirect_url: str = Field(
        max_length=255,
        description="Redirection Url. The client should set this to the used server url (location.origin).",
        serialization_alias="redirect-url",
    )
    state: str = Field(
        max_length=1024,
        description="OpenId state.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Openid_LoginPOSTResponse(BaseModel):
    """
    Response model for /access/openid/login POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_TfaGETResponse(BaseModel):
    """
    Response model for /access/tfa GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_TfaPOSTRequest(BaseModel):
    """
    Request model for /access/tfa POST
    """
    response: str = Field(
        description="The response to the current authentication challenge.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_TfaPOSTResponse(BaseModel):
    """
    Response model for /access/tfa POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_UseridGETRequest(BaseModel):
    """
    Request model for /access/tfa/{userid} GET
    """
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_UseridGETResponse(BaseModel):
    """
    Response model for /access/tfa/{userid} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_UseridPOSTRequest(BaseModel):
    """
    Request model for /access/tfa/{userid} POST
    """
    challenge: str | None = Field(
        description="When responding to a u2f challenge: the original challenge string",
    )
    description: str | None = Field(
        max_length=255,
        description="A description to distinguish multiple entries from one another",
    )
    password: str | None = Field(
        max_length=64,
        description="The current password.",
    )
    totp: str | None = Field(
        description="A totp URI.",
    )
    type: Literal["recovery", "totp", "u2f", "webauthn", "yubico"] = Field(
        description="TFA Entry Type.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )
    value: str | None = Field(
        description="The current value for the provided totp URI, or a Webauthn/U2F challenge response",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_UseridPOSTResponse(BaseModel):
    """
    Response model for /access/tfa/{userid} POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_Userid_IdDELETERequest(BaseModel):
    """
    Request model for /access/tfa/{userid}/{id} DELETE
    """
    id: str = Field(
        description="A TFA entry id.",
    )
    password: str | None = Field(
        max_length=64,
        description="The current password.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_Userid_IdGETRequest(BaseModel):
    """
    Request model for /access/tfa/{userid}/{id} GET
    """
    id: str = Field(
        description="A TFA entry id.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_Userid_IdGETResponse(BaseModel):
    """
    Response model for /access/tfa/{userid}/{id} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_Tfa_Userid_IdPUTRequest(BaseModel):
    """
    Request model for /access/tfa/{userid}/{id} PUT
    """
    description: str | None = Field(
        max_length=255,
        description="A description to distinguish multiple entries from one another",
    )
    enable: bool | int | str | None = Field(
        description="Whether the entry should be enabled for login.",
    )
    id: str = Field(
        description="A TFA entry id.",
    )
    password: str | None = Field(
        max_length=64,
        description="The current password.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_TicketPOSTRequest(BaseModel):
    """
    Request model for /access/ticket POST
    """
    new_format: bool | int | str | None = Field(
        default=0,
        description="With webauthn the format of half-authenticated tickts changed. New clients should pass 1 here and not worry about the old format. The old format is deprecated and will be retired with PVE-8.0",
        serialization_alias="new-format",
    )
    otp: str | None = Field(
        description="One-time password for Two-factor authentication.",
    )
    password: str = Field(
        description="The secret password. This can also be a valid ticket.",
    )
    path: str | None = Field(
        max_length=64,
        description="Verify ticket, and check if user have access \u0027privs\u0027 on \u0027path\u0027",
    )
    privs: str | None = Field(
        max_length=64,
        description="Verify ticket, and check if user have access \u0027privs\u0027 on \u0027path\u0027",
    )
    realm: str | None = Field(
        max_length=32,
        description="You can optionally pass the realm using this parameter. Normally the realm is simply added to the username \u003cusername\u003e@\u003crelam\u003e.",
    )
    tfa_challenge: str | None = Field(
        description="The signed TFA challenge string the user wants to respond to.",
        serialization_alias="tfa-challenge",
    )
    username: str = Field(
        max_length=64,
        description="User name",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_TicketPOSTResponse(BaseModel):
    """
    Response model for /access/ticket POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_PasswordPUTRequest(BaseModel):
    """
    Request model for /access/password PUT
    """
    password: str = Field(
        max_length=64,
        description="The new password.",
    )
    userid: str = Field(
        max_length=64,
        description="Full User ID, in the `name@realm` format.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_PermissionsGETRequest(BaseModel):
    """
    Request model for /access/permissions GET
    """
    path: str | None = Field(
        description="Only dump this specific path, not the whole tree.",
    )
    userid: str | None = Field(
        description="User ID or full API token ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Access_PermissionsGETResponse(BaseModel):
    """
    Response model for /access/permissions GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

