"""Unit tests for MultiTestReportService file export functionality (STORY-025).

Tests verify that:
1. File export writes report data to JSON file
2. File metadata response structure is correct
3. Parent directories are created automatically
4. Relative vs absolute paths work correctly
5. File overwrite succeeds
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from testio_mcp.services.multi_test_report_service import MultiTestReportService


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_writes_json_file(tmp_path: Path) -> None:
    """Verify file export writes report data to JSON file with proper formatting."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    # Mock product info
    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}

    # Mock test query result
    mock_test_repo.query_tests.return_value = [
        {
            "id": 1,
            "title": "Test 1",
            "status": "locked",
            "start_at": "2024-01-01T00:00:00+00:00",
            "end_at": "2024-01-02T00:00:00+00:00",
        }
    ]

    # Mock bug repository response
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {1: []},  # No bugs
        {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    )

    service = MultiTestReportService(
        client=mock_client,
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Create output file path
    output_file = str(tmp_path / "test_report.json")

    # Call with output_file specified
    result = await service.get_product_quality_report(
        product_id=123,
        output_file=output_file,
    )

    # Verify file was written
    assert Path(output_file).exists()

    # Verify file contents match expected structure
    file_content = Path(output_file).read_text(encoding="utf-8")
    file_data = json.loads(file_content)

    assert "summary" in file_data
    assert "by_test" in file_data
    assert "cache_stats" in file_data

    # Verify file metadata response structure
    assert "file_path" in result
    assert "summary" in result
    assert "record_count" in result
    assert "file_size_bytes" in result
    assert "format" in result

    # Verify metadata values
    assert result["file_path"] == output_file
    assert result["record_count"] == 1
    assert result["format"] == "json"
    assert result["file_size_bytes"] > 0

    # Verify summary in metadata matches file summary
    assert result["summary"]["total_tests"] == file_data["summary"]["total_tests"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_creates_parent_directories(tmp_path: Path) -> None:
    """Verify parent directories are created automatically for nested paths."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}
    mock_test_repo.query_tests.return_value = []
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

    # Create nested path (parent doesn't exist)
    output_file = str(tmp_path / "reports" / "q3-2025" / "test_report.json")

    # Call with output_file specified
    result = await service.get_product_quality_report(
        product_id=123,
        output_file=output_file,
    )

    # Verify parent directories were created
    assert Path(output_file).parent.exists()
    assert Path(output_file).exists()

    # Verify file was written
    assert result["file_path"] == output_file


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_relative_path_resolves_to_reports_dir(tmp_path: Path) -> None:
    """Verify relative paths resolve to ~/.testio-mcp/reports/ directory."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}
    mock_test_repo.query_tests.return_value = []
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

    # Use relative path
    relative_path = "test_report.json"

    # Mock Path.home() to return tmp_path for testing
    with patch("testio_mcp.utilities.file_export.Path.home", return_value=tmp_path):
        result = await service.get_product_quality_report(
            product_id=123,
            output_file=relative_path,
        )

        # Verify path resolved to reports directory
        expected_path = tmp_path / ".testio-mcp" / "reports" / relative_path
        assert result["file_path"] == str(expected_path)
        assert Path(result["file_path"]).exists()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_absolute_path_used_as_is(tmp_path: Path) -> None:
    """Verify absolute paths are used as-is (after expanding ~)."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}
    mock_test_repo.query_tests.return_value = []
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

    # Use absolute path
    absolute_path = str(tmp_path / "absolute_report.json")

    # Call with absolute path
    result = await service.get_product_quality_report(
        product_id=123,
        output_file=absolute_path,
    )

    # Verify absolute path used as-is
    assert result["file_path"] == absolute_path
    assert Path(absolute_path).exists()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_overwrites_existing_file(tmp_path: Path) -> None:
    """Verify file overwrite succeeds (existing file is replaced)."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}
    mock_test_repo.query_tests.return_value = [
        {
            "id": 1,
            "title": "Test 1",
            "status": "locked",
            "start_at": "2024-01-01T00:00:00+00:00",
            "end_at": "2024-01-02T00:00:00+00:00",
        }
    ]
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {1: []},
        {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    )

    service = MultiTestReportService(
        client=mock_client,
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    output_file = str(tmp_path / "test_report.json")

    # Create existing file with different content
    Path(output_file).write_text('{"old": "data"}', encoding="utf-8")
    original_size = Path(output_file).stat().st_size

    # Call with output_file (should overwrite)
    await service.get_product_quality_report(
        product_id=123,
        output_file=output_file,
    )

    # Verify file was overwritten
    assert Path(output_file).exists()
    new_size = Path(output_file).stat().st_size
    assert new_size != original_size  # Size changed

    # Verify new content is correct
    file_data = json.loads(Path(output_file).read_text(encoding="utf-8"))
    assert "summary" in file_data
    assert "by_test" in file_data


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_metadata_structure() -> None:
    """Verify file export metadata response has correct structure."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}
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
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {1: [], 2: []},
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

    # Call with output_file (using MagicMock to avoid actual file I/O)
    with (
        patch("testio_mcp.services.multi_test_report_service.resolve_output_path") as mock_resolve,
        patch("testio_mcp.services.multi_test_report_service.write_report_to_file") as mock_write,
        patch("testio_mcp.services.multi_test_report_service.get_file_format") as mock_format,
    ):
        mock_path = MagicMock(spec=Path)
        mock_path.__str__ = lambda self: "/tmp/test_report.json"
        mock_resolve.return_value = mock_path
        mock_write.return_value = 1024  # File size in bytes
        mock_format.return_value = "json"

        result = await service.get_product_quality_report(
            product_id=123,
            output_file="test_report.json",
        )

        # Verify metadata structure
        assert "file_path" in result
        assert "summary" in result
        assert "record_count" in result
        assert "file_size_bytes" in result
        assert "format" in result

        # Verify metadata values
        assert result["file_path"] == "/tmp/test_report.json"
        assert result["record_count"] == 2
        assert result["file_size_bytes"] == 1024
        assert result["format"] == "json"

        # Verify summary is included (without by_test array)
        assert "total_tests" in result["summary"]
        assert "tests_by_status" in result["summary"]
        assert "total_bugs" in result["summary"]
        assert result["summary"]["total_tests"] == 2

        # Verify by_test is NOT in metadata (only in file)
        assert "by_test" not in result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_file_export_returns_full_data_when_output_file_none() -> None:
    """Verify service returns full report data when output_file is None."""
    # Setup: Mock dependencies
    mock_client = AsyncMock()
    mock_test_repo = AsyncMock()
    mock_bug_repo = AsyncMock()

    mock_test_repo.get_product_info.return_value = {"id": 123, "name": "Test Product"}
    mock_test_repo.query_tests.return_value = [
        {
            "id": 1,
            "title": "Test 1",
            "status": "locked",
            "start_at": "2024-01-01T00:00:00+00:00",
            "end_at": "2024-01-02T00:00:00+00:00",
        }
    ]
    mock_bug_repo.get_bugs_cached_or_refresh.return_value = (
        {1: []},
        {
            "total_tests": 1,
            "cache_hits": 1,
            "api_calls": 0,
            "cache_hit_rate": 100.0,
            "breakdown": {"immutable_cached": 1},
        },
    )

    service = MultiTestReportService(
        client=mock_client,
        test_repo=mock_test_repo,
        bug_repo=mock_bug_repo,
        product_repo=AsyncMock(),
    )

    # Call without output_file (should return full data)
    result = await service.get_product_quality_report(
        product_id=123,
        output_file=None,
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
