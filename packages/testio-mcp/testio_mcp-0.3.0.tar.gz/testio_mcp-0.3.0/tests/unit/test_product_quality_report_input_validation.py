"""Unit tests for GetProductQualityReportInput Pydantic model validation.

Tests validate date range logic (start_date <= end_date) after parsing flexible formats.
"""

from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from testio_mcp.tools.product_quality_report_tool import GetProductQualityReportInput


@pytest.mark.unit
class TestGetProductQualityReportInputValidation:
    """Test Pydantic model validation for get_product_quality_report input."""

    def test_valid_iso_date_range(self) -> None:
        """Test that valid ISO date range (start < end) passes validation."""
        validated = GetProductQualityReportInput(
            product_id=598,
            start_date="2025-07-01",
            end_date="2025-10-31",
        )
        assert validated.product_id == 598
        assert validated.start_date == "2025-07-01"
        assert validated.end_date == "2025-10-31"

    def test_same_start_and_end_date_allowed(self) -> None:
        """Test that start_date == end_date is allowed (single day report)."""
        validated = GetProductQualityReportInput(
            product_id=598,
            start_date="2025-07-01",
            end_date="2025-07-01",
        )
        assert validated.start_date == "2025-07-01"
        assert validated.end_date == "2025-07-01"

    def test_start_date_after_end_date_raises_error(self) -> None:
        """Test that start_date > end_date raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            GetProductQualityReportInput(
                product_id=598,
                start_date="2025-10-01",  # October
                end_date="2025-07-01",  # July (before start!)
            )

        error_msg = str(exc_info.value)
        assert "start_date is after end_date" in error_msg
        assert "2025-10-01" in error_msg
        assert "2025-07-01" in error_msg

    @patch("testio_mcp.utilities.date_utils.datetime")
    def test_business_terms_validated_after_parsing(self, mock_datetime: object) -> None:
        """Test that business terms are validated after parsing to dates."""
        # Mock datetime.now to control "today"
        mock_datetime.now.return_value = datetime(2025, 11, 19, tzinfo=UTC)
        mock_datetime.strptime = datetime.strptime
        mock_datetime.fromisoformat = datetime.fromisoformat

        # "tomorrow" (Nov 20) to "yesterday" (Nov 18) = reversed!
        with pytest.raises(ValidationError) as exc_info:
            GetProductQualityReportInput(
                product_id=598,
                start_date="tomorrow",  # Nov 20
                end_date="yesterday",  # Nov 18 (before start!)
            )

        error_msg = str(exc_info.value)
        assert "start_date is after end_date" in error_msg

    def test_only_start_date_allowed(self) -> None:
        """Test that providing only start_date (no end_date) is allowed."""
        validated = GetProductQualityReportInput(
            product_id=598,
            start_date="2025-07-01",
            end_date=None,
        )
        assert validated.start_date == "2025-07-01"
        assert validated.end_date is None

    def test_only_end_date_allowed(self) -> None:
        """Test that providing only end_date (no start_date) is allowed."""
        validated = GetProductQualityReportInput(
            product_id=598,
            start_date=None,
            end_date="2025-10-31",
        )
        assert validated.start_date is None
        assert validated.end_date == "2025-10-31"

    def test_no_dates_allowed(self) -> None:
        """Test that omitting both dates is allowed (all-time report)."""
        validated = GetProductQualityReportInput(
            product_id=598,
            start_date=None,
            end_date=None,
        )
        assert validated.start_date is None
        assert validated.end_date is None

    def test_invalid_date_format_raises_error(self) -> None:
        """Test that invalid date format raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            GetProductQualityReportInput(
                product_id=598,
                start_date="not-a-date",
                end_date="2025-10-31",
            )

        error_msg = str(exc_info.value)
        # Should contain error from parse_flexible_date (converted to ValueError)
        assert "Could not parse date" in error_msg or "not-a-date" in error_msg

    def test_year_only_input_raises_error(self) -> None:
        """Test that year-only input (e.g., '2025') is rejected with clear error.

        Field validation catches year-only inputs BEFORE cross-field date range
        validation, providing a clear "ambiguous year-only input" error message.
        """
        with pytest.raises(ValidationError) as exc_info:
            GetProductQualityReportInput(
                product_id=598,
                start_date="2025",  # Year-only (ambiguous)
                end_date="2025-10-31",
            )

        error_msg = str(exc_info.value)
        # Should catch year-only validation, not date range validation
        assert "ambiguous" in error_msg.lower() or "year-only" in error_msg.lower()
        assert "2025" in error_msg

    def test_year_only_end_date_raises_error(self) -> None:
        """Test that year-only input in end_date is also rejected."""
        with pytest.raises(ValidationError) as exc_info:
            GetProductQualityReportInput(
                product_id=598,
                start_date="2025-07-01",
                end_date="2025",  # Year-only (ambiguous)
            )

        error_msg = str(exc_info.value)
        assert "ambiguous" in error_msg.lower() or "year-only" in error_msg.lower()
        assert "2025" in error_msg

    def test_product_id_validation(self) -> None:
        """Test that product_id must be positive integer."""
        with pytest.raises(ValidationError):
            GetProductQualityReportInput(
                product_id=0,  # Must be > 0
            )

        with pytest.raises(ValidationError):
            GetProductQualityReportInput(
                product_id=-1,  # Must be > 0
            )

    def test_all_parameters_optional_except_product_id(self) -> None:
        """Test that only product_id is required."""
        validated = GetProductQualityReportInput(product_id=598)
        assert validated.product_id == 598
        assert validated.start_date is None
        assert validated.end_date is None
        assert validated.statuses is None
        assert validated.output_file is None
