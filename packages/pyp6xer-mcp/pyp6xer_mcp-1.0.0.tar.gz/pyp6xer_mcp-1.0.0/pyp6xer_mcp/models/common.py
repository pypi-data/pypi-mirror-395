"""Common models and base configuration for PyP6Xer MCP Server."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ResponseFormat(str, Enum):
    """Output format for tool responses."""

    MARKDOWN = "markdown"
    JSON = "json"


class ExportType(str, Enum):
    """Types of data that can be exported to CSV."""

    ACTIVITIES = "activities"
    CRITICAL_PATH = "critical_path"
    FLOAT_ANALYSIS = "float_analysis"
    RESOURCES = "resources"
    WBS = "wbs"
    SCHEDULE_QUALITY = "schedule_quality"


# Base configuration for all input models
_BASE_CONFIG = ConfigDict(str_strip_whitespace=True, extra="forbid")


class XerCacheKeyInput(BaseModel):
    """Input model for operations requiring a cached XER reference."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(
        ...,
        description="Cache key of the loaded XER file (file path or custom key used during loading)",
        min_length=1,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable",
    )


class ProjectInput(BaseModel):
    """Input model for project-specific operations."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID or short name. If not provided, uses the first project.",
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable",
    )
