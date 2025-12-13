"""Tests for HR Platform SDK analytics resource."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from hr_platform.core.http import HttpClient
from hr_platform.models.analytics import AnalyticsSummary, EntityBreakdown, TrendDataPoint
from hr_platform.resources.analytics import AnalyticsResource


@pytest.fixture
def http_client() -> MagicMock:
    """Create a mock HTTP client."""
    mock = MagicMock(spec=HttpClient)
    return mock


@pytest.fixture
def analytics_resource(http_client: MagicMock) -> AnalyticsResource:
    """Create analytics resource with mock HTTP client."""
    return AnalyticsResource(http_client)


class TestAnalyticsResourceSummary:
    """Tests for analytics.get_summary() method."""

    def test_get_summary_no_filters(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_analytics_summary: dict,
    ) -> None:
        """Test getting summary without filters."""
        http_client.get.return_value = mock_analytics_summary

        result = analytics_resource.get_summary()

        # When no filters, params is None (not {})
        http_client.get.assert_called_once_with("/analytics/summary", params=None)
        assert isinstance(result, AnalyticsSummary)
        assert result.record_count == 12
        assert result.total_headcount == 480

    def test_get_summary_with_entity_filter(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_analytics_summary: dict,
    ) -> None:
        """Test getting summary with entity filter."""
        http_client.get.return_value = mock_analytics_summary

        result = analytics_resource.get_summary(entity="BVD")

        http_client.get.assert_called_once_with(
            "/analytics/summary", params={"entity": "BVD"}
        )

    def test_get_summary_with_year_filter(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_analytics_summary: dict,
    ) -> None:
        """Test getting summary with year filter."""
        http_client.get.return_value = mock_analytics_summary

        result = analytics_resource.get_summary(year="2025")

        http_client.get.assert_called_once_with(
            "/analytics/summary", params={"year": "2025"}
        )

    def test_get_summary_with_multiple_filters(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_analytics_summary: dict,
    ) -> None:
        """Test getting summary with multiple filters."""
        http_client.get.return_value = mock_analytics_summary

        result = analytics_resource.get_summary(entity="BVD", year="2025", month="12")

        http_client.get.assert_called_once_with(
            "/analytics/summary",
            params={"entity": "BVD", "year": "2025", "month": "12"},
        )

    def test_get_summary_all_entity(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_analytics_summary: dict,
    ) -> None:
        """Test getting summary for all entities."""
        http_client.get.return_value = mock_analytics_summary

        result = analytics_resource.get_summary(entity="All")

        http_client.get.assert_called_once_with(
            "/analytics/summary", params={"entity": "All"}
        )


class TestAnalyticsResourceTrends:
    """Tests for analytics.get_trends() method."""

    def test_get_trends_no_filters(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_trend_data: list[dict],
    ) -> None:
        """Test getting trends without filters."""
        http_client.get.return_value = mock_trend_data

        result = analytics_resource.get_trends()

        # When no filters, params is None (not {})
        http_client.get.assert_called_once_with("/analytics/trends", params=None)
        assert len(result) == 2
        assert all(isinstance(item, TrendDataPoint) for item in result)

    def test_get_trends_with_entity_filter(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_trend_data: list[dict],
    ) -> None:
        """Test getting trends with entity filter."""
        http_client.get.return_value = mock_trend_data

        result = analytics_resource.get_trends(entity="BVD")

        http_client.get.assert_called_once_with(
            "/analytics/trends", params={"entity": "BVD"}
        )

    def test_get_trends_data_points(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_trend_data: list[dict],
    ) -> None:
        """Test trend data point values."""
        http_client.get.return_value = mock_trend_data

        result = analytics_resource.get_trends()

        first = result[0]
        assert first.year == 2025
        assert first.month == 1
        assert first.entity == "BVD"
        assert first.headcount == 40
        assert first.sick_rate == 0.83

    def test_get_trends_empty_result(
        self, analytics_resource: AnalyticsResource, http_client: MagicMock
    ) -> None:
        """Test getting trends returns empty list."""
        http_client.get.return_value = []

        result = analytics_resource.get_trends()

        assert result == []


class TestAnalyticsResourceByEntity:
    """Tests for analytics.get_by_entity() method."""

    def test_get_by_entity(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_entity_breakdown: list[dict],
    ) -> None:
        """Test getting entity breakdown."""
        http_client.get.return_value = mock_entity_breakdown

        result = analytics_resource.get_by_entity()

        # Base resource always passes params=None to HTTP client
        http_client.get.assert_called_once_with("/analytics/by-entity", params=None)
        assert len(result) == 3
        assert all(isinstance(item, EntityBreakdown) for item in result)

    def test_get_by_entity_values(
        self,
        analytics_resource: AnalyticsResource,
        http_client: MagicMock,
        mock_entity_breakdown: list[dict],
    ) -> None:
        """Test entity breakdown values."""
        http_client.get.return_value = mock_entity_breakdown

        result = analytics_resource.get_by_entity()

        bvd = next(e for e in result if e.entity == "BVD")
        assert bvd.record_count == 12
        assert bvd.total_headcount == 480
        assert bvd.blue_collar == 264
        assert bvd.white_collar == 216

    def test_get_by_entity_empty_result(
        self, analytics_resource: AnalyticsResource, http_client: MagicMock
    ) -> None:
        """Test getting entity breakdown returns empty list."""
        http_client.get.return_value = []

        result = analytics_resource.get_by_entity()

        assert result == []
