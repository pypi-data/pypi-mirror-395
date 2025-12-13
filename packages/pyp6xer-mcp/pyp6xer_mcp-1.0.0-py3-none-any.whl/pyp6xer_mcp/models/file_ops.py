"""File operation input models for PyP6Xer MCP Server."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import ExportType, ResponseFormat

_BASE_CONFIG = ConfigDict(str_strip_whitespace=True, extra="forbid")


class LoadXerInput(BaseModel):
    """Input model for loading an XER file."""

    model_config = _BASE_CONFIG

    file_path: Optional[str] = Field(
        default=None,
        description=(
            "Path or URL to the XER file. Supports local paths (e.g., '/path/to/project.xer') "
            "OR URLs (e.g., 'https://example.com/project.xer'). Required unless file_content is provided."
        ),
        min_length=1,
    )
    file_content: Optional[str] = Field(
        default=None,
        description=(
            "Base64-encoded XER file content. Use this when the AI has access to the file "
            "(e.g., user uploaded to ChatGPT/Claude.ai) but the MCP server cannot access the file path. "
            "The AI should read the file and base64-encode it."
        ),
    )
    cache_key: Optional[str] = Field(
        default=None,
        description=(
            "Optional key to cache the loaded XER data for subsequent operations. "
            "If not provided, uses the file path or 'uploaded_file'."
        ),
    )


class WriteXerInput(BaseModel):
    """Input model for writing an XER file."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    output_path: str = Field(..., description="Path for the output XER file", min_length=1)


class CsvExportInput(BaseModel):
    """Input model for CSV export."""

    model_config = _BASE_CONFIG

    cache_key: str = Field(..., description="Cache key of the loaded XER file", min_length=1)
    output_path: str = Field(
        ...,
        description="Path where the CSV file will be saved (e.g., '/path/to/output.csv')",
        min_length=1,
    )
    export_type: ExportType = Field(
        default=ExportType.ACTIVITIES,
        description=(
            "Type of data to export: 'activities', 'critical_path', 'float_analysis', "
            "'resources', 'wbs', or 'schedule_quality'"
        ),
    )
    project_id: Optional[str] = Field(
        default=None, description="Optional project ID or short name to filter data"
    )
    status_filter: Optional[str] = Field(
        default=None,
        description="Optional status filter for activities: 'TK_Complete', 'TK_Active', 'TK_NotStarted'",
    )
