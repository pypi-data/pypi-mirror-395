"""Tests for HR Platform SDK pandas helpers."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

# Skip all tests if pandas is not available
pytest.importorskip("pandas")

import pandas as pd

from hr_platform.models.analytics import AnalyticsSummary, EntityBreakdown, TrendDataPoint
from hr_platform.models.records import (
    Absences,
    Capacity,
    Financials,
    FullHRRecord,
    Performance,
    Turnover,
    Workforce,
)
from hr_platform.utils.pandas_helpers import (
    entity_breakdown_to_dataframe,
    records_to_dataframe,
    summary_to_series,
    trends_to_dataframe,
)


@pytest.fixture
def sample_workforce() -> Workforce:
    """Create sample workforce data."""
    return Workforce(
        bc_male=20,
        bc_female=2,
        bc_age_under_20=0,
        bc_age_20_29=5,
        bc_age_30_39=10,
        bc_age_40_49=4,
        bc_age_50_59=2,
        bc_age_60_plus=1,
        bc_ausgesteuert=1,
        wc_male=10,
        wc_female=8,
        wc_age_under_20=0,
        wc_age_20_29=2,
        wc_age_30_39=8,
        wc_age_40_49=5,
        wc_age_50_59=2,
        wc_age_60_plus=1,
        wc_ausgesteuert=0,
    )


@pytest.fixture
def sample_capacity() -> Capacity:
    """Create sample capacity data."""
    return Capacity(
        fte_blue_collar=20.2,
        fte_white_collar=14.0,
        fte_overhead=9.0,
        external_hours_blue=1350,
        external_hours_white=0,
        overtime_hours_blue=230,
        overtime_hours_white=0,
    )


@pytest.fixture
def sample_record(sample_workforce: Workforce, sample_capacity: Capacity) -> FullHRRecord:
    """Create sample full HR record."""
    return FullHRRecord(
        id="test-uuid-123",
        entity="BVD",
        year=2025,
        month=12,
        working_days=21,
        status="DRAFT",
        submitted_by=None,
        submitted_at=None,
        approved_by=None,
        approved_at=None,
        rejected_reason=None,
        created_at="2025-12-01T00:00:00.000Z",
        updated_at="2025-12-01T00:00:00.000Z",
        workforce=sample_workforce,
        capacity=sample_capacity,
        absences=Absences(
            sick_days_blue=7,
            sick_days_white=0,
            long_term_sick_fte=0.33,
            vacation_hours_blue=1248.8,
            vacation_hours_white=640,
            maternity_fte=0,
            parental_fte=0,
        ),
        turnover=Turnover(
            voluntary_bc=0,
            voluntary_wc=1,
            involuntary_bc=0,
            involuntary_wc=0,
        ),
        performance=Performance(
            year_reviews_blue=6,
            year_reviews_white=8,
        ),
        financials=Financials(
            wages=71333.95,
            salaries=93244.14,
            temp_wages=58592.64,
        ),
    )


@pytest.fixture
def sample_records(sample_record: FullHRRecord) -> list[FullHRRecord]:
    """Create list of sample records."""
    # Create a second record for VHH
    record2 = FullHRRecord(
        id="test-uuid-456",
        entity="VHH",
        year=2025,
        month=11,
        working_days=20,
        status="APPROVED",
        submitted_by="user-1",
        submitted_at="2025-11-15T00:00:00.000Z",
        approved_by="user-2",
        approved_at="2025-11-16T00:00:00.000Z",
        rejected_reason=None,
        created_at="2025-11-01T00:00:00.000Z",
        updated_at="2025-11-16T00:00:00.000Z",
        workforce=Workforce(
            bc_male=15,
            bc_female=5,
            bc_age_under_20=1,
            bc_age_20_29=4,
            bc_age_30_39=8,
            bc_age_40_49=4,
            bc_age_50_59=2,
            bc_age_60_plus=1,
            bc_ausgesteuert=0,
            wc_male=8,
            wc_female=12,
            wc_age_under_20=0,
            wc_age_20_29=3,
            wc_age_30_39=10,
            wc_age_40_49=5,
            wc_age_50_59=2,
            wc_age_60_plus=0,
            wc_ausgesteuert=1,
        ),
        capacity=Capacity(
            fte_blue_collar=18.0,
            fte_white_collar=16.0,
            fte_overhead=8.0,
            external_hours_blue=1000,
            external_hours_white=500,
            overtime_hours_blue=150,
            overtime_hours_white=50,
        ),
        absences=Absences(
            sick_days_blue=5,
            sick_days_white=3,
            long_term_sick_fte=0.5,
            vacation_hours_blue=1000,
            vacation_hours_white=800,
            maternity_fte=1.0,
            parental_fte=0.5,
        ),
        turnover=Turnover(
            voluntary_bc=1,
            voluntary_wc=0,
            involuntary_bc=1,
            involuntary_wc=0,
        ),
        performance=Performance(
            year_reviews_blue=10,
            year_reviews_white=15,
        ),
        financials=Financials(
            wages=65000.0,
            salaries=85000.0,
            temp_wages=45000.0,
        ),
    )
    return [sample_record, record2]


class TestRecordsToDataFrame:
    """Tests for records_to_dataframe function."""

    def test_empty_records(self) -> None:
        """Test with empty list returns empty DataFrame."""
        df = records_to_dataframe([])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_basic_columns(self, sample_records: list[FullHRRecord]) -> None:
        """Test basic record columns are present."""
        df = records_to_dataframe(sample_records)

        assert "id" in df.columns
        assert "entity" in df.columns
        assert "year" in df.columns
        assert "month" in df.columns
        assert "status" in df.columns

    def test_flattened_workforce_columns(self, sample_records: list[FullHRRecord]) -> None:
        """Test workforce columns are flattened."""
        df = records_to_dataframe(sample_records, flatten=True)

        assert "bc_male" in df.columns
        assert "bc_female" in df.columns
        assert "wc_male" in df.columns
        assert "wc_female" in df.columns

    def test_flattened_capacity_columns(self, sample_records: list[FullHRRecord]) -> None:
        """Test capacity columns are flattened."""
        df = records_to_dataframe(sample_records, flatten=True)

        assert "fte_blue_collar" in df.columns
        assert "fte_white_collar" in df.columns
        assert "external_hours_blue" in df.columns

    def test_derived_columns(self, sample_records: list[FullHRRecord]) -> None:
        """Test derived columns are calculated."""
        df = records_to_dataframe(sample_records, flatten=True)

        assert "total_headcount" in df.columns
        assert "blue_collar_total" in df.columns
        assert "white_collar_total" in df.columns
        assert "total_internal_fte" in df.columns
        assert "total_costs" in df.columns

    def test_total_headcount_calculation(self, sample_records: list[FullHRRecord]) -> None:
        """Test total headcount is calculated correctly."""
        df = records_to_dataframe(sample_records, flatten=True)

        # First record: bc_male=20, bc_female=2, wc_male=10, wc_female=8 = 40
        bvd_row = df[df["entity"] == "BVD"].iloc[0]
        assert bvd_row["total_headcount"] == 40

    def test_not_flattened(self, sample_records: list[FullHRRecord]) -> None:
        """Test non-flattened mode keeps nested dicts."""
        df = records_to_dataframe(sample_records, flatten=False)

        assert "workforce" in df.columns
        assert "capacity" in df.columns
        assert isinstance(df.iloc[0]["workforce"], dict)

    def test_exclude_nested(self, sample_records: list[FullHRRecord]) -> None:
        """Test excluding nested data."""
        df = records_to_dataframe(sample_records, include_nested=False)

        assert "bc_male" not in df.columns
        assert "fte_blue_collar" not in df.columns
        assert "total_headcount" not in df.columns

    def test_row_count(self, sample_records: list[FullHRRecord]) -> None:
        """Test correct number of rows."""
        df = records_to_dataframe(sample_records)
        assert len(df) == 2


class TestTrendsToDataFrame:
    """Tests for trends_to_dataframe function."""

    @pytest.fixture
    def sample_trends(self) -> list[TrendDataPoint]:
        """Create sample trend data."""
        return [
            TrendDataPoint(
                year=2025,
                month=1,
                entity="BVD",
                headcount=40,
                blue_collar=22,
                white_collar=18,
                internal_fte=34.2,
                external_fte=7.8,
                sick_days=7,
                working_days=21,
                sick_rate=0.83,
                turnover=1,
                reviews_completed=14,
                wages=71333.95,
                salaries=93244.14,
                temp_wages=58592.64,
            ),
            TrendDataPoint(
                year=2025,
                month=2,
                entity="BVD",
                headcount=42,
                blue_collar=24,
                white_collar=18,
                internal_fte=36.0,
                external_fte=8.0,
                sick_days=5,
                working_days=20,
                sick_rate=0.60,
                turnover=0,
                reviews_completed=16,
                wages=73000.0,
                salaries=95000.0,
                temp_wages=60000.0,
            ),
        ]

    def test_empty_trends(self) -> None:
        """Test with empty list returns empty DataFrame."""
        df = trends_to_dataframe([])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_basic_columns(self, sample_trends: list[TrendDataPoint]) -> None:
        """Test basic trend columns are present."""
        df = trends_to_dataframe(sample_trends)

        assert "year" in df.columns
        assert "month" in df.columns
        assert "entity" in df.columns
        assert "headcount" in df.columns

    def test_period_column(self, sample_trends: list[TrendDataPoint]) -> None:
        """Test period column is generated."""
        df = trends_to_dataframe(sample_trends, include_period_column=True)

        assert "period" in df.columns
        assert df.iloc[0]["period"] == "2025-01"
        assert df.iloc[1]["period"] == "2025-02"

    def test_no_period_column(self, sample_trends: list[TrendDataPoint]) -> None:
        """Test period column can be excluded."""
        df = trends_to_dataframe(sample_trends, include_period_column=False)

        assert "period" not in df.columns

    def test_period_first_column(self, sample_trends: list[TrendDataPoint]) -> None:
        """Test period is the first column when included."""
        df = trends_to_dataframe(sample_trends, include_period_column=True)

        assert df.columns[0] == "period"


class TestEntityBreakdownToDataFrame:
    """Tests for entity_breakdown_to_dataframe function."""

    @pytest.fixture
    def sample_breakdown(self) -> list[EntityBreakdown]:
        """Create sample entity breakdown."""
        return [
            EntityBreakdown(
                entity="BVD",
                record_count=12,
                total_headcount=480,
                blue_collar=264,
                white_collar=216,
            ),
            EntityBreakdown(
                entity="VHH",
                record_count=12,
                total_headcount=360,
                blue_collar=180,
                white_collar=180,
            ),
        ]

    def test_empty_breakdown(self) -> None:
        """Test with empty list returns empty DataFrame."""
        df = entity_breakdown_to_dataframe([])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_indexed_by_entity(self, sample_breakdown: list[EntityBreakdown]) -> None:
        """Test DataFrame is indexed by entity."""
        df = entity_breakdown_to_dataframe(sample_breakdown)

        assert df.index.name == "entity"
        assert "BVD" in df.index
        assert "VHH" in df.index

    def test_values_accessible_by_entity(
        self, sample_breakdown: list[EntityBreakdown]
    ) -> None:
        """Test values can be accessed by entity index."""
        df = entity_breakdown_to_dataframe(sample_breakdown)

        assert df.loc["BVD", "total_headcount"] == 480
        assert df.loc["VHH", "blue_collar"] == 180


class TestSummaryToSeries:
    """Tests for summary_to_series function."""

    @pytest.fixture
    def sample_summary(self) -> AnalyticsSummary:
        """Create sample analytics summary."""
        return AnalyticsSummary(
            record_count=12,
            total_headcount=480,
            blue_collar_total=264,
            white_collar_total=216,
            total_internal_fte=410.4,
            total_external_fte=93.6,
            total_sick_days=84,
            total_costs=2678048.76,
            total_turnover=5,
            total_reviews_completed=168,
        )

    def test_returns_series(self, sample_summary: AnalyticsSummary) -> None:
        """Test returns pandas Series."""
        series = summary_to_series(sample_summary)
        assert isinstance(series, pd.Series)

    def test_series_name(self, sample_summary: AnalyticsSummary) -> None:
        """Test series has correct name."""
        series = summary_to_series(sample_summary)
        assert series.name == "summary"

    def test_series_values(self, sample_summary: AnalyticsSummary) -> None:
        """Test series contains expected values."""
        series = summary_to_series(sample_summary)

        assert series["record_count"] == 12
        assert series["total_headcount"] == 480
        assert series["total_costs"] == 2678048.76
