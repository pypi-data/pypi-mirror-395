"""Activity-related input models for PyP6Xer MCP Server."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import ResponseFormat

_BASE_CONFIG = ConfigDict(str_strip_whitespace=True, extra="forbid")


class ListActivitiesInput(BaseModel):
    """Input model for listing activities."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name filter")
    status_filter: Optional[str] = Field(
        default=None,
        description="Filter by status: 'TK_Complete', 'TK_Active', 'TK_NotStarted', or 'all'",
    )
    wbs_id: Optional[str] = Field(default=None, description="Filter by WBS ID")
    limit: int = Field(
        default=50, description="Maximum number of activities to return", ge=1, le=500
    )
    offset: int = Field(default=0, description="Number of activities to skip", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class ActivityDetailInput(BaseModel):
    """Input model for getting activity details."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    activity_code: str = Field(
        ..., description="Activity code (task_code) to look up", min_length=1
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class SearchActivitiesInput(BaseModel):
    """Input model for searching activities."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    search_term: str = Field(
        ..., description="Text to search for in activity codes and names", min_length=1
    )
    project_id: Optional[str] = Field(default=None, description="Project ID or short name filter")
    limit: int = Field(default=50, description="Maximum number of results", ge=1, le=200)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class UpdateActivityInput(BaseModel):
    """Input model for updating an activity."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    activity_code: str = Field(..., description="Activity code to update", min_length=1)
    phys_complete_pct: Optional[float] = Field(
        default=None, description="Physical completion percentage (0-100)", ge=0, le=100
    )
    status_code: Optional[str] = Field(
        default=None,
        description="New status: 'TK_Complete', 'TK_Active', or 'TK_NotStarted'",
    )
