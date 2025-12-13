"""Schedule analysis input models for PyP6Xer MCP Server."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import ResponseFormat

_BASE_CONFIG = ConfigDict(str_strip_whitespace=True, extra="forbid")


class CriticalPathInput(BaseModel):
    """Input model for critical path analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    float_threshold_hours: int = Field(
        default=0,
        description="Activities with total float <= this value (in hours) are considered critical",
        ge=0,
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class ScheduleQualityInput(BaseModel):
    """Input model for schedule quality checks."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    max_duration_days: int = Field(
        default=20, description="Flag activities with duration greater than this value", ge=1
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class FloatAnalysisInput(BaseModel):
    """Input model for float analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    float_categories: Optional[List[int]] = Field(
        default=None,
        description=(
            "Custom float category thresholds in days (e.g., [0, 5, 10, 20]). "
            "Default: [0, 5, 10, 20, 40]"
        ),
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class RelationshipAnalysisInput(BaseModel):
    """Input model for relationship analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    relationship_type: Optional[str] = Field(
        default=None,
        description=(
            "Filter by type: 'PR_FS' (Finish-Start), 'PR_SS' (Start-Start), "
            "'PR_FF' (Finish-Finish), 'PR_SF' (Start-Finish)"
        ),
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class SlippingActivitiesInput(BaseModel):
    """Input model for slipping activities analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    threshold_days: float = Field(
        default=0, description="Only show activities slipping by more than this many days", ge=0
    )
    include_completed: bool = Field(
        default=False, description="Include completed activities in the analysis"
    )
    limit: int = Field(
        default=50, description="Maximum number of activities to return", ge=1, le=500
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class ScheduleHealthCheckInput(BaseModel):
    """Input model for schedule health check analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class WorkPackageSummaryInput(BaseModel):
    """Input model for work package summary analysis."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(default=None, description="Project ID or short name")
    prefix_list: List[str] = Field(
        ...,
        description="List of activity code prefixes to group by (e.g., ['KH-', 'MoS-', 'CIVIL-'])",
        min_length=1,
    )
    include_unmatched: bool = Field(
        default=True,
        description="Include activities not matching any prefix in an 'Other' category",
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)
