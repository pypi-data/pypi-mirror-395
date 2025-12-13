"""Analytics resource.

API resource for analytics and reporting operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from hr_platform.models.analytics import (
    AnalyticsQueryParams,
    AnalyticsSummary,
    EntityBreakdown,
    TrendDataPoint,
)
from hr_platform.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from hr_platform.core.async_http import AsyncHttpClient
    from hr_platform.core.http import HttpClient


class AnalyticsResource(BaseResource):
    """Synchronous analytics API resource.

    Provides methods for retrieving aggregated HR analytics data.

    Example:
        >>> summary = client.analytics.get_summary(entity="BVD")
        >>> trends = client.analytics.get_trends(entity="All")
        >>> by_entity = client.analytics.get_by_entity()
    """

    def __init__(self, client: "HttpClient") -> None:
        """Initialize analytics resource.

        Args:
            client: HTTP client instance.
        """
        super().__init__(client)

    def get_summary(
        self,
        *,
        entity: str | None = None,
        year: str | None = None,
        month: str | None = None,
    ) -> AnalyticsSummary:
        """Get aggregated summary metrics.

        Returns totals and aggregations across the selected filters.

        Args:
            entity: Filter by entity (BVD, VHH, VHO, or "All").
            year: Filter by year (e.g., "2025" or "All").
            month: Filter by month (1-12 or "All").

        Returns:
            Summary metrics including headcount, FTE, costs, etc.

        Example:
            >>> summary = client.analytics.get_summary(entity="BVD", year="2025")
            >>> print(f"Total headcount: {summary.total_headcount}")
            >>> print(f"Total costs: {summary.total_costs}")
        """
        params = AnalyticsQueryParams(entity=entity, year=year, month=month)
        query_params = params.to_params()
        data = self._get("/analytics/summary", params=query_params if query_params else None)
        return AnalyticsSummary.model_validate(data)

    def get_trends(
        self,
        *,
        entity: str | None = None,
    ) -> list[TrendDataPoint]:
        """Get trend data for time-series charts.

        Returns monthly data points for visualization.

        Args:
            entity: Filter by entity (BVD, VHH, VHO, or "All").

        Returns:
            List of trend data points ordered by year and month.

        Example:
            >>> trends = client.analytics.get_trends(entity="BVD")
            >>> for point in trends:
            ...     print(f"{point.year}/{point.month}: {point.headcount}")
        """
        params: dict[str, str] = {}
        if entity is not None:
            params["entity"] = entity

        data = self._get("/analytics/trends", params=params if params else None)
        return [TrendDataPoint.model_validate(item) for item in data]

    def get_by_entity(self) -> list[EntityBreakdown]:
        """Get breakdown of data by entity.

        Returns aggregated data grouped by entity for comparison.

        Returns:
            List of entity breakdowns with totals per entity.

        Example:
            >>> breakdown = client.analytics.get_by_entity()
            >>> for entity_data in breakdown:
            ...     print(f"{entity_data.entity}: {entity_data.total_headcount}")
        """
        data = self._get("/analytics/by-entity")
        return [EntityBreakdown.model_validate(item) for item in data]


class AsyncAnalyticsResource(AsyncBaseResource):
    """Asynchronous analytics API resource.

    Provides async methods for retrieving aggregated HR analytics data.

    Example:
        >>> summary = await client.analytics.get_summary(entity="BVD")
        >>> trends = await client.analytics.get_trends(entity="All")
    """

    def __init__(self, client: "AsyncHttpClient") -> None:
        """Initialize async analytics resource.

        Args:
            client: Async HTTP client instance.
        """
        super().__init__(client)

    async def get_summary(
        self,
        *,
        entity: str | None = None,
        year: str | None = None,
        month: str | None = None,
    ) -> AnalyticsSummary:
        """Get aggregated summary metrics.

        Returns totals and aggregations across the selected filters.

        Args:
            entity: Filter by entity (BVD, VHH, VHO, or "All").
            year: Filter by year (e.g., "2025" or "All").
            month: Filter by month (1-12 or "All").

        Returns:
            Summary metrics including headcount, FTE, costs, etc.
        """
        params = AnalyticsQueryParams(entity=entity, year=year, month=month)
        query_params = params.to_params()
        data = await self._get("/analytics/summary", params=query_params if query_params else None)
        return AnalyticsSummary.model_validate(data)

    async def get_trends(
        self,
        *,
        entity: str | None = None,
    ) -> list[TrendDataPoint]:
        """Get trend data for time-series charts.

        Returns monthly data points for visualization.

        Args:
            entity: Filter by entity (BVD, VHH, VHO, or "All").

        Returns:
            List of trend data points ordered by year and month.
        """
        params: dict[str, str] = {}
        if entity is not None:
            params["entity"] = entity

        data = await self._get("/analytics/trends", params=params if params else None)
        return [TrendDataPoint.model_validate(item) for item in data]

    async def get_by_entity(self) -> list[EntityBreakdown]:
        """Get breakdown of data by entity.

        Returns aggregated data grouped by entity for comparison.

        Returns:
            List of entity breakdowns with totals per entity.
        """
        data = await self._get("/analytics/by-entity")
        return [EntityBreakdown.model_validate(item) for item in data]
