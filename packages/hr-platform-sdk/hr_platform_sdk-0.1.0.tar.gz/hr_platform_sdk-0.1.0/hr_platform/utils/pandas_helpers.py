"""pandas integration helpers.

Functions to convert HR Platform API responses to pandas DataFrames
for data analysis and visualization.

Example:
    >>> from hr_platform import HRPlatformClient
    >>> from hr_platform.utils.pandas_helpers import records_to_dataframe
    >>>
    >>> client = HRPlatformClient.with_api_key("hrp_live_xxx...")
    >>> records = client.records.list()
    >>> df = records_to_dataframe(records)
    >>> print(df.groupby("entity")["total_headcount"].sum())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None  # type: ignore

if TYPE_CHECKING:
    from hr_platform.models.analytics import EntityBreakdown, TrendDataPoint
    from hr_platform.models.records import FullHRRecord


def _check_pandas() -> None:
    """Check if pandas is available.

    Raises:
        ImportError: If pandas is not installed.
    """
    if not PANDAS_AVAILABLE:
        raise ImportError(
            "pandas is required for DataFrame conversion. "
            "Install it with: pip install hr-platform-sdk[pandas]"
        )


def records_to_dataframe(
    records: list["FullHRRecord"],
    *,
    flatten: bool = True,
    include_nested: bool = True,
) -> "pd.DataFrame":
    """Convert HR records to a pandas DataFrame.

    Flattens the nested record structure (workforce, capacity, absences,
    turnover, performance, financials) into a single row per record.

    Args:
        records: List of FullHRRecord instances from client.records.list().
        flatten: If True, flatten nested objects into columns. If False,
            keep nested objects as dictionary columns.
        include_nested: If True, include all nested data. If False, only
            include top-level record fields.

    Returns:
        pandas DataFrame with one row per record.

    Example:
        >>> records = client.records.list()
        >>> df = records_to_dataframe(records)
        >>> df.columns
        Index(['id', 'entity', 'year', 'month', 'working_days', 'status',
               'bc_male', 'bc_female', 'wc_male', 'wc_female', ...])
        >>> df.groupby("entity")["bc_male"].sum()
        entity
        BVD    240
        VHH    180
        VHO    120
    """
    _check_pandas()

    if not records:
        return pd.DataFrame()

    rows: list[dict[str, Any]] = []

    for record in records:
        row: dict[str, Any] = {
            "id": record.id,
            "entity": record.entity,
            "year": record.year,
            "month": record.month,
            "working_days": record.working_days,
            "status": record.status,
            "submitted_by": record.submitted_by,
            "submitted_at": record.submitted_at,
            "approved_by": record.approved_by,
            "approved_at": record.approved_at,
            "rejected_reason": record.rejected_reason,
            "created_at": record.created_at,
            "updated_at": record.updated_at,
        }

        if include_nested:
            if flatten:
                # Flatten workforce
                if record.workforce:
                    row.update(
                        {
                            "bc_male": record.workforce.bc_male,
                            "bc_female": record.workforce.bc_female,
                            "bc_age_under_20": record.workforce.bc_age_under_20,
                            "bc_age_20_29": record.workforce.bc_age_20_29,
                            "bc_age_30_39": record.workforce.bc_age_30_39,
                            "bc_age_40_49": record.workforce.bc_age_40_49,
                            "bc_age_50_59": record.workforce.bc_age_50_59,
                            "bc_age_60_plus": record.workforce.bc_age_60_plus,
                            "bc_ausgesteuert": record.workforce.bc_ausgesteuert,
                            "wc_male": record.workforce.wc_male,
                            "wc_female": record.workforce.wc_female,
                            "wc_age_under_20": record.workforce.wc_age_under_20,
                            "wc_age_20_29": record.workforce.wc_age_20_29,
                            "wc_age_30_39": record.workforce.wc_age_30_39,
                            "wc_age_40_49": record.workforce.wc_age_40_49,
                            "wc_age_50_59": record.workforce.wc_age_50_59,
                            "wc_age_60_plus": record.workforce.wc_age_60_plus,
                            "wc_ausgesteuert": record.workforce.wc_ausgesteuert,
                        }
                    )

                # Flatten capacity
                if record.capacity:
                    row.update(
                        {
                            "fte_blue_collar": record.capacity.fte_blue_collar,
                            "fte_white_collar": record.capacity.fte_white_collar,
                            "fte_overhead": record.capacity.fte_overhead,
                            "external_hours_blue": record.capacity.external_hours_blue,
                            "external_hours_white": record.capacity.external_hours_white,
                            "overtime_hours_blue": record.capacity.overtime_hours_blue,
                            "overtime_hours_white": record.capacity.overtime_hours_white,
                        }
                    )

                # Flatten absences
                if record.absences:
                    row.update(
                        {
                            "sick_days_blue": record.absences.sick_days_blue,
                            "sick_days_white": record.absences.sick_days_white,
                            "long_term_sick_fte": record.absences.long_term_sick_fte,
                            "vacation_hours_blue": record.absences.vacation_hours_blue,
                            "vacation_hours_white": record.absences.vacation_hours_white,
                            "maternity_fte": record.absences.maternity_fte,
                            "parental_fte": record.absences.parental_fte,
                        }
                    )

                # Flatten turnover
                if record.turnover:
                    row.update(
                        {
                            "voluntary_bc": record.turnover.voluntary_bc,
                            "voluntary_wc": record.turnover.voluntary_wc,
                            "involuntary_bc": record.turnover.involuntary_bc,
                            "involuntary_wc": record.turnover.involuntary_wc,
                        }
                    )

                # Flatten performance
                if record.performance:
                    row.update(
                        {
                            "year_reviews_blue": record.performance.year_reviews_blue,
                            "year_reviews_white": record.performance.year_reviews_white,
                        }
                    )

                # Flatten financials
                if record.financials:
                    row.update(
                        {
                            "wages": record.financials.wages,
                            "salaries": record.financials.salaries,
                            "temp_wages": record.financials.temp_wages,
                        }
                    )
            else:
                # Keep as dictionaries
                row["workforce"] = (
                    record.workforce.model_dump() if record.workforce else None
                )
                row["capacity"] = (
                    record.capacity.model_dump() if record.capacity else None
                )
                row["absences"] = (
                    record.absences.model_dump() if record.absences else None
                )
                row["turnover"] = (
                    record.turnover.model_dump() if record.turnover else None
                )
                row["performance"] = (
                    record.performance.model_dump() if record.performance else None
                )
                row["financials"] = (
                    record.financials.model_dump() if record.financials else None
                )

        rows.append(row)

    df = pd.DataFrame(rows)

    # Calculate derived columns if flattened
    if flatten and include_nested:
        # Total headcount
        if "bc_male" in df.columns and "wc_male" in df.columns:
            df["total_headcount"] = (
                df["bc_male"].fillna(0)
                + df["bc_female"].fillna(0)
                + df["wc_male"].fillna(0)
                + df["wc_female"].fillna(0)
            )
            df["blue_collar_total"] = df["bc_male"].fillna(0) + df["bc_female"].fillna(
                0
            )
            df["white_collar_total"] = df["wc_male"].fillna(0) + df["wc_female"].fillna(
                0
            )

        # Total FTE
        if "fte_blue_collar" in df.columns:
            df["total_internal_fte"] = (
                df["fte_blue_collar"].fillna(0)
                + df["fte_white_collar"].fillna(0)
                + df["fte_overhead"].fillna(0)
            )

        # External FTE (hours / 173)
        if "external_hours_blue" in df.columns:
            df["external_fte_blue"] = df["external_hours_blue"].fillna(0) / 173
            df["external_fte_white"] = df["external_hours_white"].fillna(0) / 173
            df["total_external_fte"] = df["external_fte_blue"] + df["external_fte_white"]

        # Total costs
        if "wages" in df.columns:
            df["total_costs"] = (
                df["wages"].fillna(0)
                + df["salaries"].fillna(0)
                + df["temp_wages"].fillna(0)
            )

        # Total turnover
        if "voluntary_bc" in df.columns:
            df["total_turnover"] = (
                df["voluntary_bc"].fillna(0)
                + df["voluntary_wc"].fillna(0)
                + df["involuntary_bc"].fillna(0)
                + df["involuntary_wc"].fillna(0)
            )

        # Total sick days
        if "sick_days_blue" in df.columns:
            df["total_sick_days"] = df["sick_days_blue"].fillna(0) + df[
                "sick_days_white"
            ].fillna(0)

    return df


def trends_to_dataframe(
    trends: list["TrendDataPoint"],
    *,
    include_period_column: bool = True,
) -> "pd.DataFrame":
    """Convert trend data to a pandas DataFrame.

    Args:
        trends: List of TrendDataPoint instances from client.analytics.get_trends().
        include_period_column: If True, add a combined 'period' column (YYYY-MM).

    Returns:
        pandas DataFrame with one row per trend data point.

    Example:
        >>> trends = client.analytics.get_trends()
        >>> df = trends_to_dataframe(trends)
        >>> df.pivot(index="period", columns="entity", values="headcount")
    """
    _check_pandas()

    if not trends:
        return pd.DataFrame()

    rows: list[dict[str, Any]] = []

    for trend in trends:
        row = {
            "year": trend.year,
            "month": trend.month,
            "entity": trend.entity,
            "headcount": trend.headcount,
            "blue_collar": trend.blue_collar,
            "white_collar": trend.white_collar,
            "internal_fte": trend.internal_fte,
            "external_fte": trend.external_fte,
            "sick_days": trend.sick_days,
            "working_days": trend.working_days,
            "sick_rate": trend.sick_rate,
            "turnover": trend.turnover,
            "reviews_completed": trend.reviews_completed,
            "wages": trend.wages,
            "salaries": trend.salaries,
            "temp_wages": trend.temp_wages,
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    if include_period_column:
        df["period"] = df.apply(
            lambda r: f"{int(r['year'])}-{int(r['month']):02d}", axis=1
        )
        # Reorder to put period first
        cols = ["period"] + [c for c in df.columns if c != "period"]
        df = df[cols]

    return df


def entity_breakdown_to_dataframe(
    breakdown: list["EntityBreakdown"],
) -> "pd.DataFrame":
    """Convert entity breakdown data to a pandas DataFrame.

    Args:
        breakdown: List of EntityBreakdown instances from
            client.analytics.get_by_entity().

    Returns:
        pandas DataFrame indexed by entity.

    Example:
        >>> breakdown = client.analytics.get_by_entity()
        >>> df = entity_breakdown_to_dataframe(breakdown)
        >>> df.loc["BVD", "total_headcount"]
    """
    _check_pandas()

    if not breakdown:
        return pd.DataFrame()

    rows: list[dict[str, Any]] = []

    for entity_data in breakdown:
        row = {
            "entity": entity_data.entity,
            "record_count": entity_data.record_count,
            "total_headcount": entity_data.total_headcount,
            "blue_collar": entity_data.blue_collar,
            "white_collar": entity_data.white_collar,
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.set_index("entity")

    return df


def summary_to_series(summary: Any) -> "pd.Series":
    """Convert analytics summary to a pandas Series.

    Args:
        summary: AnalyticsSummary instance from client.analytics.get_summary().

    Returns:
        pandas Series with summary metrics.

    Example:
        >>> summary = client.analytics.get_summary()
        >>> series = summary_to_series(summary)
        >>> print(series["total_headcount"])
    """
    _check_pandas()

    data = {
        "record_count": summary.record_count,
        "total_headcount": summary.total_headcount,
        "blue_collar_total": summary.blue_collar_total,
        "white_collar_total": summary.white_collar_total,
        "total_internal_fte": summary.total_internal_fte,
        "total_external_fte": summary.total_external_fte,
        "total_sick_days": summary.total_sick_days,
        "total_costs": summary.total_costs,
        "total_turnover": summary.total_turnover,
        "total_reviews_completed": summary.total_reviews_completed,
    }

    return pd.Series(data, name="summary")
