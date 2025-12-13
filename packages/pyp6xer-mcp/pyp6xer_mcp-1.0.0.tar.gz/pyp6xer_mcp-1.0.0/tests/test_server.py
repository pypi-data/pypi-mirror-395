"""Tests for the MCP server initialization and basic functionality.

These tests verify backward compatibility with the monolith exports
from the pyp6xer_mcp package __init__.py.
"""

import pytest
from pyp6xer_mcp import mcp


def test_server_name():
    """Test that the server has the correct name."""
    assert mcp.name == "pyp6xer_mcp"


def test_server_imports():
    """Test that required modules can be imported."""
    # Test core dependencies
    import mcp as mcp_module
    import pydantic
    import xerparser  # pyp6xer package provides xerparser module

    assert mcp_module is not None
    assert pydantic is not None
    assert xerparser is not None


def test_response_format_enum():
    """Test ResponseFormat enum exists and has expected values."""
    from pyp6xer_mcp import ResponseFormat

    assert hasattr(ResponseFormat, "MARKDOWN")
    assert hasattr(ResponseFormat, "JSON")
    assert ResponseFormat.MARKDOWN.value == "markdown"
    assert ResponseFormat.JSON.value == "json"


def test_pydantic_models_exist():
    """Test that key Pydantic models are defined."""
    from pyp6xer_mcp import LoadXerInput, ResponseFormat

    # Test that we can create a model instance
    load_input = LoadXerInput(file_path="/test/path.xer", cache_key="test")
    assert load_input.file_path == "/test/path.xer"
    assert load_input.cache_key == "test"


def test_pydantic_model_validation():
    """Test that Pydantic models validate correctly."""
    from pyp6xer_mcp import LoadXerInput

    # Test whitespace stripping
    load_input = LoadXerInput(file_path="  /test/path.xer  ", cache_key="  test  ")
    assert load_input.file_path == "/test/path.xer"
    assert load_input.cache_key == "test"


def test_pydantic_model_forbids_extra_fields():
    """Test that models reject extra fields."""
    from pyp6xer_mcp import LoadXerInput
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        LoadXerInput(
            file_path="/test/path.xer", cache_key="test", invalid_field="should_fail"
        )

    assert "Extra inputs are not permitted" in str(exc_info.value)


def test_xer_cache_exists():
    """Test that the global XER cache exists."""
    from pyp6xer_mcp import _xer_cache

    assert _xer_cache is not None
    assert isinstance(_xer_cache, dict)


def test_helper_functions_exist():
    """Test that helper functions are defined."""
    from pyp6xer_mcp import (
        _get_xer,
        _get_project,
        _safe_getattr,
        _format_activity,
        _to_markdown_table,
    )

    # These are internal functions but good to verify they exist
    assert callable(_get_xer)
    assert callable(_get_project)
    assert callable(_safe_getattr)
    assert callable(_format_activity)
    assert callable(_to_markdown_table)
