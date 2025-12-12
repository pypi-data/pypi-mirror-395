"""Unit tests for get_product_quality_report MCP tool."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp.exceptions import ToolError

from testio_mcp.exceptions import ProductNotFoundException, TestIOAPIError
from testio_mcp.tools.product_quality_report_tool import (
    get_product_quality_report as get_product_quality_report_tool,
)
from tests.unit.test_utils import mock_service_context

get_product_quality_report = get_product_quality_report_tool.fn


def create_mock_summary(
    total_tests: int = 0,
    tests_by_status: dict[str, int] | None = None,
    statuses_applied: list[str] | str = "all",
    total_bugs: int = 0,
    active_accepted: int = 0,
    auto_accepted: int = 0,
    rejected: int = 0,
    open_bugs: int = 0,
    period: str = "all time",
) -> dict:
    """Helper to create mock EBR summary with all required fields (STORY-026)."""
    if tests_by_status is None:
        tests_by_status = {}

    total_accepted = active_accepted + auto_accepted
    reviewed = active_accepted + rejected  # Human-reviewed only (excludes auto_accepted)

    bugs_by_status = {
        "active_accepted": active_accepted,
        "auto_accepted": auto_accepted,
        "rejected": rejected,
        "open": open_bugs,
    }

    # Calculate rates using total_bugs as denominator (matches production)
    rates = None
    total_bugs_count = active_accepted + auto_accepted + rejected + open_bugs
    if total_bugs_count > 0:
        rates = {
            "active_acceptance_rate": active_accepted / total_bugs_count,
            "auto_acceptance_rate": auto_accepted / total_accepted if total_accepted > 0 else None,
            "overall_acceptance_rate": total_accepted / total_bugs_count,
            "rejection_rate": rejected / total_bugs_count,
        }

    # Calculate review rate (user reviewed / total_bugs)
    # Review rate = bugs reviewed by humans (active_accepted + rejected)
    # Excludes auto_accepted (system-reviewed) and open (not reviewed)
    user_reviewed = active_accepted + rejected
    review_rate = user_reviewed / total_bugs if total_bugs > 0 else None

    return {
        "total_tests": total_tests,
        "tests_by_status": tests_by_status,
        "statuses_applied": statuses_applied,  # STORY-026: Track what filter was used
        "total_bugs": total_bugs,
        "bugs_by_status": bugs_by_status,
        "active_accepted": active_accepted,
        "auto_accepted": auto_accepted,
        "rejected": rejected,
        "open": open_bugs,
        "total_accepted": total_accepted,
        "reviewed": reviewed,
        "active_acceptance_rate": rates["active_acceptance_rate"] if rates else None,
        "auto_acceptance_rate": rates["auto_acceptance_rate"] if rates else None,
        "overall_acceptance_rate": rates["overall_acceptance_rate"] if rates else None,
        "rejection_rate": rates["rejection_rate"] if rates else None,
        "review_rate": review_rate,
        "period": period,
    }


def create_mock_test(
    test_id: int,
    title: str,
    status: str = "locked",
    start_at: str | None = None,
    end_at: str | None = None,
    active_accepted: int = 0,
    auto_accepted: int = 0,
    rejected: int = 0,
    open_bugs: int = 0,
) -> dict:
    """Helper to create mock test metrics with all required fields."""
    total_accepted = active_accepted + auto_accepted
    reviewed = active_accepted + rejected  # Human-reviewed only (excludes auto_accepted)
    bugs_count = active_accepted + auto_accepted + rejected + open_bugs

    # Calculate rates using total_bugs as denominator (matches production)
    rates = None
    total_bugs_count = active_accepted + auto_accepted + rejected + open_bugs
    if total_bugs_count > 0:
        rates = {
            "active_acceptance_rate": active_accepted / total_bugs_count,
            "auto_acceptance_rate": auto_accepted / total_accepted if total_accepted > 0 else None,
            "overall_acceptance_rate": total_accepted / total_bugs_count,
            "rejection_rate": rejected / total_bugs_count,
        }

    # Calculate review rate (user reviewed / total_bugs)
    # Review rate = bugs reviewed by humans (active_accepted + rejected)
    # Excludes auto_accepted (system-reviewed) and open (not reviewed)
    user_reviewed = active_accepted + rejected
    review_rate = user_reviewed / bugs_count if bugs_count > 0 else None

    return {
        "test_id": test_id,
        "title": title,
        "status": status,
        "start_at": start_at,
        "end_at": end_at,
        "bugs_count": bugs_count,
        "bugs": {
            "active_accepted": active_accepted,
            "auto_accepted": auto_accepted,
            "rejected": rejected,
            "open": open_bugs,
            "total_accepted": total_accepted,
            "reviewed": reviewed,
        },
        "active_acceptance_rate": rates["active_acceptance_rate"] if rates else None,
        "auto_acceptance_rate": rates["auto_acceptance_rate"] if rates else None,
        "overall_acceptance_rate": rates["overall_acceptance_rate"] if rates else None,
        "rejection_rate": rates["rejection_rate"] if rates else None,
        "review_rate": review_rate,
    }


@pytest.mark.unit
@pytest.mark.asyncio
async def test_transforms_product_not_found_to_tool_error() -> None:
    """Verify ProductNotFoundException → ToolError."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.side_effect = ProductNotFoundException(product_id=999)

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        with pytest.raises(ToolError) as exc_info:
            await get_product_quality_report(product_id=999, ctx=mock_ctx)

        error_msg = str(exc_info.value)
        assert "❌" in error_msg
        assert "not found" in error_msg.lower()
        assert "ℹ️" in error_msg
        assert "💡" in error_msg


@pytest.mark.unit
@pytest.mark.asyncio
async def test_transforms_api_error_to_tool_error() -> None:
    """Verify TestIOAPIError → ToolError."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.side_effect = TestIOAPIError(
        message="Server error", status_code=503
    )

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        with pytest.raises(ToolError) as exc_info:
            await get_product_quality_report(product_id=123, ctx=mock_ctx)

        error_msg = str(exc_info.value)
        assert "❌" in error_msg
        assert "503" in error_msg


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delegates_with_minimal_parameters() -> None:
    """Verify tool delegates with only product_id (no filters)."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.return_value = {
        "summary": create_mock_summary(),
        "by_test": [],
        "cache_stats": {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        await get_product_quality_report(product_id=598, ctx=mock_ctx)

        call_args = mock_service.get_product_quality_report.call_args
        assert call_args.kwargs["product_id"] == 598
        assert call_args.kwargs["start_date"] is None
        assert call_args.kwargs["end_date"] is None
        assert call_args.kwargs["statuses"] is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delegates_with_date_filters() -> None:
    """Verify tool passes date filters to service."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.return_value = {
        "summary": create_mock_summary(period="2024-01-01 to 2024-12-31"),
        "by_test": [],
        "cache_stats": {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        await get_product_quality_report(
            product_id=598,
            start_date="2024-01-01",
            end_date="2024-12-31",
            ctx=mock_ctx,
        )

        call_args = mock_service.get_product_quality_report.call_args
        assert call_args.kwargs["start_date"] == "2024-01-01"
        assert call_args.kwargs["end_date"] == "2024-12-31"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delegates_with_status_filter() -> None:
    """Verify tool passes status filter to service."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.return_value = {
        "summary": create_mock_summary(),
        "by_test": [],
        "cache_stats": {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        await get_product_quality_report(product_id=598, statuses=["locked"], ctx=mock_ctx)

        call_args = mock_service.get_product_quality_report.call_args
        assert call_args.kwargs["statuses"] == ["locked"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_parses_comma_separated_statuses() -> None:
    """Verify tool parses comma-separated status string."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.return_value = {
        "summary": create_mock_summary(),
        "by_test": [],
        "cache_stats": {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    }

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        # Pass comma-separated string
        await get_product_quality_report(product_id=598, statuses="locked,running", ctx=mock_ctx)

        call_args = mock_service.get_product_quality_report.call_args
        # Verify parsed to list
        assert call_args.kwargs["statuses"] == ["locked", "running"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_returns_formatted_output() -> None:
    """Verify tool formats service result to Pydantic output."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.return_value = {
        "summary": create_mock_summary(
            total_tests=2,
            tests_by_status={"locked": 2},
            total_bugs=15,
            active_accepted=12,
            auto_accepted=3,
            rejected=0,
            open_bugs=0,
            period="2024-01-01 to 2024-12-31",
        ),
        "by_test": [
            create_mock_test(
                test_id=123,
                title="Test 1",
                status="locked",
                start_at="2024-01-01T00:00:00+00:00",
                end_at="2024-01-31T23:59:59+00:00",
                active_accepted=10,
                auto_accepted=2,
                rejected=0,
                open_bugs=0,
            )
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
        result = await get_product_quality_report(product_id=598, ctx=mock_ctx)

        # Verify output structure
        assert "summary" in result
        assert "by_test" in result
        assert "cache_stats" in result

        # Verify summary fields
        assert result["summary"]["total_tests"] == 2
        assert result["summary"]["tests_by_status"] == {"locked": 2}
        assert result["summary"]["total_bugs"] == 15
        assert result["summary"]["bugs_by_status"]["active_accepted"] == 12
        assert result["summary"]["overall_acceptance_rate"] == 1.0

        # Verify by_test fields
        assert len(result["by_test"]) == 1
        assert result["by_test"][0]["test_id"] == 123
        assert result["by_test"][0]["status"] == "locked"
        assert result["by_test"][0]["bugs_count"] == 12
        assert result["by_test"][0]["bugs"]["active_accepted"] == 10
        # Review rate = (10 active + 0 rejected) / 12 total = 0.8333
        # 2 bugs auto-accepted (not user-reviewed)
        assert abs(result["by_test"][0]["review_rate"] - 0.8333333333333334) < 0.0001

        # Verify cache_stats fields
        assert result["cache_stats"]["total_tests"] == 2
        assert result["cache_stats"]["cache_hits"] == 2
        assert result["cache_stats"]["api_calls"] == 0
        assert result["cache_stats"]["cache_hit_rate"] == 100.0
        assert result["cache_stats"]["breakdown"] == {"immutable_cached": 2}


@pytest.mark.unit
@pytest.mark.asyncio
async def test_handles_none_acceptance_rates() -> None:
    """Verify tool handles None acceptance rates (no bugs to calculate rates from)."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.return_value = {
        "summary": create_mock_summary(
            total_tests=1,
            tests_by_status={"locked": 1},
            total_bugs=5,
            active_accepted=0,
            auto_accepted=0,
            rejected=0,
            open_bugs=5,  # All bugs are open
            period="all time",
        ),
        "by_test": [
            create_mock_test(
                test_id=123,
                title="Test 1",
                status="locked",
                active_accepted=0,
                auto_accepted=0,
                rejected=0,
                open_bugs=5,
            )
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
        result = await get_product_quality_report(product_id=598, ctx=mock_ctx)

        # Verify rates are 0.0 when all bugs are open (no accepted/rejected)
        assert result["summary"]["overall_acceptance_rate"] == 0.0
        assert result["by_test"][0]["overall_acceptance_rate"] == 0.0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_reraises_tool_error_from_date_parsing() -> None:
    """Verify ToolError from parse_flexible_date is re-raised."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    mock_service.get_product_quality_report.side_effect = ToolError(
        "❌ Could not parse date: 'invalid_date'\n"
        "ℹ️ Supported formats: ...\n"
        "💡 Use ISO format (YYYY-MM-DD)"
    )

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        with pytest.raises(ToolError) as exc_info:
            await get_product_quality_report(
                product_id=598, start_date="invalid_date", ctx=mock_ctx
            )

        # Verify original ToolError is re-raised
        assert "Could not parse date" in str(exc_info.value)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_transforms_unexpected_error_to_tool_error() -> None:
    """Verify unexpected exceptions → ToolError."""
    mock_ctx = MagicMock()
    mock_service = AsyncMock()
    # Use RuntimeError instead of ValueError (ValueError is re-raised for date parsing)
    mock_service.get_product_quality_report.side_effect = RuntimeError("Unexpected error")

    with patch(
        "testio_mcp.tools.product_quality_report_tool.get_service_context",
        return_value=mock_service_context(mock_service),
    ):
        with pytest.raises(ToolError) as exc_info:
            await get_product_quality_report(product_id=598, ctx=mock_ctx)

        error_msg = str(exc_info.value)
        assert "❌" in error_msg
        assert "Unexpected error" in error_msg
