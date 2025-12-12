"""MCP tool for generating Product Quality Reports.

This module implements the get_product_quality_report tool following the service
layer pattern (ADR-006). The tool is a thin wrapper that:
1. Validates input with Pydantic
2. Extracts dependencies from server context (ADR-007)
3. Delegates to MultiTestReportService (STORY-023e)
4. Converts exceptions to user-friendly error format
"""

from datetime import datetime
from typing import Annotated, Any, Literal

from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, Field, field_validator, model_validator

from testio_mcp.exceptions import ProductNotFoundException, TestIOAPIError
from testio_mcp.server import mcp
from testio_mcp.services.multi_test_report_service import MultiTestReportService
from testio_mcp.utilities import get_service_context
from testio_mcp.utilities.date_utils import parse_flexible_date
from testio_mcp.utilities.schema_utils import inline_schema_refs

# Type aliases for valid values (using Literal to avoid $defs in JSON schema)

TestStatus = Literal[
    "running", "locked", "archived", "cancelled", "customer_finalized", "initialized"
]

# Pydantic Models
# NOTE: Models use nested BaseModel classes for type safety and better FastAPI docs.
# Schemas are post-processed with inline_schema_refs() to avoid $ref resolution issues
# in some MCP clients like Gemini CLI 0.16.0.


class GetProductQualityReportInput(BaseModel):
    """Input validation for get_product_quality_report tool.

    Validates:
    1. Per-field: Rejects ambiguous year-only inputs (e.g., "2025")
    2. Cross-field: Validates date range (start_date <= end_date) after parsing
    """

    product_id: int = Field(gt=0)
    start_date: str | None = None
    end_date: str | None = None
    statuses: str | list[str] | None = None
    output_file: str | None = None

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def validate_date_format(cls, v: str | None) -> str | None:
        """Validate date format and reject ambiguous year-only inputs.

        This runs BEFORE cross-field validation, catching year-only inputs
        like "2025" with a clear error message.

        Args:
            v: Date string value

        Returns:
            Original date string if valid (or None)

        Raises:
            ValueError: If date is year-only format (ambiguous)
        """
        if v is None:
            return v

        # Validate using parse_flexible_date (includes year-only check)
        # This will raise ToolError for invalid formats, which we convert to ValueError
        try:
            parse_flexible_date(v, start_of_day=True)
            return v
        except ToolError as e:
            # Convert ToolError to ValueError so Pydantic can handle it
            raise ValueError(str(e)) from e

    @model_validator(mode="after")
    def validate_date_range(self) -> "GetProductQualityReportInput":
        """Validate that start_date <= end_date after parsing flexible formats.

        Raises:
            ValueError: If start_date > end_date or date parsing fails
        """
        if self.start_date and self.end_date:
            # Parse dates using flexible parser
            try:
                parsed_start = parse_flexible_date(self.start_date, start_of_day=True)
                parsed_end = parse_flexible_date(self.end_date, start_of_day=False)

                # Convert to datetime for comparison
                start_dt = datetime.fromisoformat(parsed_start.replace("Z", "+00:00"))
                end_dt = datetime.fromisoformat(parsed_end.replace("Z", "+00:00"))

                # Validate start <= end
                if start_dt > end_dt:
                    raise ValueError(
                        f"start_date is after end_date: "
                        f"start_date='{self.start_date}' ({parsed_start}) > "
                        f"end_date='{self.end_date}' ({parsed_end}). "
                        f"Ensure start_date comes before or equals end_date."
                    )
            except ToolError as e:
                # Convert ToolError to ValueError so Pydantic can handle it
                raise ValueError(str(e)) from e

        return self


class BugCounts(BaseModel):
    """Bug classification counts for a test."""

    active_accepted: int = Field(description="Actively accepted by customer")
    auto_accepted: int = Field(description="Auto-accepted after 10 days")
    rejected: int = Field(description="Rejected by customer")
    open: int = Field(description="Forwarded to customer")
    total_accepted: int = Field(description="Active + auto", ge=0)
    reviewed: int = Field(description="Active + rejected", ge=0)


class TestBugMetrics(BaseModel):
    """Bug metrics for a single test in EBR."""

    __test__ = False

    test_id: int = Field(description="Test ID")
    title: str = Field(description="Test title")
    status: str = Field(description="Lifecycle status")
    start_at: str | None = Field(description="Start date (ISO 8601)")
    end_at: str | None = Field(description="End date (ISO 8601)")
    bugs_count: int = Field(description="Total bugs", ge=0)
    bugs: BugCounts = Field(description="Bug counts by classification")
    test_environment: dict[str, Any] | None = Field(
        default=None, description="Test environment info (id, title)"
    )
    active_acceptance_rate: float | None = Field(
        default=None, description="active_accepted / total_bugs", ge=0.0, le=1.0
    )
    auto_acceptance_rate: float | None = Field(
        default=None, description="auto_accepted / (active + auto)", ge=0.0, le=1.0
    )
    overall_acceptance_rate: float | None = Field(
        default=None, description="(active + auto) / total_bugs", ge=0.0, le=1.0
    )
    rejection_rate: float | None = Field(
        default=None, description="rejected / total_bugs", ge=0.0, le=1.0
    )
    review_rate: float | None = Field(
        default=None, description="(active + rejected) / total_bugs", ge=0.0, le=1.0
    )


class ProductQualityReportSummary(BaseModel):
    """Summary metrics aggregated across all tests."""

    total_tests: int = Field(ge=0, description="Tests in report")
    tests_by_status: dict[str, int] = Field(description="Tests by status")
    statuses_applied: list[str] | str = Field(
        description="Statuses included (default: excludes initialized, cancelled)"
    )
    total_bugs: int = Field(ge=0, description="Total bugs")
    bugs_by_status: dict[str, int] = Field(description="Bugs by classification")
    bugs_by_severity: dict[str, int] = Field(
        default_factory=dict, description="Bugs by severity (critical, high, etc.)"
    )
    tests_by_type: dict[str, int] = Field(
        default_factory=dict, description="Tests by testing type (rapid, focused, etc.)"
    )
    total_accepted: int = Field(ge=0, description="Active + auto")
    reviewed: int = Field(ge=0, description="Active + rejected")
    active_acceptance_rate: float | None = Field(
        default=None, description="active_accepted / total_bugs", ge=0.0, le=1.0
    )
    auto_acceptance_rate: float | None = Field(
        default=None, description="auto_accepted / (active + auto)", ge=0.0, le=1.0
    )
    overall_acceptance_rate: float | None = Field(
        default=None, description="(active + auto) / total_bugs", ge=0.0, le=1.0
    )
    rejection_rate: float | None = Field(
        default=None, description="rejected / total_bugs", ge=0.0, le=1.0
    )
    review_rate: float | None = Field(
        default=None, description="(active + rejected) / total_bugs", ge=0.0, le=1.0
    )
    avg_bugs_per_test: float | None = Field(
        default=None, description="Average bugs per test (efficiency metric)", ge=0.0
    )
    period: str = Field(description="Report period")


class CacheStats(BaseModel):
    """Bug cache efficiency statistics."""

    total_tests: int = Field(ge=0, description="Tests processed")
    cache_hits: int = Field(ge=0, description="From SQLite")
    api_calls: int = Field(ge=0, description="From API")
    cache_hit_rate: float = Field(ge=0.0, le=100.0, description="Cache hit %")
    breakdown: dict[str, int] = Field(description="Cache decisions by category")


class GetProductQualityReportOutput(BaseModel):
    """Product Quality Report output (full report or file export metadata)."""

    # Full report fields
    summary: ProductQualityReportSummary = Field(description="Aggregate metrics")
    by_test: list[TestBugMetrics] | None = Field(
        default=None, description="Per-test metrics (omitted for file export)"
    )
    cache_stats: CacheStats | None = Field(
        default=None, description="Cache efficiency (omitted for file export)"
    )

    # File export fields
    file_path: str | None = Field(default=None, description="Export file path")
    record_count: int | None = Field(default=None, ge=0, description="Tests exported")
    file_size_bytes: int | None = Field(default=None, ge=0, description="File size (bytes)")
    format: Literal["json"] | None = Field(default=None, description="File format")


# MCP Tool
@mcp.tool(output_schema=inline_schema_refs(GetProductQualityReportOutput.model_json_schema()))
async def get_product_quality_report(
    product_id: Annotated[
        int,
        Field(gt=0, description="Product ID (use list_products to find)", examples=[598]),
    ],
    ctx: Context,
    start_date: Annotated[
        str | None,
        Field(
            description="Start date (ISO 8601 or business terms). No year-only values",
            examples=["2025-07-01", "last 30 days", "this quarter"],
        ),
    ] = None,
    end_date: Annotated[
        str | None,
        Field(
            description="End date (ISO 8601 or business terms). No year-only values",
            examples=["2025-10-31", "today"],
        ),
    ] = None,
    statuses: Annotated[
        str | list[TestStatus] | None,
        Field(
            description=(
                "Filter by status. Default: excludes initialized, cancelled. "
                "Comma-separated or array"
            ),
            examples=["locked", "running,locked", ["locked"], ["running", "locked"]],
        ),
    ] = None,
    output_file: Annotated[
        str | None,
        Field(
            description=(
                "Export to file (avoids token limits for >100 tests). "
                "Relative paths → ~/.testio-mcp/reports/"
            ),
            examples=["canva-q3-2025.json", "q3-2025/canva.json"],
        ),
    ] = None,
) -> dict[str, Any]:
    """Generate product quality report with bug metrics, acceptance rates, and per-test summaries.

    Date filters support ISO 8601 or business terms (e.g., 'last 30 days'). No year-only values.
    Default excludes initialized/cancelled tests (executed tests only).

    For large products (>100 tests), use output_file to export to ~/.testio-mcp/reports/.
    Returns file metadata instead of full data.

    Uses intelligent caching (10-30s for 100+ tests). For fresh data, call sync_data first.
    """
    # Validate input with Pydantic (including date range validation)
    # Convert TestStatus Literal types to strings for Pydantic model
    statuses_for_validation: str | list[str] | None = None
    if statuses is not None:
        if isinstance(statuses, str):
            statuses_for_validation = statuses
        else:
            # Convert list of Literal types to list of strings
            statuses_for_validation = [str(s) for s in statuses]

    try:
        validated_input = GetProductQualityReportInput(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            statuses=statuses_for_validation,
            output_file=output_file,
        )
    except ValueError as e:
        # Pydantic validation error (including date range validation)
        error_msg = str(e)
        if "start_date is after end_date" in error_msg:
            raise ToolError(
                f"❌ Invalid date range: {error_msg}\n"
                f"ℹ️  The start date must come before or equal to the end date\n"
                f"💡 For single-day reports, use the same date for both parameters. "
                f"For date ranges, ensure start_date < end_date."
            ) from e
        # Other validation errors
        raise ToolError(
            f"❌ Invalid input: {error_msg}\n"
            f"ℹ️  Check your parameter values\n"
            f"💡 Ensure all parameters are in the correct format"
        ) from e

    # Create service with managed AsyncSession lifecycle (STORY-033)
    async with get_service_context(ctx, MultiTestReportService) as service:
        # Parse comma-separated string to list if needed (AI-friendly format)
        statuses_list: list[str] | None = None
        if validated_input.statuses is not None:
            if isinstance(validated_input.statuses, str):
                # Parse comma-separated string: "running,locked" -> ["running", "locked"]
                statuses_list = [s.strip() for s in validated_input.statuses.split(",")]
            else:
                # Extract enum values and convert to list of strings
                from enum import Enum

                statuses_list = [
                    s.value if isinstance(s, Enum) else s for s in validated_input.statuses
                ]

        # Delegate to service and convert exceptions to MCP error format
        try:
            service_result = await service.get_product_quality_report(
                product_id=product_id,
                start_date=start_date,
                end_date=end_date,
                statuses=statuses_list,
                output_file=output_file,
            )

            # If output_file is specified, service returns file metadata
            if output_file is not None:
                # Service already wrote file and returned metadata
                # Return file export response (by_test and cache_stats are None)
                output = GetProductQualityReportOutput(
                    summary=ProductQualityReportSummary(
                        total_tests=service_result["summary"]["total_tests"],
                        tests_by_status=service_result["summary"]["tests_by_status"],
                        statuses_applied=service_result["summary"]["statuses_applied"],
                        total_bugs=service_result["summary"]["total_bugs"],
                        bugs_by_status=service_result["summary"]["bugs_by_status"],
                        bugs_by_severity=service_result["summary"].get("bugs_by_severity", {}),
                        tests_by_type=service_result["summary"].get("tests_by_type", {}),
                        total_accepted=service_result["summary"]["total_accepted"],
                        reviewed=service_result["summary"]["reviewed"],
                        active_acceptance_rate=service_result["summary"].get(
                            "active_acceptance_rate"
                        ),
                        auto_acceptance_rate=service_result["summary"].get("auto_acceptance_rate"),
                        overall_acceptance_rate=service_result["summary"].get(
                            "overall_acceptance_rate"
                        ),
                        rejection_rate=service_result["summary"].get("rejection_rate"),
                        review_rate=service_result["summary"].get("review_rate"),
                        avg_bugs_per_test=service_result["summary"].get("avg_bugs_per_test"),
                        period=service_result["summary"]["period"],
                    ),
                    by_test=None,  # Omitted for file export
                    cache_stats=None,  # Omitted for file export
                    file_path=service_result["file_path"],
                    record_count=service_result["record_count"],
                    file_size_bytes=service_result["file_size_bytes"],
                    format=service_result["format"],
                )
                return output.model_dump(by_alias=True, exclude_none=True)

            # Otherwise, transform service result to tool output format
            summary = service_result["summary"]
            by_test = service_result["by_test"]
            cache_stats = service_result["cache_stats"]

            # Build validated output
            output = GetProductQualityReportOutput(
                summary=ProductQualityReportSummary(
                    total_tests=summary["total_tests"],
                    tests_by_status=summary["tests_by_status"],
                    statuses_applied=summary["statuses_applied"],
                    total_bugs=summary["total_bugs"],
                    bugs_by_status=summary["bugs_by_status"],
                    bugs_by_severity=summary.get("bugs_by_severity", {}),
                    tests_by_type=summary.get("tests_by_type", {}),
                    total_accepted=summary["total_accepted"],
                    reviewed=summary["reviewed"],
                    active_acceptance_rate=summary.get("active_acceptance_rate"),
                    auto_acceptance_rate=summary.get("auto_acceptance_rate"),
                    overall_acceptance_rate=summary.get("overall_acceptance_rate"),
                    rejection_rate=summary.get("rejection_rate"),
                    review_rate=summary.get("review_rate"),
                    avg_bugs_per_test=summary.get("avg_bugs_per_test"),
                    period=summary["period"],
                ),
                cache_stats=CacheStats(
                    total_tests=cache_stats["total_tests"],
                    cache_hits=cache_stats["cache_hits"],
                    api_calls=cache_stats["api_calls"],
                    cache_hit_rate=cache_stats["cache_hit_rate"],
                    breakdown=cache_stats["breakdown"],
                ),
                by_test=[
                    TestBugMetrics(
                        test_id=test["test_id"],
                        title=test["title"],
                        status=test["status"],
                        start_at=test.get("start_at"),
                        end_at=test.get("end_at"),
                        bugs_count=test["bugs_count"],
                        bugs=BugCounts(
                            active_accepted=test["bugs"]["active_accepted"],
                            auto_accepted=test["bugs"]["auto_accepted"],
                            rejected=test["bugs"]["rejected"],
                            open=test["bugs"]["open"],
                            total_accepted=test["bugs"]["total_accepted"],
                            reviewed=test["bugs"]["reviewed"],
                        ),
                        test_environment=test.get("test_environment"),
                        active_acceptance_rate=test.get("active_acceptance_rate"),
                        auto_acceptance_rate=test.get("auto_acceptance_rate"),
                        overall_acceptance_rate=test.get("overall_acceptance_rate"),
                        rejection_rate=test.get("rejection_rate"),
                        review_rate=test.get("review_rate"),
                    )
                    for test in by_test
                ],
                # File export fields are None for full report
                file_path=None,
                record_count=None,
                file_size_bytes=None,
                format=None,
            )

            return output.model_dump(by_alias=True, exclude_none=True)

        except ProductNotFoundException as e:
            # Convert domain exception to ToolError with user-friendly message
            raise ToolError(
                f"❌ Product ID '{e.product_id}' not found\n"
                f"ℹ️  This product may not exist or you don't have access to it\n"
                f"💡 Use the list_products tool to see available products"
            ) from e

        except TestIOAPIError as e:
            # Convert API error to ToolError with user-friendly message
            raise ToolError(
                f"❌ API error: {e.message}\n"
                f"ℹ️  HTTP status code: {e.status_code}\n"
                f"💡 Check API status and try again. If the problem persists, contact support."
            ) from e

        except (PermissionError, OSError) as e:
            # File write errors (permissions, disk full, etc.)
            error_type = "permission" if isinstance(e, PermissionError) else "I/O"
            raise ToolError(
                f"❌ File export failed: {error_type} error\n"
                f"ℹ️  Cannot write to file: {str(e)}\n"
                f"💡 Check file permissions and disk space. "
                f"For relative paths, ensure ~/.testio-mcp/reports/ is writable."
            ) from e

        except ValueError as e:
            # Path validation errors (invalid path, unsupported extension, path traversal)
            if "path" in str(e).lower() or "extension" in str(e).lower():
                raise ToolError(
                    f"❌ Invalid output file path\n"
                    f"ℹ️  {str(e)}\n"
                    f"💡 Use absolute paths or relative paths under ~/.testio-mcp/reports/. "
                    f"Supported extensions: .json"
                ) from e
            # Re-raise other ValueError (e.g., from date parsing)
            raise

        except ToolError:
            # Re-raise ToolError from parse_flexible_date (already formatted)
            raise

        except Exception as e:
            # Catch-all for unexpected errors
            raise ToolError(
                f"❌ Unexpected error: {str(e)}\n"
                f"ℹ️  An unexpected error occurred while generating EBR\n"
                f"💡 Please try again or contact support if the problem persists"
            ) from e
