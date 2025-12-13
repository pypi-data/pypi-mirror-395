#!/usr/bin/env python3
"""pandas integration example for HR Platform SDK.

This example demonstrates:
- Converting records to DataFrames with flattened columns
- Converting trends to DataFrames with period column
- Entity breakdown as indexed DataFrame
- Summary as pandas Series
- Data analysis and visualization examples

Run with:
    pip install hr-platform-sdk[pandas]
    python examples/pandas_integration.py
"""

from __future__ import annotations

import os

# Check pandas is installed
try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas is required for this example.")
    print("Install with: pip install hr-platform-sdk[pandas]")
    raise SystemExit(1)

from hr_platform import HRPlatformClient
from hr_platform.utils import (
    entity_breakdown_to_dataframe,
    records_to_dataframe,
    summary_to_series,
    trends_to_dataframe,
)


def main() -> None:
    """Demonstrate pandas integration."""
    api_key = os.environ.get("HR_PLATFORM_API_KEY", "hrp_test_demo_key")
    base_url = os.environ.get("HR_PLATFORM_URL", "http://localhost:4000")

    client = HRPlatformClient.with_api_key(api_key, base_url=base_url)

    with client:
        # ============================================================
        # 1. RECORDS TO DATAFRAME
        # ============================================================
        print("=" * 60)
        print("1. RECORDS TO DATAFRAME")
        print("=" * 60)

        records = client.records.list()
        print(f"Fetched {len(records)} records")

        # Convert to DataFrame with flattened nested data
        df_records = records_to_dataframe(records, flatten=True)
        print(f"\nDataFrame shape: {df_records.shape}")
        print(f"Columns: {list(df_records.columns[:10])}... ({len(df_records.columns)} total)")

        # Show first few rows
        print("\nFirst 3 rows (selected columns):")
        cols = ["entity", "year", "month", "status", "total_headcount"]
        available_cols = [c for c in cols if c in df_records.columns]
        if available_cols:
            print(df_records[available_cols].head(3).to_string())

        # ============================================================
        # 2. ANALYZING RECORDS DATA
        # ============================================================
        print("\n" + "=" * 60)
        print("2. ANALYZING RECORDS DATA")
        print("=" * 60)

        if not df_records.empty and "total_headcount" in df_records.columns:
            # Group by entity
            print("\nHeadcount by Entity:")
            entity_stats = df_records.groupby("entity")["total_headcount"].agg(
                ["mean", "min", "max", "count"]
            )
            print(entity_stats.to_string())

            # Group by status
            print("\nRecords by Status:")
            status_counts = df_records["status"].value_counts()
            print(status_counts.to_string())

            # Monthly totals
            if "year" in df_records.columns and "month" in df_records.columns:
                print("\nTotal Headcount by Month (2025):")
                monthly = (
                    df_records[df_records["year"] == 2025]
                    .groupby("month")["total_headcount"]
                    .sum()
                )
                print(monthly.to_string())

        # ============================================================
        # 3. TRENDS TO DATAFRAME
        # ============================================================
        print("\n" + "=" * 60)
        print("3. TRENDS TO DATAFRAME")
        print("=" * 60)

        trends = client.analytics.get_trends()
        print(f"Fetched {len(trends)} trend data points")

        # Convert with period column (e.g., "2025-01")
        df_trends = trends_to_dataframe(trends, include_period=True)
        print(f"\nDataFrame shape: {df_trends.shape}")

        if not df_trends.empty:
            # Show first few rows
            print("\nFirst 5 rows:")
            cols = ["period", "entity", "headcount", "sick_rate", "turnover"]
            available_cols = [c for c in cols if c in df_trends.columns]
            if available_cols:
                print(df_trends[available_cols].head(5).to_string())

            # Pivot table: sick rate by entity over time
            if "period" in df_trends.columns and "sick_rate" in df_trends.columns:
                print("\nSick Rate by Entity (Pivot):")
                pivot = df_trends.pivot_table(
                    values="sick_rate",
                    index="period",
                    columns="entity",
                    aggfunc="mean",
                )
                print(pivot.head().to_string())

        # ============================================================
        # 4. ENTITY BREAKDOWN TO INDEXED DATAFRAME
        # ============================================================
        print("\n" + "=" * 60)
        print("4. ENTITY BREAKDOWN (INDEXED)")
        print("=" * 60)

        breakdown = client.analytics.get_by_entity()
        print(f"Fetched {len(breakdown)} entity summaries")

        # Convert with entity as index
        df_breakdown = entity_breakdown_to_dataframe(breakdown)
        print(f"\nDataFrame shape: {df_breakdown.shape}")
        print(f"Index: {list(df_breakdown.index)}")

        print("\nEntity Breakdown:")
        print(df_breakdown.to_string())

        # Access specific entity data
        if "BVD" in df_breakdown.index:
            print(f"\nBVD Details:")
            print(f"  Total Headcount: {df_breakdown.loc['BVD', 'total_headcount']}")
            print(f"  Blue Collar: {df_breakdown.loc['BVD', 'blue_collar']}")
            print(f"  White Collar: {df_breakdown.loc['BVD', 'white_collar']}")

        # ============================================================
        # 5. SUMMARY TO SERIES
        # ============================================================
        print("\n" + "=" * 60)
        print("5. SUMMARY TO SERIES")
        print("=" * 60)

        summary = client.analytics.get_summary()
        print("Fetched analytics summary")

        # Convert to Series
        series = summary_to_series(summary)
        print(f"\nSeries length: {len(series)}")
        print(f"Series name: {series.name}")

        print("\nSummary Metrics:")
        print(series.to_string())

        # Compare summaries across entities
        print("\nComparing Entities:")
        bvd_series = summary_to_series(
            client.analytics.get_summary(entity="BVD"), name="BVD"
        )
        vhh_series = summary_to_series(
            client.analytics.get_summary(entity="VHH"), name="VHH"
        )

        comparison = pd.DataFrame({"BVD": bvd_series, "VHH": vhh_series})
        comparison["Diff"] = comparison["BVD"] - comparison["VHH"]
        print(comparison.to_string())

        # ============================================================
        # 6. EXPORTING TO CSV
        # ============================================================
        print("\n" + "=" * 60)
        print("6. EXPORT EXAMPLES")
        print("=" * 60)

        print("\nExport to CSV (German Excel format):")
        print("""
        # German format: semicolon delimiter, comma decimal
        df_records.to_csv(
            "records.csv",
            sep=";",
            decimal=",",
            index=False,
            encoding="utf-8-sig",  # BOM for Excel
        )
        """)

        print("Export to Excel with multiple sheets:")
        print("""
        with pd.ExcelWriter("hr_report.xlsx") as writer:
            df_records.to_excel(writer, sheet_name="Records")
            df_trends.to_excel(writer, sheet_name="Trends")
            df_breakdown.to_excel(writer, sheet_name="Entities")
        """)

        # ============================================================
        # 7. VISUALIZATION EXAMPLES (matplotlib required)
        # ============================================================
        print("\n" + "=" * 60)
        print("7. VISUALIZATION EXAMPLES")
        print("=" * 60)

        print("""
        # pip install matplotlib

        import matplotlib.pyplot as plt

        # Headcount trend by entity
        pivot = df_trends.pivot(index="period", columns="entity", values="headcount")
        pivot.plot(kind="line", marker="o", figsize=(10, 6))
        plt.title("Headcount Trend by Entity")
        plt.ylabel("Headcount")
        plt.legend(title="Entity")
        plt.tight_layout()
        plt.savefig("headcount_trend.png")

        # Sick rate comparison
        df_trends.boxplot(column="sick_rate", by="entity", figsize=(8, 5))
        plt.title("Sick Rate Distribution by Entity")
        plt.suptitle("")
        plt.ylabel("Sick Rate (%)")
        plt.savefig("sick_rate_box.png")

        # Entity breakdown pie chart
        df_breakdown["total_headcount"].plot(
            kind="pie",
            autopct="%1.1f%%",
            figsize=(8, 8),
        )
        plt.title("Headcount Distribution by Entity")
        plt.ylabel("")
        plt.savefig("entity_pie.png")
        """)

    print("\n" + "=" * 60)
    print("pandas integration examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
