#!/usr/bin/env python3
"""Async usage example for HR Platform SDK.

This example demonstrates:
- Creating an async client
- Concurrent API requests with asyncio.gather
- Async context manager usage
- Async iteration patterns

Run with:
    python examples/async_usage.py
"""

from __future__ import annotations

import asyncio
import os
import time

from hr_platform import AsyncHRPlatformClient


async def main() -> None:
    """Demonstrate async SDK usage."""
    api_key = os.environ.get("HR_PLATFORM_API_KEY", "hrp_test_demo_key")
    base_url = os.environ.get("HR_PLATFORM_URL", "http://localhost:4000")

    # Create async client
    client = AsyncHRPlatformClient.with_api_key(
        api_key,
        base_url=base_url,
        timeout=30.0,
    )

    async with client:
        # ============================================================
        # 1. SEQUENTIAL REQUESTS (for comparison)
        # ============================================================
        print("=" * 60)
        print("1. SEQUENTIAL REQUESTS")
        print("=" * 60)

        start = time.perf_counter()

        records = await client.records.list()
        summary = await client.analytics.get_summary()
        trends = await client.analytics.get_trends()
        breakdown = await client.analytics.get_by_entity()

        sequential_time = time.perf_counter() - start
        print(f"Sequential requests completed in {sequential_time:.3f}s")
        print(f"  Records: {len(records)}")
        print(f"  Summary headcount: {summary.total_headcount}")
        print(f"  Trends: {len(trends)} data points")
        print(f"  Breakdown: {len(breakdown)} entities")

        # ============================================================
        # 2. CONCURRENT REQUESTS (faster!)
        # ============================================================
        print("\n" + "=" * 60)
        print("2. CONCURRENT REQUESTS")
        print("=" * 60)

        start = time.perf_counter()

        # Run all requests concurrently using asyncio.gather
        (
            records,
            summary,
            trends,
            breakdown,
            bvd_summary,
            vhh_summary,
        ) = await asyncio.gather(
            client.records.list(),
            client.analytics.get_summary(),
            client.analytics.get_trends(),
            client.analytics.get_by_entity(),
            client.analytics.get_summary(entity="BVD"),
            client.analytics.get_summary(entity="VHH"),
        )

        concurrent_time = time.perf_counter() - start
        print(f"Concurrent requests completed in {concurrent_time:.3f}s")
        print(f"  Speedup: {sequential_time / concurrent_time:.1f}x faster")
        print(f"  Records: {len(records)}")
        print(f"  BVD headcount: {bvd_summary.total_headcount}")
        print(f"  VHH headcount: {vhh_summary.total_headcount}")

        # ============================================================
        # 3. FETCH MULTIPLE RECORDS CONCURRENTLY
        # ============================================================
        print("\n" + "=" * 60)
        print("3. FETCH MULTIPLE RECORDS CONCURRENTLY")
        print("=" * 60)

        if len(records) >= 3:
            record_ids = [r.id for r in records[:3]]

            start = time.perf_counter()

            # Fetch multiple records concurrently
            detailed_records = await asyncio.gather(
                *[client.records.get(rid) for rid in record_ids]
            )

            fetch_time = time.perf_counter() - start
            print(f"Fetched {len(detailed_records)} records in {fetch_time:.3f}s")

            for record in detailed_records:
                print(f"  {record.id[:8]}... - {record.entity} "
                      f"{record.month}/{record.year} [{record.status}]")

        # ============================================================
        # 4. FETCH ALL ENTITY SUMMARIES CONCURRENTLY
        # ============================================================
        print("\n" + "=" * 60)
        print("4. ALL ENTITY SUMMARIES (CONCURRENT)")
        print("=" * 60)

        entities = ["BVD", "VHH", "VHO", "All"]

        start = time.perf_counter()

        summaries = await asyncio.gather(
            *[client.analytics.get_summary(entity=e) for e in entities]
        )

        summary_time = time.perf_counter() - start
        print(f"Fetched {len(summaries)} summaries in {summary_time:.3f}s")

        for entity, summary in zip(entities, summaries):
            print(f"  {entity}: {summary.total_headcount} headcount, "
                  f"{summary.record_count} records")

        # ============================================================
        # 5. ERROR HANDLING IN CONCURRENT REQUESTS
        # ============================================================
        print("\n" + "=" * 60)
        print("5. CONCURRENT REQUESTS WITH ERROR HANDLING")
        print("=" * 60)

        # Use return_exceptions=True to handle errors gracefully
        results = await asyncio.gather(
            client.records.list(entity="BVD"),
            client.records.list(entity="VHH"),
            client.analytics.get_summary(),
            return_exceptions=True,  # Don't fail on first error
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"  Request {i}: FAILED - {type(result).__name__}: {result}")
            else:
                print(f"  Request {i}: SUCCESS - {type(result).__name__}")

    print("\n" + "=" * 60)
    print("Done! Async client automatically closed.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
