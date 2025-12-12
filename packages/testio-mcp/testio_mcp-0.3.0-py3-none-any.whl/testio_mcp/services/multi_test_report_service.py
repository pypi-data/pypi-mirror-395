"""Multi-test reporting service for Executive Bug Report (EBR) generation.

This service aggregates bug metrics across multiple tests for a product,
providing comprehensive quality reporting capabilities.

STORY-023e: Implements EBR functionality on SQLite-first architecture
Uses shared utilities from STORY-023b (bug_classifiers, date_utils)
Uses repository pattern from STORY-023c

Responsibilities:
- Multi-test bug aggregation
- Flexible date filtering (ISO 8601, business terms, natural language)
- Acceptance rate calculations
- Test status filtering
- Period summarization

Does NOT handle:
- MCP protocol formatting
- User-facing error messages
- HTTP transport concerns
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from testio_mcp.client import TestIOClient
from testio_mcp.exceptions import ProductNotFoundException
from testio_mcp.repositories.bug_repository import BugRepository
from testio_mcp.repositories.test_repository import TestRepository
from testio_mcp.schemas.constants import EXECUTED_TEST_STATUSES
from testio_mcp.services.base_service import BaseService
from testio_mcp.utilities.bug_classifiers import (
    calculate_acceptance_rates,
    classify_bugs,
)
from testio_mcp.utilities.date_utils import parse_flexible_date
from testio_mcp.utilities.file_export import (
    get_file_format,
    resolve_output_path,
    write_report_to_file,
)

if TYPE_CHECKING:
    from testio_mcp.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


class MultiTestReportService(BaseService):
    """Service for multi-test reporting and aggregation.

    Generates Executive Bug Reports (EBR) that aggregate metrics across
    multiple tests for a product or initiative.

    Example:
        ```python
        service = MultiTestReportService(
            client=client,
            test_repo=test_repo,
            bug_repo=bug_repo
        )
        report = await service.generate_ebr_report(
            product_id=598,
            start_date="2024-01-01",
            end_date="2024-12-31",
            statuses=["locked"]
        )
        ```
    """

    def __init__(
        self,
        client: TestIOClient,
        test_repo: TestRepository,
        bug_repo: BugRepository,
        product_repo: "ProductRepository",
    ) -> None:
        """Initialize service with API client and repositories.

        Args:
            client: TestIO API client for making HTTP requests
            test_repo: Repository for test data access
            bug_repo: Repository for bug data access
            product_repo: Repository for product data access
        """
        super().__init__(client)
        self.test_repo = test_repo
        self.bug_repo = bug_repo
        self.product_repo = product_repo

    async def get_product_quality_report(
        self,
        product_id: int,
        start_date: str | None = None,
        end_date: str | None = None,
        statuses: list[str] | None = None,
        output_file: str | None = None,
    ) -> dict[str, Any]:
        """Generate Executive Bug Report for a product.

        Aggregates bug metrics across multiple tests with flexible filtering.
        Uses intelligent bug caching (STORY-024): immutable tests (archived/cancelled)
        are always served from cache, mutable tests refresh if stale (>1 hour).

        Args:
            product_id: Product to report on
            start_date: Start date (ISO 8601, relative, or natural language)
                       Examples: "2024-01-01", "last 30 days", "this quarter"
            end_date: End date (ISO 8601, relative, or natural language)
                     Examples: "2024-12-31", "today", "yesterday"
            statuses: Filter tests by status. If None, excludes ["initialized", "cancelled"]
                     by default (only executed tests). Pass explicit list to override.
            output_file: Optional path to export full report as file (STORY-025).
                        If specified, returns file metadata instead of full data.
                        If None, returns full JSON response (may truncate for large products).

        Returns:
            When output_file is None:
                Dictionary with structure:
                    {
                        "summary": {...},
                        "by_test": [...],
                        "cache_stats": {...}
                    }

            When output_file is specified:
                Dictionary with structure:
                    {
                        "file_path": str,  # Absolute path to written file
                        "summary": {...},  # Summary metrics only
                        "record_count": int,  # Number of tests in report
                        "file_size_bytes": int,  # File size
                        "format": "json"  # File format
                    }

        Raises:
            ProductNotFoundException: If product doesn't exist
            ToolError: If date parsing fails (from parse_flexible_date)
            ValueError: If output_file path is invalid or extension unsupported
            PermissionError: If file cannot be written (permissions)
            OSError: If disk is full or other I/O error occurs

        Performance:
            - With cache (typical): ~12 seconds for 295 tests
            - With force_refresh: ~30-45 seconds (same as before)

        Example:
            >>> # For fresh data, call sync_data first
            >>> await sync_service.sync_data(product_ids=[598])
            >>> # Then generate report (uses fresh cache)
            >>> report = await service.generate_ebr_report(
            ...     product_id=598,
            ...     start_date="last 30 days",
            ...     statuses=["locked"]
            ... )
            >>> report["summary"]["total_tests"]
            15
            >>> # Export to file (large product)
            >>> metadata = await service.generate_ebr_report(
            ...     product_id=598,
            ...     output_file="canva-q3-2025.json"
            ... )
            >>> metadata["file_path"]
            "/Users/username/.testio-mcp/reports/canva-q3-2025.json"
        """
        # Verify product exists (use repository to check) (STORY-032A)
        product_info = await self.product_repo.get_product_info(product_id)
        if not product_info:
            raise ProductNotFoundException(product_id)

        # Apply default filter if statuses not specified (STORY-026)
        # Default: exclude unexecuted tests (initialized, cancelled)
        # Rationale: Quality metrics should reflect only executed tests
        effective_statuses = statuses
        if statuses is None:
            # Exclude initialized (not reviewed/executed) and cancelled (never executed)
            effective_statuses = EXECUTED_TEST_STATUSES

        # Parse date filters (flexible formats)
        parsed_start_date: datetime | None = None
        parsed_end_date: datetime | None = None

        if start_date:
            # parse_flexible_date returns ISO string, convert to datetime
            start_iso = parse_flexible_date(start_date, start_of_day=True)
            parsed_start_date = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))

        if end_date:
            # parse_flexible_date returns ISO string, convert to datetime
            end_iso = parse_flexible_date(end_date, start_of_day=False)
            parsed_end_date = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))

        # Query tests from repository (filtered by date + status)
        tests = await self.test_repo.query_tests(
            product_id=product_id,
            statuses=effective_statuses,  # Use effective statuses (default or explicit)
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            date_field="start_at",  # Filter by test start date
            page=1,
            per_page=1000,  # EBR typically covers all tests in period
        )

        logger.debug(
            f"Generating EBR for product {product_id}: "
            f"{len(tests)} tests found with filters: "
            f"start_date={start_date}, end_date={end_date}, statuses={statuses}"
        )

        # Initialize aggregation counters
        summary_counts = {
            "active_accepted": 0,
            "auto_accepted": 0,
            "rejected": 0,
            "open": 0,
            "total_bugs": 0,  # Track total bugs (not derived from statuses)
        }
        tests_by_status: dict[str, int] = {}  # Count tests by status
        tests_by_type: dict[str, int] = {}  # Count tests by testing_type (STORY-084)
        bugs_by_severity: dict[str, int] = {}  # Count bugs by severity (STORY-084)
        by_test_results = []

        # Extract valid test IDs and build lookup map
        test_id_map = {}  # Map test_id -> test dict for later lookup
        for test in tests:
            test_id = test.get("id")
            if test_id is None:
                logger.warning(f"Test missing ID, skipping: {test.get('title', 'Untitled')}")
                continue
            test_id_map[test_id] = test

        valid_test_ids = list(test_id_map.keys())

        # Batch-aware intelligent caching (STORY-024)
        # One call handles all cache decisions + batched refreshes
        # Immutable tests (80%): SQLite cache (~2.4s for 236 tests)
        # Mutable tests (20%): API refresh (~10s for 59 tests)
        # Total: ~12s vs ~45s before (4x faster)
        bugs_by_test, cache_stats = await self.bug_repo.get_bugs_cached_or_refresh(
            test_ids=valid_test_ids,
            force_refresh=False,  # Always use cache (call sync_data for fresh data)
        )

        logger.debug(f"Fetched bugs for {len(valid_test_ids)} tests using intelligent caching")

        # Aggregate bugs across all tests
        for test_id, test in test_id_map.items():
            test_title = test.get("title", "Untitled")
            test_status = test.get("status", "unknown")
            test_start_at = test.get("start_at")
            test_end_at = test.get("end_at")

            # Track test status counts for summary
            tests_by_status[test_status] = tests_by_status.get(test_status, 0) + 1

            # Track testing type counts (STORY-084)
            testing_type = test.get("testing_type") or "unknown"
            tests_by_type[testing_type] = tests_by_type.get(testing_type, 0) + 1

            # Get bugs from cached/refreshed batch result
            bugs = bugs_by_test[test_id]

            # Aggregate bug severity (STORY-084)
            for bug in bugs:
                severity = bug.get("severity") or "unknown"
                bugs_by_severity[severity] = bugs_by_severity.get(severity, 0) + 1

            # Classify bugs using shared utility (STORY-023b)
            bug_counts = classify_bugs(bugs)

            # Total bugs count from actual bug list (not derived from statuses)
            # This ensures correctness if TestIO adds new bug statuses
            bugs_count = len(bugs)

            # Calculate acceptance rates for this test
            # review_rate is now included in shared utility (no duplication!)
            # Pass explicit bugs_count for future-proofing (handles new bug statuses)
            rates = calculate_acceptance_rates(
                active_accepted=bug_counts["active_accepted"],
                auto_accepted=bug_counts["auto_accepted"],
                rejected=bug_counts["rejected"],
                open_bugs=bug_counts["open"],
                total_bugs=bugs_count,  # Use len(bugs), not derived from statuses
            )

            # Build per-test result
            test_result: dict[str, Any] = {
                "test_id": test_id,
                "title": test_title,
                "status": test_status,
                "start_at": test_start_at,
                "end_at": test_end_at,
                "bugs_count": bugs_count,
                "bugs": {
                    "active_accepted": bug_counts["active_accepted"],
                    "auto_accepted": bug_counts["auto_accepted"],
                    "rejected": bug_counts["rejected"],
                    "open": bug_counts["open"],
                    "total_accepted": bug_counts["total_accepted"],
                    "reviewed": bug_counts["reviewed"],
                },
                "test_environment": test.get("test_environment"),
            }

            # Add acceptance rates (may be None if no bugs)
            self._apply_acceptance_rates(test_result, rates)

            by_test_results.append(test_result)

            # Aggregate to summary totals
            summary_counts["active_accepted"] += bug_counts["active_accepted"]
            summary_counts["auto_accepted"] += bug_counts["auto_accepted"]
            summary_counts["rejected"] += bug_counts["rejected"]
            summary_counts["open"] += bug_counts["open"]
            summary_counts["total_bugs"] += bugs_count  # Aggregate actual bug count

        # Calculate summary acceptance rates
        # Pass explicit aggregated total_bugs for future-proofing
        summary_rates = calculate_acceptance_rates(
            active_accepted=summary_counts["active_accepted"],
            auto_accepted=summary_counts["auto_accepted"],
            rejected=summary_counts["rejected"],
            open_bugs=summary_counts["open"],
            total_bugs=summary_counts["total_bugs"],  # Use aggregated total, not derived
        )

        # Build period string for display
        period_str = self._format_period_string(start_date, end_date)

        # Build summary section
        total_accepted = summary_counts["active_accepted"] + summary_counts["auto_accepted"]
        total_bugs = summary_counts["total_bugs"]  # Use aggregated total (not derived)
        # Reviewed = human-reviewed bugs only (excludes auto_accepted)
        reviewed = summary_counts["active_accepted"] + summary_counts["rejected"]

        # Build bugs_by_status dict for consistent structure
        bugs_by_status = {
            "active_accepted": summary_counts["active_accepted"],
            "auto_accepted": summary_counts["auto_accepted"],
            "rejected": summary_counts["rejected"],
            "open": summary_counts["open"],
        }

        # Calculate average bugs per test (STORY-084)
        avg_bugs_per_test = 0.0
        if len(tests) > 0:
            avg_bugs_per_test = round(total_bugs / len(tests), 2)

        summary: dict[str, Any] = {
            "total_tests": len(tests),
            "tests_by_status": tests_by_status,
            "statuses_applied": effective_statuses or "all",  # Show what filter was used
            "total_bugs": total_bugs,
            "bugs_by_status": bugs_by_status,
            "bugs_by_severity": bugs_by_severity,  # New metric (STORY-084)
            "tests_by_type": tests_by_type,  # New metric (STORY-084)
            "total_accepted": total_accepted,
            "reviewed": reviewed,
            "avg_bugs_per_test": avg_bugs_per_test,  # New metric (STORY-084)
            "period": period_str,
        }

        # Add summary acceptance rates (review_rate now from shared utility!)
        self._apply_acceptance_rates(summary, summary_rates)

        logger.info(
            f"EBR generated for product {product_id}: "
            f"{len(tests)} tests, {total_bugs} bugs, "
            f"acceptance_rate={summary.get('overall_acceptance_rate')}"
        )

        # If output_file is specified, write to file and return metadata
        if output_file is not None:
            # Resolve and validate output path
            output_path = resolve_output_path(output_file)

            # Build full report dict for file export
            full_report = {
                "summary": summary,
                "by_test": by_test_results,
                "cache_stats": cache_stats,
            }

            # Write report to file
            file_size_bytes = write_report_to_file(full_report, output_path)

            # Get file format
            file_format = get_file_format(output_path)

            # Return file metadata (not full data)
            return {
                "file_path": str(output_path),
                "summary": summary,  # Summary metrics only (without by_test array)
                "record_count": len(tests),
                "file_size_bytes": file_size_bytes,
                "format": file_format,
            }

        # Otherwise, return full report dict
        return {
            "summary": summary,
            "by_test": by_test_results,
            "cache_stats": cache_stats,
        }

    def _apply_acceptance_rates(
        self, target: dict[str, Any], rates: dict[str, float | None]
    ) -> None:
        """Apply acceptance rates to target dict.

        This helper eliminates duplication of the rate assignment pattern that
        appears twice in generate_ebr_report (per-test and summary).

        After STORY-081, calculate_acceptance_rates() always returns a dict
        (never None). Individual rate values may be None when total_bugs == 0.

        Args:
            target: Dictionary to update with rate fields
            rates: Rate dictionary from calculate_acceptance_rates()
                  (individual rates may be None if no bugs)
        """
        target["active_acceptance_rate"] = rates["active_acceptance_rate"]
        target["auto_acceptance_rate"] = rates["auto_acceptance_rate"]
        target["overall_acceptance_rate"] = rates["overall_acceptance_rate"]
        target["rejection_rate"] = rates["rejection_rate"]
        target["review_rate"] = rates["review_rate"]

    def _format_period_string(self, start_date: str | None, end_date: str | None) -> str:
        """Format period string for display in EBR summary.

        Args:
            start_date: Start date string (original input)
            end_date: End date string (original input)

        Returns:
            Human-readable period string

        Examples:
            >>> _format_period_string("2024-01-01", "2024-12-31")
            "2024-01-01 to 2024-12-31"
            >>> _format_period_string("last 30 days", None)
            "last 30 days to present"
            >>> _format_period_string(None, None)
            "all time"
        """
        if not start_date and not end_date:
            return "all time"
        elif start_date and not end_date:
            return f"{start_date} to present"
        elif not start_date and end_date:
            return f"through {end_date}"
        else:
            return f"{start_date} to {end_date}"
