"""Analytics models.

Pydantic models for analytics responses.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from hr_platform.models.enums import Entity


class AnalyticsSummary(BaseModel):
    """Aggregated summary metrics.

    Contains total counts and aggregations across selected
    entity/year/month filters.
    """

    model_config = ConfigDict(populate_by_name=True)

    record_count: int = Field(description="Number of records in aggregation")
    total_headcount: int = Field(description="Total employees")
    blue_collar_total: int = Field(description="Total blue collar employees")
    white_collar_total: int = Field(description="Total white collar employees")
    total_internal_fte: float = Field(description="Total internal FTE")
    total_external_fte: float = Field(description="Total external FTE")
    total_sick_days: int = Field(description="Total sick days")
    total_costs: float = Field(description="Total personnel costs (EUR)")
    total_turnover: int = Field(description="Total employee departures")
    total_reviews_completed: int = Field(description="Total annual reviews completed")


class TrendDataPoint(BaseModel):
    """Single data point in trend time series.

    Represents metrics for a specific month.
    """

    model_config = ConfigDict(populate_by_name=True)

    year: int = Field(description="Year")
    month: int = Field(description="Month (1-12)")
    entity: Entity = Field(description="Entity code")

    headcount: int = Field(description="Total headcount")
    blue_collar: int = Field(description="Blue collar headcount")
    white_collar: int = Field(description="White collar headcount")
    internal_fte: float = Field(description="Internal FTE")
    external_fte: float = Field(description="External FTE (hours/173)")
    sick_days: int = Field(description="Sick days")
    working_days: int = Field(description="Working days in month")
    sick_rate: float = Field(description="Sick rate percentage")
    turnover: int = Field(description="Total departures")
    reviews_completed: int = Field(description="Reviews completed")
    wages: float = Field(description="Blue collar wages (EUR)")
    salaries: float = Field(description="White collar salaries (EUR)")
    temp_wages: float = Field(description="Temp/external costs (EUR)")


class EntityBreakdown(BaseModel):
    """Aggregated data for a single entity.

    Used for entity comparison charts.
    """

    model_config = ConfigDict(populate_by_name=True)

    entity: Entity = Field(description="Entity code")
    record_count: int = Field(description="Number of records")
    total_headcount: int = Field(description="Total headcount")
    blue_collar: int = Field(description="Blue collar headcount")
    white_collar: int = Field(description="White collar headcount")


class AnalyticsQueryParams(BaseModel):
    """Query parameters for analytics endpoints.

    All parameters are optional - defaults to all entities/years/months.
    """

    entity: str | None = Field(
        default=None, description="Entity filter (BVD, VHH, VHO, or 'All')"
    )
    year: str | None = Field(
        default=None, description="Year filter (e.g., '2025' or 'All')"
    )
    month: str | None = Field(
        default=None, description="Month filter (1-12 or 'All')"
    )

    def to_params(self) -> dict[str, str]:
        """Convert to query parameter dict, excluding None values."""
        params: dict[str, str] = {}
        if self.entity is not None:
            params["entity"] = self.entity
        if self.year is not None:
            params["year"] = self.year
        if self.month is not None:
            params["month"] = self.month
        return params
