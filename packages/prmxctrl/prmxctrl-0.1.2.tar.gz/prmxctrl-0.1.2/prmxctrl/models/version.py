"""
Pydantic models for version API endpoints.

This module contains auto-generated Pydantic v2 models for request and response
validation in the version API endpoints.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Any

class VersionGETResponse(BaseModel):
    """
    Response model for /version GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

