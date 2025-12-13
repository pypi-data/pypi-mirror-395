#!/usr/bin/env python3
"""Error handling example for HR Platform SDK.

This example demonstrates:
- Catching specific exception types
- Handling rate limits with retry logic
- Validation error field access
- Network and timeout error handling
- Using the base exception class

Run with:
    python examples/error_handling.py
"""

from __future__ import annotations

import os
import sys

from hr_platform import HRPlatformClient
from hr_platform.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    HRPlatformError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)


def main() -> None:
    """Demonstrate error handling patterns."""
    api_key = os.environ.get("HR_PLATFORM_API_KEY", "hrp_test_demo_key")
    base_url = os.environ.get("HR_PLATFORM_URL", "http://localhost:4000")

    client = HRPlatformClient.with_api_key(api_key, base_url=base_url)

    with client:
        # ============================================================
        # 1. CATCHING SPECIFIC EXCEPTION TYPES
        # ============================================================
        print("=" * 60)
        print("1. SPECIFIC EXCEPTION HANDLING")
        print("=" * 60)

        # Example: Fetching a non-existent record
        try:
            record = client.records.get("non-existent-uuid-12345")
            print(f"Found record: {record.id}")
        except NotFoundError as e:
            print(f"NotFoundError: {e.message}")
            print(f"  Status code: {e.status}")
            print(f"  Error code: {e.code}")
            if e.resource_type:
                print(f"  Resource type: {e.resource_type}")
            if e.resource_id:
                print(f"  Resource ID: {e.resource_id}")

        # ============================================================
        # 2. VALIDATION ERRORS WITH FIELD DETAILS
        # ============================================================
        print("\n" + "=" * 60)
        print("2. VALIDATION ERROR HANDLING")
        print("=" * 60)

        # This would be a validation error if entity is invalid
        # Simulating what a validation error looks like
        validation_error = ValidationError(
            "Validation failed",
            fields=[
                {"field": "entity", "message": "Invalid enum value"},
                {"field": "year", "message": "Must be between 2020 and 2100"},
            ],
        )
        print(f"ValidationError example:")
        print(f"  Message: {validation_error.message}")
        print(f"  Status: {validation_error.status}")
        print(f"  Fields with errors:")
        for field in validation_error.fields:
            print(f"    - {field['field']}: {field['message']}")

        # ============================================================
        # 3. RATE LIMIT HANDLING
        # ============================================================
        print("\n" + "=" * 60)
        print("3. RATE LIMIT HANDLING")
        print("=" * 60)

        # Simulating rate limit error (SDK has built-in retry)
        rate_limit_error = RateLimitError(retry_after=60)
        print(f"RateLimitError example:")
        print(f"  Message: {rate_limit_error.message}")
        print(f"  Status: {rate_limit_error.status}")
        print(f"  Retry after: {rate_limit_error.retry_after} seconds")
        print(f"  Error code: {rate_limit_error.code}")

        # Real handling pattern:
        print("\n  Handling pattern:")
        print("""
        import time
        try:
            records = client.records.list()
        except RateLimitError as e:
            if e.retry_after:
                print(f"Rate limited. Waiting {e.retry_after}s...")
                time.sleep(e.retry_after)
                # Retry the request
                records = client.records.list()
        """)

        # ============================================================
        # 4. AUTHENTICATION & AUTHORIZATION ERRORS
        # ============================================================
        print("\n" + "=" * 60)
        print("4. AUTH ERROR HANDLING")
        print("=" * 60)

        # Authentication (401) - Invalid API key
        auth_error = AuthenticationError("Invalid API key")
        print(f"AuthenticationError (401):")
        print(f"  Message: {auth_error.message}")
        print(f"  Status: {auth_error.status}")

        # Authorization (403) - Insufficient permissions
        authz_error = AuthorizationError("Admin access required")
        print(f"\nAuthorizationError (403):")
        print(f"  Message: {authz_error.message}")
        print(f"  Status: {authz_error.status}")

        # ============================================================
        # 5. NETWORK AND TIMEOUT ERRORS
        # ============================================================
        print("\n" + "=" * 60)
        print("5. NETWORK & TIMEOUT ERRORS")
        print("=" * 60)

        # Network error
        network_error = NetworkError("Connection refused")
        print(f"NetworkError:")
        print(f"  Message: {network_error.message}")
        print(f"  Code: {network_error.code}")

        # Timeout error
        timeout_error = TimeoutError(30.0)
        print(f"\nTimeoutError:")
        print(f"  Message: {timeout_error.message}")
        print(f"  Timeout: {timeout_error.timeout}s")

        # ============================================================
        # 6. CONFLICT ERRORS
        # ============================================================
        print("\n" + "=" * 60)
        print("6. CONFLICT ERROR HANDLING")
        print("=" * 60)

        # Conflict (409) - Duplicate record
        conflict_error = ConflictError(
            "Record already exists for BVD December 2025"
        )
        print(f"ConflictError (409):")
        print(f"  Message: {conflict_error.message}")
        print(f"  Status: {conflict_error.status}")
        print(f"  Code: {conflict_error.code}")

        # ============================================================
        # 7. SERVER ERRORS
        # ============================================================
        print("\n" + "=" * 60)
        print("7. SERVER ERROR HANDLING")
        print("=" * 60)

        # Server error (500-599)
        server_error = ServerError("Internal server error", status=503)
        print(f"ServerError:")
        print(f"  Message: {server_error.message}")
        print(f"  Status: {server_error.status}")
        print(f"  Note: SDK will automatically retry on 500, 502, 503, 504")

        # ============================================================
        # 8. CATCHING ALL SDK ERRORS
        # ============================================================
        print("\n" + "=" * 60)
        print("8. CATCHING ALL SDK ERRORS")
        print("=" * 60)

        print("Use HRPlatformError to catch all SDK-specific errors:")
        print("""
        try:
            record = client.records.get(record_id)
        except NotFoundError:
            # Handle 404 specifically
            print("Record not found")
        except ValidationError as e:
            # Handle validation errors
            for field in e.fields:
                print(f"Field {field['field']}: {field['message']}")
        except HRPlatformError as e:
            # Catch-all for other SDK errors
            print(f"API error [{e.status}]: {e.message}")
            if e.body:
                print(f"Response body: {e.body}")
        except Exception as e:
            # Non-SDK errors (programming errors, etc.)
            print(f"Unexpected error: {e}")
        """)

        # ============================================================
        # 9. EXCEPTION HIERARCHY
        # ============================================================
        print("\n" + "=" * 60)
        print("9. EXCEPTION HIERARCHY")
        print("=" * 60)

        print("""
        HRPlatformError (base class)
        |
        +-- AuthenticationError (401)
        +-- AuthorizationError (403)
        +-- NotFoundError (404)
        |   +-- resource_type: str | None
        |   +-- resource_id: str | None
        +-- ValidationError (400)
        |   +-- fields: list[dict]
        +-- RateLimitError (429)
        |   +-- retry_after: int | None
        |   +-- limit: int | None
        +-- ConflictError (409)
        +-- ServerError (500-599)
        +-- NetworkError (connection issues)
        |   +-- __cause__: Exception
        +-- TimeoutError
            +-- timeout: float
        """)

    print("\n" + "=" * 60)
    print("Error handling examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
