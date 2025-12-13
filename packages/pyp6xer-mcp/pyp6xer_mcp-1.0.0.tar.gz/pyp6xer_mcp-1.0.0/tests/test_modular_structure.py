"""Tests for the modular package structure.

These tests verify that the refactored modular structure works correctly.
"""

import pytest


class TestModularImports:
    """Test that the modular package structure imports correctly."""

    def test_server_import(self):
        """Test importing mcp from the modular server module."""
        from pyp6xer_mcp.server import mcp

        assert mcp.name == "pyp6xer_mcp"

    def test_models_common_import(self):
        """Test importing common models."""
        from pyp6xer_mcp.models.common import ResponseFormat, ExportType

        assert ResponseFormat.MARKDOWN.value == "markdown"
        assert ResponseFormat.JSON.value == "json"
        assert ExportType.ACTIVITIES.value == "activities"

    def test_models_file_ops_import(self):
        """Test importing file operations models."""
        from pyp6xer_mcp.models.file_ops import LoadXerInput, WriteXerInput

        load = LoadXerInput(file_path="/test.xer")
        assert load.file_path == "/test.xer"

    def test_models_activities_import(self):
        """Test importing activity models."""
        from pyp6xer_mcp.models.activities import (
            ListActivitiesInput,
            ActivityDetailInput,
            SearchActivitiesInput,
        )

        assert ListActivitiesInput is not None
        assert ActivityDetailInput is not None
        assert SearchActivitiesInput is not None

    def test_core_cache_import(self):
        """Test importing the XerCache class."""
        from pyp6xer_mcp.core.cache import XerCache, xer_cache

        assert isinstance(xer_cache, XerCache)
        assert hasattr(xer_cache, "get")
        assert hasattr(xer_cache, "set")
        assert hasattr(xer_cache, "keys")

    def test_core_formatters_import(self):
        """Test importing formatter functions."""
        from pyp6xer_mcp.core.formatters import (
            format_activity,
            format_resource,
            format_project,
            to_markdown_table,
        )

        assert callable(format_activity)
        assert callable(format_resource)
        assert callable(format_project)
        assert callable(to_markdown_table)

    def test_core_helpers_import(self):
        """Test importing helper functions."""
        from pyp6xer_mcp.core.helpers import get_project, get_project_from_dict
        from pyp6xer_mcp.core.formatters import safe_getattr

        assert callable(safe_getattr)
        assert callable(get_project)
        assert callable(get_project_from_dict)


class TestToolRegistration:
    """Test that all tools are properly registered."""

    def test_tool_count(self):
        """Test that exactly 22 tools are registered."""
        from pyp6xer_mcp.server import mcp

        tools = mcp._tool_manager._tools
        assert len(tools) == 22, f"Expected 22 tools, got {len(tools)}"

    def test_file_ops_tools_registered(self):
        """Test that file operation tools are registered."""
        from pyp6xer_mcp.server import mcp

        tools = mcp._tool_manager._tools
        expected = [
            "pyp6xer_load_file",
            "pyp6xer_write_file",
            "pyp6xer_clear_cache",
            "pyp6xer_export_csv",
        ]
        for tool_name in expected:
            assert tool_name in tools, f"Tool {tool_name} not registered"

    def test_analysis_tools_registered(self):
        """Test that analysis tools are registered."""
        from pyp6xer_mcp.server import mcp

        tools = mcp._tool_manager._tools
        expected = [
            "pyp6xer_critical_path",
            "pyp6xer_float_analysis",
            "pyp6xer_schedule_quality",
            "pyp6xer_schedule_health_check",
        ]
        for tool_name in expected:
            assert tool_name in tools, f"Tool {tool_name} not registered"


class TestPromptRegistration:
    """Test that prompts are properly registered."""

    def test_prompt_count(self):
        """Test that exactly 5 prompts are registered."""
        from pyp6xer_mcp.server import mcp

        prompts = mcp._prompt_manager._prompts
        assert len(prompts) == 5, f"Expected 5 prompts, got {len(prompts)}"

    def test_prompts_registered(self):
        """Test that all prompts are registered."""
        from pyp6xer_mcp.server import mcp

        prompts = mcp._prompt_manager._prompts
        expected = [
            "analyze_critical_path",
            "export_schedule_dashboard",
            "compare_baseline_to_actual",
            "identify_schedule_quality_issues",
            "generate_executive_summary",
        ]
        for prompt_name in expected:
            assert prompt_name in prompts, f"Prompt {prompt_name} not registered"


class TestResourceRegistration:
    """Test that resources are properly registered."""

    def test_resource_count(self):
        """Test that resources and templates are registered."""
        from pyp6xer_mcp.server import mcp

        rm = mcp._resource_manager
        # 1 static resource + 2 templates = 3 total
        total = len(rm._resources) + len(rm._templates)
        assert total == 3, f"Expected 3 resources/templates, got {total}"

    def test_resources_registered(self):
        """Test that all resources are registered."""
        from pyp6xer_mcp.server import mcp

        rm = mcp._resource_manager
        # Static resource
        assert "schedule://projects" in rm._resources
        # Templates
        assert "schedule://{cache_key}/summary" in rm._templates
        assert "schedule://{cache_key}/critical" in rm._templates


class TestContextHelper:
    """Test the context helper function."""

    def test_context_helper_import(self):
        """Test importing the context helper."""
        from pyp6xer_mcp.context import get_xer_files_context

        assert callable(get_xer_files_context)

    def test_context_helper_no_files(self):
        """Test context helper returns message when no files loaded."""
        from pyp6xer_mcp.context import get_xer_files_context
        from pyp6xer_mcp.core import xer_cache

        # Clear cache to ensure no files
        xer_cache.clear()
        result = get_xer_files_context()
        assert "No Primavera P6 XER files" in result


class TestHttpLayer:
    """Test the HTTP layer components."""

    def test_middleware_import(self):
        """Test importing the auth middleware."""
        from pyp6xer_mcp.http.middleware import APIKeyAuthMiddleware

        assert APIKeyAuthMiddleware is not None

    def test_routes_import(self):
        """Test importing the route handlers."""
        from pyp6xer_mcp.http.routes import health_check, upload_file

        assert callable(health_check)
        assert callable(upload_file)


class TestCli:
    """Test the CLI entry point."""

    def test_cli_import(self):
        """Test importing the CLI main function."""
        from pyp6xer_mcp.cli import main

        assert callable(main)
