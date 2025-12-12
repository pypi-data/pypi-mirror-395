"""Unit tests for MultiTestReportService."""

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from testio_mcp.exceptions import ProductNotFoundException
from testio_mcp.services.multi_test_report_service import MultiTestReportService


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_aggregates_bugs() -> None:
    """Verify EBR aggregates bugs across multiple tests."""
    # Mock repositories
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = [
        {"id": 123, "title": "Test 1"},
        {"id": 124, "title": "Test 2"},
    ]

    mock_bug_repo = AsyncMock()
    # STORY-024: Service now uses get_bugs_cached_or_refresh
    # STORY-047: Use enriched status values
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {
            123: [{"status": "accepted"}],  # Active accepted (enriched)
            124: [{"status": "rejected"}],
        },
        {
            "total_tests": 2,
            "cache_hits": 2,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 2},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    result = await service.get_product_quality_report(product_id=598)

    # Verify summary aggregation
    assert result["summary"]["total_tests"] == 2
    assert result["summary"]["total_bugs"] == 2
    assert result["summary"]["bugs_by_status"]["active_accepted"] == 1
    assert result["summary"]["bugs_by_status"]["rejected"] == 1
    assert result["summary"]["reviewed"] == 2
    assert result["summary"]["overall_acceptance_rate"] == 0.5  # 1/2

    # Verify per-test metrics
    assert len(result["by_test"]) == 2
    assert result["by_test"][0]["test_id"] == 123
    assert result["by_test"][0]["bugs"]["active_accepted"] == 1
    assert result["by_test"][1]["test_id"] == 124
    assert result["by_test"][1]["bugs"]["rejected"] == 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_filters_by_date() -> None:
    """Verify date filtering works with flexible formats."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = []

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {},
        {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Use parse_flexible_date internally (via service)
    await service.get_product_quality_report(
        product_id=598,
        start_date="last 30 days",
        end_date="today",
    )

    # Verify TestRepository was called with parsed dates
    call_args = mock_test_repo.query_tests.call_args
    assert call_args.kwargs["start_date"] is not None
    assert call_args.kwargs["end_date"] is not None
    assert isinstance(call_args.kwargs["start_date"], datetime)
    assert isinstance(call_args.kwargs["end_date"], datetime)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_filters_by_status() -> None:
    """Verify status filtering is passed to repository."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = []

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {},
        {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    await service.get_product_quality_report(
        product_id=598,
        statuses=["locked", "running"],
    )

    # Verify statuses passed to repository
    call_args = mock_test_repo.query_tests.call_args
    assert call_args.kwargs["statuses"] == ["locked", "running"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_handles_no_tests() -> None:
    """Verify EBR handles empty test list gracefully."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = []

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {},
        {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    result = await service.get_product_quality_report(product_id=598)

    # Verify empty summary
    assert result["summary"]["total_tests"] == 0
    assert result["summary"]["total_bugs"] == 0
    assert result["summary"]["reviewed"] == 0
    assert result["summary"]["overall_acceptance_rate"] is None
    assert result["by_test"] == []


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_handles_test_with_no_bugs() -> None:
    """Verify EBR handles test with no bugs (acceptance rate should be None)."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = [
        {"id": 123, "title": "Test 1"},
    ]

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {123: []},  # No bugs for test 123
        {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    result = await service.get_product_quality_report(product_id=598)

    # Verify summary
    assert result["summary"]["total_tests"] == 1
    assert result["summary"]["total_bugs"] == 0

    # STORY-081: All rate fields should be None (not 0.0) when no bugs exist
    assert result["summary"]["active_acceptance_rate"] is None
    assert result["summary"]["auto_acceptance_rate"] is None
    assert result["summary"]["overall_acceptance_rate"] is None
    assert result["summary"]["rejection_rate"] is None
    assert result["summary"]["review_rate"] is None

    # Verify per-test metrics
    assert result["by_test"][0]["bugs"]["reviewed"] == 0

    # STORY-081: All rate fields should be None (not 0.0) when test has no bugs
    assert result["by_test"][0]["active_acceptance_rate"] is None
    assert result["by_test"][0]["auto_acceptance_rate"] is None
    assert result["by_test"][0]["overall_acceptance_rate"] is None
    assert result["by_test"][0]["rejection_rate"] is None
    assert result["by_test"][0]["review_rate"] is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_calculates_acceptance_rates() -> None:
    """Verify acceptance rate calculations match shared utilities."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = [
        {"id": 123, "title": "Test 1"},
    ]

    # 12 active accepted, 3 auto accepted, 3 rejected
    # STORY-047: Use enriched status values (auto_accepted as status)
    bugs = (
        [{"status": "accepted"}] * 12  # Active accepted
        + [{"status": "auto_accepted"}] * 3  # Auto accepted (enriched status)
        + [{"status": "rejected"}] * 3
    )

    mock_bug_repo = AsyncMock()
    # STORY-024: Service now uses get_bugs_cached_or_refresh
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {123: bugs},
        {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    result = await service.get_product_quality_report(product_id=598)

    # Verify counts
    assert result["by_test"][0]["bugs"]["active_accepted"] == 12
    assert result["by_test"][0]["bugs"]["auto_accepted"] == 3
    assert result["by_test"][0]["bugs"]["rejected"] == 3
    assert result["by_test"][0]["bugs"]["reviewed"] == 15  # active + rejected (excludes auto)

    # Verify rates with new formulas
    # total_bugs = 18, total_accepted = 15
    assert abs(result["by_test"][0]["active_acceptance_rate"] - (12 / 18)) < 0.001  # 0.667
    assert abs(result["by_test"][0]["auto_acceptance_rate"] - (3 / 15)) < 0.001  # 0.2
    assert abs(result["by_test"][0]["overall_acceptance_rate"] - (15 / 18)) < 0.001  # 0.833
    assert abs(result["by_test"][0]["rejection_rate"] - (3 / 18)) < 0.001  # 0.167


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_handles_open_bugs() -> None:
    """Verify open (forwarded) bugs are excluded from reviewed count."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = [
        {"id": 123, "title": "Test 1"},
    ]

    # 5 accepted, 5 open (should not affect acceptance rate)
    # STORY-047: Use enriched status values
    bugs = [{"status": "accepted"}] * 5 + [{"status": "forwarded"}] * 5

    mock_bug_repo = AsyncMock()
    # STORY-024: Service now uses get_bugs_cached_or_refresh
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {123: bugs},
        {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    result = await service.get_product_quality_report(product_id=598)

    # Verify counts
    assert result["by_test"][0]["bugs"]["active_accepted"] == 5
    assert result["by_test"][0]["bugs"]["open"] == 5
    assert result["by_test"][0]["bugs"]["reviewed"] == 5  # Only active_accepted (human-reviewed)
    assert result["by_test"][0]["overall_acceptance_rate"] == 0.5  # 5/10 (total_bugs)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_raises_product_not_found() -> None:
    """Verify ProductNotFoundException is raised for missing product."""
    mock_test_repo = AsyncMock()

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {},
        {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    )

    mock_product_repo = AsyncMock()
    mock_product_repo.get_product_info.return_value = None  # Product not found (STORY-032A)

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=mock_product_repo,
    )

    with pytest.raises(ProductNotFoundException) as exc_info:
        await service.get_product_quality_report(product_id=999)

    assert exc_info.value.product_id == 999


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_formats_period_string() -> None:
    """Verify period string formatting for various date combinations."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = []

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {},
        {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Test all combinations
    result = await service.get_product_quality_report(product_id=598)
    assert result["summary"]["period"] == "all time"

    result = await service.get_product_quality_report(product_id=598, start_date="2024-01-01")
    assert result["summary"]["period"] == "2024-01-01 to present"

    result = await service.get_product_quality_report(product_id=598, end_date="2024-12-31")
    assert result["summary"]["period"] == "through 2024-12-31"

    result = await service.get_product_quality_report(
        product_id=598, start_date="2024-01-01", end_date="2024-12-31"
    )
    assert result["summary"]["period"] == "2024-01-01 to 2024-12-31"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_uses_shared_utilities() -> None:
    """Verify EBR uses shared utilities from STORY-023b."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = [
        {"id": 123, "title": "Test 1"},
    ]

    # STORY-047: Use enriched status values
    bugs = [{"status": "accepted"}] * 10

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {123: bugs},
        {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Patch utilities to verify they're called
    with patch("testio_mcp.services.multi_test_report_service.classify_bugs") as mock_classify:
        with patch(
            "testio_mcp.services.multi_test_report_service.calculate_acceptance_rates"
        ) as mock_calc_rates:
            # Set up mock return values
            mock_classify.return_value = {
                "active_accepted": 10,
                "auto_accepted": 0,
                "rejected": 0,
                "open": 0,
                "total_accepted": 10,
                "reviewed": 10,
            }
            mock_calc_rates.return_value = {
                "active_acceptance_rate": 1.0,
                "auto_acceptance_rate": 0.0,
                "overall_acceptance_rate": 1.0,
                "rejection_rate": 0.0,
                "review_rate": 1.0,  # Now included in shared utility
            }

            await service.get_product_quality_report(product_id=598)

            # Verify utilities were called
            assert mock_classify.call_count >= 1
            assert mock_calc_rates.call_count >= 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_parses_iso_date() -> None:
    """Verify ISO 8601 date parsing works correctly."""
    mock_test_repo = AsyncMock()
    mock_test_repo.get_product_info.return_value = {
        "id": 598,
        "name": "Test Product",
        "type": "web",
    }
    mock_test_repo.query_tests.return_value = []

    mock_bug_repo = AsyncMock()
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {},
        {
            "total_tests": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "cache_hit_rate": 0.0,
            "breakdown": {},
        },
    )

    service = MultiTestReportService(
        client=AsyncMock(),
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    await service.get_product_quality_report(
        product_id=598,
        start_date="2024-01-01",
        end_date="2024-12-31",
    )

    # Verify dates were parsed
    call_args = mock_test_repo.query_tests.call_args
    start_dt = call_args.kwargs["start_date"]
    end_dt = call_args.kwargs["end_date"]

    assert start_dt.year == 2024
    assert start_dt.month == 1
    assert start_dt.day == 1
    assert start_dt.hour == 0  # Start of day

    assert end_dt.year == 2024
    assert end_dt.month == 12
    assert end_dt.day == 31
    assert end_dt.hour == 23  # End of day


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_quality_report_enhancements() -> None:
    """Verify enhancements: bugs_by_severity, tests_by_type, avg_bugs_per_test."""
    # Setup mocks
    client = AsyncMock()
    test_repo = AsyncMock()
    bug_repo = AsyncMock()
    product_repo = AsyncMock()

    service = MultiTestReportService(client, test_repo, bug_repo, product_repo)

    # Mock product info
    product_repo.get_product_info.return_value = {"id": 1, "title": "Test Product"}

    # Mock tests
    # Test 1: Rapid, 2 bugs (Critical, Low)
    # Test 2: Focused, 1 bug (High)
    # Test 3: Rapid, 0 bugs
    tests = [
        {
            "id": 101,
            "title": "Test 1",
            "status": "locked",
            "testing_type": "rapid",
            "start_at": datetime.now(),
        },
        {
            "id": 102,
            "title": "Test 2",
            "status": "locked",
            "testing_type": "focused",
            "start_at": datetime.now(),
        },
        {
            "id": 103,
            "title": "Test 3",
            "status": "locked",
            "testing_type": "rapid",
            "start_at": datetime.now(),
        },
    ]
    test_repo.query_tests.return_value = tests

    # Mock bugs
    bugs_map = {
        101: [
            {"id": 1, "severity": "critical", "status": "accepted", "known": False},
            {"id": 2, "severity": "low", "status": "rejected", "known": False},
        ],
        102: [
            {"id": 3, "severity": "high", "status": "accepted", "known": False},
        ],
        103: [],
    }
    bug_repo.get_bugs_cached_or_refresh.return_value = (bugs_map, {"cache_hit_rate": 100})

    # Execute
    report = await service.get_product_quality_report(product_id=1)
    summary = report["summary"]

    # Verify Tests by Type
    assert summary["tests_by_type"] == {"rapid": 2, "focused": 1}

    # Verify Bugs by Severity
    # Total bugs = 3 (Critical, Low, High)
    assert summary["bugs_by_severity"] == {"critical": 1, "low": 1, "high": 1}

    # Verify Avg Bugs per Test
    # Total bugs = 3, Total tests = 3 -> Avg = 1.0
    assert summary["avg_bugs_per_test"] == 1.0

    # Verify Total Bugs
    assert summary["total_bugs"] == 3
