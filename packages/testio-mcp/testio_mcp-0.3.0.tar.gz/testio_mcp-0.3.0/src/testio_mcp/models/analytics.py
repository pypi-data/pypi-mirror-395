"""Pydantic models for analytics responses.

These models provide type-safe data structures for analytics query results.

STORY-043: Analytics Service (The Engine)
Epic: EPIC-007 (Generic Analytics Framework)
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class QueryMetadata(BaseModel):
    """Metadata about an analytics query execution.

    Attributes:
        total_rows: Number of rows returned in the result set
        dimensions_used: List of dimension keys used for grouping
        metrics_used: List of metric keys measured
        query_time_ms: Query execution time in milliseconds
    """

    total_rows: int = Field(..., ge=0, description="Number of rows in result set")
    dimensions_used: list[str] = Field(..., description="Dimension keys used for grouping")
    metrics_used: list[str] = Field(..., description="Metric keys measured")
    query_time_ms: int = Field(..., ge=0, description="Query execution time in milliseconds")


class QueryResponse(BaseModel):
    """Response structure for analytics queries.

    Contains query results with rich metadata and human-readable explanation.

    Attributes:
        data: Query result rows (structure varies by dimensions/metrics)
        metadata: Query execution metadata
        query_explanation: Human-readable description of what was queried
        warnings: List of warnings or caveats about the results
    """

    data: list[dict[str, Any]] = Field(..., description="Query result rows with dynamic schema")
    metadata: QueryMetadata = Field(..., description="Query execution metadata")
    query_explanation: str = Field(..., description="Human-readable query description")
    warnings: list[str] = Field(default_factory=list, description="Result caveats")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": [
                    {"feature_id": 1, "feature": "Login", "bug_count": 10},
                    {"feature_id": 2, "feature": "Dashboard", "bug_count": 5},
                ],
                "metadata": {
                    "total_rows": 2,
                    "dimensions_used": ["feature"],
                    "metrics_used": ["bug_count"],
                    "query_time_ms": 45,
                },
                "query_explanation": (
                    "Showing Total number of bugs found grouped by "
                    "Group by Feature Title, sorted by bug_count descending"
                ),
                "warnings": [],
            }
        }
    )
