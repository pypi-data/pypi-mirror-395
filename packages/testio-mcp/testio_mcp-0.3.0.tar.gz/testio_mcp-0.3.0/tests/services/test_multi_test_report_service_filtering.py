"""Unit tests for MultiTestReportService default filtering behavior (STORY-026).

Tests verify that:
1. statuses=None excludes initialized and cancelled by default
2. Explicit statuses list overrides default filtering
3. statuses_applied field is correctly included in response
"""

from unittest.mock import AsyncMock

import pytest

from testio_mcp.services.multi_test_report_service import MultiTestReportService


@pytest.mark.unit
@pytest.mark.asyncio
async def test_default_excludes_initialized_and_cancelled() -> None:
    """Verify statuses=None excludes initialized and cancelled by default."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    # Mock product info (exists)
    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}

    # Mock test query result (empty for this test, we're checking the query call)
    mock_test_repo.query_tests.return_value = []

    # Mock bug repository response
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

    # Create service
    service = MultiTestReportService(
        client=mock_client,
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Call with statuses=None
    result = await service.get_product_quality_report(
        product_id=123,
        statuses=None,  # Default filter
    )

    # Verify query_tests called with correct filter
    mock_test_repo.query_tests.assert_called_once()
    call_args = mock_test_repo.query_tests.call_args
    assert call_args.kwargs["product_id"] == 123
    assert call_args.kwargs["statuses"] == [
        "running",
        "locked",
        "archived",
        "customer_finalized",
    ]

    # Verify summary includes effective statuses
    assert result["summary"]["statuses_applied"] == [
        "running",
        "locked",
        "archived",
        "customer_finalized",
    ]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_explicit_statuses_override_default() -> None:
    """Verify explicit statuses list overrides default filtering."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    # Mock product info
    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}

    # Mock test query result
    mock_test_repo.query_tests.return_value = []

    # Mock bug repository response
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
        client=mock_client,
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Call with explicit statuses
    result = await service.get_product_quality_report(
        product_id=123,
        statuses=["initialized", "cancelled"],  # Explicit override
    )

    # Verify explicit statuses used (no default filter applied)
    call_args = mock_test_repo.query_tests.call_args
    assert call_args.kwargs["statuses"] == ["initialized", "cancelled"]

    # Verify statuses_applied reflects explicit choice
    assert result["summary"]["statuses_applied"] == ["initialized", "cancelled"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_with_mock_data_excludes_unexecuted() -> None:
    """Test with mock data: verify initialized/cancelled tests excluded from results."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    # Mock product info
    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}

    # Mock test query result (simulates repository filtering - only executed tests returned)
    mock_test_repo.query_tests.return_value = [
        {
            "id": 1,
            "title": "Test 1",
            "status": "locked",
            "start_at": "2024-01-01T00:00:00+00:00",
            "end_at": "2024-01-02T00:00:00+00:00",
        },
        {
            "id": 2,
            "title": "Test 2",
            "status": "archived",
            "start_at": "2024-01-03T00:00:00+00:00",
            "end_at": "2024-01-04T00:00:00+00:00",
        },
    ]

    # Mock bug repository response (no bugs for simplicity)
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {1: [], 2: []},  # No bugs
        {
            "total_tests": 2,
            "cache_hits": 2,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 2},
        },
    )

    service = MultiTestReportService(
        client=mock_client,
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Call with statuses=None (default filter)
    result = await service.get_product_quality_report(product_id=123, statuses=None)

    # Verify no initialized/cancelled tests in results
    statuses_in_results = result["summary"]["tests_by_status"].keys()
    assert "initialized" not in statuses_in_results
    assert "cancelled" not in statuses_in_results

    # Verify only executed tests counted
    assert result["summary"]["total_tests"] == 2
    assert result["summary"]["tests_by_status"] == {"locked": 1, "archived": 1}

    # Verify statuses_applied field
    assert result["summary"]["statuses_applied"] == [
        "running",
        "locked",
        "archived",
        "customer_finalized",
    ]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_all_statuses_when_explicit_empty_list() -> None:
    """Verify that passing an explicit empty list uses 'all' statuses."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    # Mock product info
    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}

    # Mock test query result
    mock_test_repo.query_tests.return_value = []

    # Mock bug repository response
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
        client=mock_client,
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Call with explicit empty list (edge case: should be treated as "no filter")
    result = await service.get_product_quality_report(
        product_id=123,
        statuses=[],  # Explicit empty list
    )

    # Verify empty list passed to repository (no filter, but explicit choice)
    call_args = mock_test_repo.query_tests.call_args
    assert call_args.kwargs["statuses"] == []

    # Verify statuses_applied shows "all" for empty list
    # Empty list is falsy, so effective_statuses or "all" returns "all"
    assert result["summary"]["statuses_applied"] == "all"
