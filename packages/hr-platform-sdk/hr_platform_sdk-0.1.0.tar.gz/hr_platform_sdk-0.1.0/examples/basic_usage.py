#!/usr/bin/env python3
"""Basic usage example for HR Platform SDK.

This example demonstrates:
- Creating a client with API key authentication
- Fetching records with filters
- Getting analytics summaries
- Creating and updating records
- Workflow operations (submit, approve, reject)

Run with:
    python examples/basic_usage.py
"""

from __future__ import annotations

import os

from hr_platform import HRPlatformClient
from hr_platform.core.config import RetryConfig


def main() -> None:
    """Demonstrate basic SDK usage."""
    # Get API key from environment
    api_key = os.environ.get("HR_PLATFORM_API_KEY", "hrp_test_demo_key")
    base_url = os.environ.get("HR_PLATFORM_URL", "http://localhost:4000")

    # Create client with API key authentication
    # The SDK uses httpx for HTTP requests with automatic retry logic
    client = HRPlatformClient.with_api_key(
        api_key,
        base_url=base_url,
        timeout=30.0,
        retry=RetryConfig(
            max_retries=3,
            initial_delay=1.0,
            backoff_multiplier=2.0,
        ),
    )

    # Use context manager for automatic cleanup
    with client:
        # ============================================================
        # 1. LIST RECORDS
        # ============================================================
        print("=" * 60)
        print("1. LISTING RECORDS")
        print("=" * 60)

        # Get all records
        all_records = client.records.list()
        print(f"Total records: {len(all_records)}")

        # Filter by entity
        bvd_records = client.records.list(entity="BVD")
        print(f"BVD records: {len(bvd_records)}")

        # Filter by year and month
        recent_records = client.records.list(year="2025", month="12")
        print(f"December 2025 records: {len(recent_records)}")

        # Combined filters
        filtered_records = client.records.list(entity="BVD", year="2025")
        print(f"BVD 2025 records: {len(filtered_records)}")

        # ============================================================
        # 2. GET SINGLE RECORD
        # ============================================================
        print("\n" + "=" * 60)
        print("2. GET SINGLE RECORD")
        print("=" * 60)

        if all_records:
            record = client.records.get(all_records[0].id)
            print(f"Record ID: {record.id}")
            print(f"Entity: {record.entity}")
            print(f"Period: {record.month}/{record.year}")
            print(f"Status: {record.status}")

            # Access nested data
            if record.workforce:
                total_headcount = (
                    record.workforce.bc_male
                    + record.workforce.bc_female
                    + record.workforce.wc_male
                    + record.workforce.wc_female
                )
                print(f"Total Headcount: {total_headcount}")

            if record.financials:
                total_costs = (
                    record.financials.wages
                    + record.financials.salaries
                    + record.financials.temp_wages
                )
                print(f"Total Costs: EUR {total_costs:,.2f}")

        # ============================================================
        # 3. ANALYTICS
        # ============================================================
        print("\n" + "=" * 60)
        print("3. ANALYTICS")
        print("=" * 60)

        # Get overall summary
        summary = client.analytics.get_summary()
        print(f"Records analyzed: {summary.record_count}")
        print(f"Total Headcount: {summary.total_headcount}")
        print(f"Blue Collar: {summary.blue_collar_total}")
        print(f"White Collar: {summary.white_collar_total}")
        print(f"Total FTE: {summary.total_internal_fte + summary.total_external_fte:.1f}")
        print(f"Total Costs: EUR {summary.total_costs:,.2f}")

        # Summary for specific entity
        bvd_summary = client.analytics.get_summary(entity="BVD")
        print(f"\nBVD Summary:")
        print(f"  Headcount: {bvd_summary.total_headcount}")
        print(f"  Records: {bvd_summary.record_count}")

        # Get trends over time
        trends = client.analytics.get_trends(entity="BVD")
        print(f"\nBVD Trends: {len(trends)} data points")
        for trend in trends[:3]:  # Show first 3
            print(f"  {trend.month}/{trend.year}: Headcount={trend.headcount}, "
                  f"Sick Rate={trend.sick_rate:.2f}%")

        # Entity breakdown
        breakdown = client.analytics.get_by_entity()
        print(f"\nEntity Breakdown:")
        for entity in breakdown:
            print(f"  {entity.entity}: {entity.total_headcount} employees, "
                  f"{entity.record_count} records")

        # ============================================================
        # 4. USER INFO
        # ============================================================
        print("\n" + "=" * 60)
        print("4. USER INFO")
        print("=" * 60)

        profile = client.users.get_profile()
        print(f"Current User: {profile.name}")
        print(f"Email: {profile.email}")
        print(f"Role: {profile.role}")
        if profile.entity:
            print(f"Entity: {profile.entity}")

        # Get password policy
        policy = client.users.get_password_policy()
        print(f"\nPassword Policy:")
        print(f"  Min Length: {policy.policy.min_length}")
        print(f"  Requires: uppercase={policy.policy.require_uppercase}, "
              f"lowercase={policy.policy.require_lowercase}, "
              f"numbers={policy.policy.require_numbers}, "
              f"special={policy.policy.require_special_chars}")

    print("\n" + "=" * 60)
    print("Done! Client automatically closed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
