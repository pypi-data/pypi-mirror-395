"""Unit tests for get_product_quality_report tool file export functionality (STORY-025).

Tests verify error transformations, parameter validation, and service delegation.
"""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp.exceptions import ToolError

from testio_mcp.tools.product_quality_report_tool import (
    get_product_quality_report as get_product_quality_report_tool,
)
from tests.unit.test_utils import mock_service_context

get_product_quality_report = get_product_quality_report_tool.fn


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_delegates_to_service(tmp_path: Path) -> None:
    """Verify tool delegates file export to service layer."""
    # Setup: Mock context and service
    mock_ctx = MagicMock()
    mock_service = AsyncMock()

    # Mock service response (file metadata)
    mock_service.get_product_quality_report.return_value = {
        "file_path": str(tmp_path / "report.json"),
        "summary": {
            "total_tests": 2,
            "tests_by_status": {"locked": 2},
            "statuses_applied": "all",
            "total_bugs": 5,
            "bugs_by_status": {
                "active_accepted": 3,
                "auto_accepted": 1,
                "rejected": 1,
                "open": 0,
            },
            "total_accepted": 4,
            "reviewed": 4,
            "active_acceptance_rate": 0.6,
            "auto_acceptance_rate": 0.25,
            "overall_acceptance_rate": 0.8,
            "rejection_rate": 0.2,
            "review_rate": 0.8,
            "period": "all time",
        },
        "record_count": 2,
        "file_size_bytes": 1024,
        "format": "json",
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        result = await get_product_quality_report(
            product_id=123,
            output_file="report.json",
            ctx=mock_ctx,
        )

        # Verify service was called with output_file
        mock_service.get_product_quality_report.assert_called_once_with(
            product_id=123,
            start_date=None,
            end_date=None,
            statuses=None,
            output_file="report.json",
        )

        # Verify file metadata structure returned
        assert "file_path" in result
        assert "summary" in result
        assert "record_count" in result
        assert "file_size_bytes" in result
        assert "format" in result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_permission_error_transformation() -> None:
    """Verify PermissionError is transformed to ToolError with clear message."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.side_effect = PermissionError("Permission denied")

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        with pytest.raises(ToolError) as exc_info:
            await get_product_quality_report(
                product_id=123,
                output_file="report.json",
                ctx=mock_ctx,
            )

        error_msg = str(exc_info.value)
        assert "❌" in error_msg
        assert "permission" in error_msg.lower()
        assert "ℹ️" in error_msg
        assert "💡" in error_msg


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_oserror_transformation() -> None:
    """Verify OSError (disk full) is transformed to ToolError with helpful message."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.side_effect = OSError("No space left on device")

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        with pytest.raises(ToolError) as exc_info:
            await get_product_quality_report(
                product_id=123,
                output_file="report.json",
                ctx=mock_ctx,
            )

        error_msg = str(exc_info.value)
        assert "❌" in error_msg
        assert "I/O" in error_msg or "disk" in error_msg.lower()
        assert "ℹ️" in error_msg
        assert "💡" in error_msg
        assert "disk space" in error_msg.lower()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_valueerror_path_transformation() -> None:
    """Verify ValueError (invalid path) is transformed to ToolError."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.side_effect = ValueError("Path traversal detected")

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        with pytest.raises(ToolError) as exc_info:
            await get_product_quality_report(
                product_id=123,
                output_file="../../../etc/passwd",
                ctx=mock_ctx,
            )

        error_msg = str(exc_info.value)
        assert "❌" in error_msg
        assert "Invalid output file path" in error_msg
        assert "ℹ️" in error_msg
        assert "💡" in error_msg
        assert ".json" in error_msg


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_valueerror_date_parsing_caught_early() -> None:
    """Verify date parsing errors are caught by Pydantic validation (not service layer).

    After adding Pydantic input validation, invalid dates are caught at the tool
    level before reaching the service, providing better user experience with
    clear error messages.
    """
    mock_ctx = MagicMock()
    mock_service = AsyncMock()

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        # Invalid date should be caught by Pydantic validation, converted to ToolError
        with pytest.raises(ToolError, match="Invalid input"):
            await get_product_quality_report(
                product_id=123,
                start_date="invalid-date",
                ctx=mock_ctx,
            )

        # Service should NOT be called (validation fails before service invocation)
        mock_service.get_product_quality_report.assert_not_called()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_returns_full_data_when_output_file_none() -> None:
    """Verify tool returns full JSON response when output_file is None."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()

    # Mock service response (full report)
    mock_service.get_product_quality_report.return_value = {
        "summary": {
            "total_tests": 2,
            "tests_by_status": {"locked": 2},
            "statuses_applied": "all",
            "total_bugs": 5,
            "bugs_by_status": {
                "active_accepted": 3,
                "auto_accepted": 1,
                "rejected": 1,
                "open": 0,
            },
            "total_accepted": 4,
            "reviewed": 4,
            "active_acceptance_rate": 0.6,
            "auto_acceptance_rate": 0.25,
            "overall_acceptance_rate": 0.8,
            "rejection_rate": 0.2,
            "review_rate": 0.8,
            "period": "all time",
        },
        "by_test": [
            {
                "test_id": 1,
                "title": "Test 1",
                "status": "locked",
                "bugs_count": 3,
                "bugs": {
                    "active_accepted": 2,
                    "auto_accepted": 1,
                    "rejected": 0,
                    "open": 0,
                    "total_accepted": 3,
                    "reviewed": 2,
                },
            }
        ],
        "cache_stats": {
            "total_tests": 2,
            "cache_hits": 2,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 2},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        result = await get_product_quality_report(
            product_id=123,
            output_file=None,  # No file export
            ctx=mock_ctx,
        )

        # Verify full report structure returned
        assert "summary" in result
        assert "by_test" in result
        assert "cache_stats" in result

        # Verify NOT file metadata structure
        assert "file_path" not in result
        assert "record_count" not in result
        assert "file_size_bytes" not in result
        assert "format" not in result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_validates_metadata_structure() -> None:
    """Verify file export metadata is validated with FileExportMetadata model."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()

    # Mock service response with incomplete metadata (should fail validation)
    mock_service.get_product_quality_report.return_value = {
        "file_path": "/tmp/report.json",
        "summary": {"total_tests": 2},
        # Missing required fields: record_count, file_size_bytes, format
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        # Should raise ToolError (catches KeyError from missing fields)
        with pytest.raises(ToolError, match="Unexpected error"):
            await get_product_quality_report(
                product_id=123,
                output_file="report.json",
                ctx=mock_ctx,
            )


# STORY-074: Test Environment Field Tests
@pytest.mark.unit
@pytest.mark.asyncio
async def test_report_includes_test_environment_when_present() -> None:
    """Verify report includes test_environment field when provided by service (AC1, AC2)."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()

    # Mock service response with test_environment
    mock_service.get_product_quality_report.return_value = {
        "summary": {
            "total_tests": 1,
            "tests_by_status": {"locked": 1},
            "statuses_applied": "all",
            "total_bugs": 2,
            "bugs_by_status": {
                "active_accepted": 1,
                "auto_accepted": 1,
                "rejected": 0,
                "open": 0,
            },
            "total_accepted": 2,
            "reviewed": 1,
            "active_acceptance_rate": 0.5,
            "overall_acceptance_rate": 1.0,
            "period": "all time",
        },
        "by_test": [
            {
                "test_id": 123,
                "title": "Production Test",
                "status": "locked",
                "bugs_count": 2,
                "bugs": {
                    "active_accepted": 1,
                    "auto_accepted": 1,
                    "rejected": 0,
                    "open": 0,
                    "total_accepted": 2,
                    "reviewed": 1,
                },
                "test_environment": {"id": 456, "title": "Production"},
            }
        ],
        "cache_stats": {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        result = await get_product_quality_report(
            product_id=598,
            ctx=mock_ctx,
        )

        # Verify test_environment is present in by_test array
        assert "by_test" in result
        assert len(result["by_test"]) == 1
        test_entry = result["by_test"][0]

        # Verify test_environment field exists and has correct structure
        assert "test_environment" in test_entry
        assert test_entry["test_environment"] == {"id": 456, "title": "Production"}


@pytest.mark.unit
@pytest.mark.asyncio
async def test_report_handles_none_test_environment_gracefully() -> None:
    """Verify report handles None test_environment without errors (AC1, AC2)."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()

    # Mock service response with test_environment=None
    mock_service.get_product_quality_report.return_value = {
        "summary": {
            "total_tests": 1,
            "tests_by_status": {"locked": 1},
            "statuses_applied": "all",
            "total_bugs": 2,
            "bugs_by_status": {
                "active_accepted": 1,
                "auto_accepted": 1,
                "rejected": 0,
                "open": 0,
            },
            "total_accepted": 2,
            "reviewed": 1,
            "period": "all time",
        },
        "by_test": [
            {
                "test_id": 789,
                "title": "Test Without Environment",
                "status": "locked",
                "bugs_count": 2,
                "bugs": {
                    "active_accepted": 1,
                    "auto_accepted": 1,
                    "rejected": 0,
                    "open": 0,
                    "total_accepted": 2,
                    "reviewed": 1,
                },
                "test_environment": None,
            }
        ],
        "cache_stats": {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        result = await get_product_quality_report(
            product_id=598,
            ctx=mock_ctx,
        )

        # Verify test_environment is present but None (no errors)
        assert "by_test" in result
        assert len(result["by_test"]) == 1
        test_entry = result["by_test"][0]

        # Verify test_environment field is excluded when None (exclude_none=True behavior)
        # This is expected behavior - the Pydantic model serializes with exclude_none=True
        assert "test_environment" not in test_entry or test_entry["test_environment"] is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_report_handles_missing_test_environment_field() -> None:
    """Verify report handles missing test_environment field (backward compatibility)."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()

    # Mock service response without test_environment field (old service version)
    mock_service.get_product_quality_report.return_value = {
        "summary": {
            "total_tests": 1,
            "tests_by_status": {"locked": 1},
            "statuses_applied": "all",
            "total_bugs": 2,
            "bugs_by_status": {
                "active_accepted": 1,
                "auto_accepted": 1,
                "rejected": 0,
                "open": 0,
            },
            "total_accepted": 2,
            "reviewed": 1,
            "period": "all time",
        },
        "by_test": [
            {
                "test_id": 999,
                "title": "Legacy Test",
                "status": "locked",
                "bugs_count": 2,
                "bugs": {
                    "active_accepted": 1,
                    "auto_accepted": 1,
                    "rejected": 0,
                    "open": 0,
                    "total_accepted": 2,
                    "reviewed": 1,
                },
                # test_environment field is missing entirely
            }
        ],
        "cache_stats": {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        result = await get_product_quality_report(
            product_id=598,
            ctx=mock_ctx,
        )

        # Verify report generation succeeds (backward compatibility)
        assert "by_test" in result
        assert len(result["by_test"]) == 1
        test_entry = result["by_test"][0]

        # Verify test_environment is excluded when missing (exclude_none=True behavior)
        # This is expected behavior - the Pydantic model serializes with exclude_none=True
        assert "test_environment" not in test_entry or test_entry["test_environment"] is None


@pytest.mark.unit
def test_testbugmetrics_model_accepts_test_environment() -> None:
    """Verify TestBugMetrics Pydantic model accepts test_environment field (AC1)."""
    from testio_mcp.tools.product_quality_report_tool import BugCounts, TestBugMetrics

    # Create model instance with test_environment
    metrics = TestBugMetrics(
        test_id=123,
        title="Test with Environment",
        status="locked",
        start_at="2025-01-01T00:00:00Z",
        end_at="2025-01-31T23:59:59Z",
        bugs_count=5,
        bugs=BugCounts(
            active_accepted=3,
            auto_accepted=1,
            rejected=1,
            open=0,
            total_accepted=4,
            reviewed=4,
        ),
        test_environment={"id": 789, "title": "Staging"},
        active_acceptance_rate=0.6,
        overall_acceptance_rate=0.8,
    )

    # Verify field is accessible and properly typed
    assert metrics.test_environment == {"id": 789, "title": "Staging"}
    assert isinstance(metrics.test_environment, dict)


@pytest.mark.unit
def test_testbugmetrics_model_defaults_test_environment_to_none() -> None:
    """Verify TestBugMetrics model defaults test_environment to None (AC1)."""
    from testio_mcp.tools.product_quality_report_tool import BugCounts, TestBugMetrics

    # Create model instance without test_environment
    metrics = TestBugMetrics(
        test_id=456,
        title="Test without Environment",
        status="running",
        start_at=None,
        end_at=None,
        bugs_count=0,
        bugs=BugCounts(
            active_accepted=0,
            auto_accepted=0,
            rejected=0,
            open=0,
            total_accepted=0,
            reviewed=0,
        ),
    )

    # Verify field defaults to None
    assert metrics.test_environment is None

    # Verify model serialization works
    serialized = metrics.model_dump(exclude_none=True)
    assert "test_environment" not in serialized  # None values excluded
