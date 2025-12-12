"""
Pydantic models for pools API endpoints.

This module contains auto-generated Pydantic v2 models for request and response
validation in the pools API endpoints.
"""

from ..base.types import ProxmoxNode, ProxmoxVMID
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Literal

class PoolsGETResponse(BaseModel):
    """
    Response model for /pools GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class PoolsPOSTRequest(BaseModel):
    """
    Request model for /pools POST
    """
    comment: str | None = Field(
    )
    poolid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Pools_PoolidDELETERequest(BaseModel):
    """
    Request model for /pools/{poolid} DELETE
    """
    poolid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Pools_PoolidGETRequest(BaseModel):
    """
    Request model for /pools/{poolid} GET
    """
    poolid: str = Field(
    )
    type: Literal["lxc", "qemu", "storage"] | None = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Pools_PoolidGETResponse(BaseModel):
    """
    Response model for /pools/{poolid} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Pools_PoolidPUTRequest(BaseModel):
    """
    Request model for /pools/{poolid} PUT
    """
    comment: str | None = Field(
    )
    delete: bool | int | str | None = Field(
        description="Remove vms/storage (instead of adding it).",
    )
    poolid: str = Field(
    )
    storage: list[str] | None = Field(
        description="List of storage IDs.",
    )
    vms: list[ProxmoxVMID] | None = Field(
        description="List of virtual machines.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

