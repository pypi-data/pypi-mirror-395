"""Resource and structure-related input models for PyP6Xer MCP Server."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import ResponseFormat

_BASE_CONFIG = ConfigDict(str_strip_whitespace=True, extra="forbid")


class ResourceUtilizationInput(BaseModel):
    """Input model for resource utilization analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    resource_type: Optional[str] = Field(
        default=None,
        description="Filter by resource type: 'RT_Labor', 'RT_Mat', 'RT_Equip', or None for all",
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class CalendarInput(BaseModel):
    """Input model for calendar information."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    calendar_id: Optional[str] = Field(
        default=None, description="Specific calendar ID to get details for"
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class ProgressSummaryInput(BaseModel):
    """Input model for progress summary."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class EarnedValueInput(BaseModel):
    """Input model for earned value analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class WbsInput(BaseModel):
    """Input model for WBS analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    max_depth: int = Field(
        default=10, description="Maximum depth to traverse in WBS hierarchy", ge=1, le=20
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)
