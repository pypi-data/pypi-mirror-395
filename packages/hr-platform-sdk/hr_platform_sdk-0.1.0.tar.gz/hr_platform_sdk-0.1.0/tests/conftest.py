"""Pytest fixtures for HR Platform SDK tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest

from hr_platform.core.config import ApiKeyAuth, HRPlatformConfig, RetryConfig


@pytest.fixture
def api_key() -> str:
    """Test API key."""
    return "hrp_test_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"


@pytest.fixture
def base_url() -> str:
    """Test base URL."""
    return "https://test.hr-platform.example.com"


@pytest.fixture
def config(api_key: str, base_url: str) -> HRPlatformConfig:
    """Test configuration."""
    return HRPlatformConfig(
        base_url=base_url,
        api_version="v1",
        auth=ApiKeyAuth(api_key=api_key),
        timeout=30.0,
        retry=RetryConfig(
            max_retries=3,
            initial_delay=0.1,
            max_delay=1.0,
            backoff_multiplier=2.0,
        ),
        headers={},
    )


@pytest.fixture
def mock_response_json() -> dict[str, Any]:
    """Sample JSON response."""
    return {
        "id": "test-uuid-123",
        "entity": "BVD",
        "year": 2025,
        "month": 12,
        "working_days": 21,
        "status": "DRAFT",
    }


@pytest.fixture
def mock_record() -> dict[str, Any]:
    """Sample full HR record."""
    return {
        "id": "test-uuid-123",
        "entity": "BVD",
        "year": 2025,
        "month": 12,
        "working_days": 21,
        "status": "DRAFT",
        "submitted_by": None,
        "submitted_at": None,
        "approved_by": None,
        "approved_at": None,
        "rejected_reason": None,
        "created_at": "2025-12-01T00:00:00.000Z",
        "updated_at": "2025-12-01T00:00:00.000Z",
        "workforce": {
            "bc_male": 20,
            "bc_female": 2,
            "bc_age_under_20": 0,
            "bc_age_20_29": 5,
            "bc_age_30_39": 10,
            "bc_age_40_49": 4,
            "bc_age_50_59": 2,
            "bc_age_60_plus": 1,
            "bc_ausgesteuert": 1,
            "wc_male": 10,
            "wc_female": 8,
            "wc_age_under_20": 0,
            "wc_age_20_29": 2,
            "wc_age_30_39": 8,
            "wc_age_40_49": 5,
            "wc_age_50_59": 2,
            "wc_age_60_plus": 1,
            "wc_ausgesteuert": 0,
        },
        "capacity": {
            "fte_blue_collar": 20.2,
            "fte_white_collar": 14.0,
            "fte_overhead": 9.0,
            "external_hours_blue": 1350,
            "external_hours_white": 0,
            "overtime_hours_blue": 230,
            "overtime_hours_white": 0,
        },
        "absences": {
            "sick_days_blue": 7,
            "sick_days_white": 0,
            "long_term_sick_fte": 0.33,
            "vacation_hours_blue": 1248.8,
            "vacation_hours_white": 640,
            "maternity_fte": 0,
            "parental_fte": 0,
        },
        "turnover": {
            "voluntary_bc": 0,
            "voluntary_wc": 1,
            "involuntary_bc": 0,
            "involuntary_wc": 0,
        },
        "performance": {
            "year_reviews_blue": 6,
            "year_reviews_white": 8,
        },
        "financials": {
            "wages": 71333.95,
            "salaries": 93244.14,
            "temp_wages": 58592.64,
        },
    }


@pytest.fixture
def mock_analytics_summary() -> dict[str, Any]:
    """Sample analytics summary."""
    return {
        "record_count": 12,
        "total_headcount": 480,
        "blue_collar_total": 264,
        "white_collar_total": 216,
        "total_internal_fte": 410.4,
        "total_external_fte": 93.6,
        "total_sick_days": 84,
        "total_costs": 2678048.76,
        "total_turnover": 5,
        "total_reviews_completed": 168,
    }


@pytest.fixture
def mock_trend_data() -> list[dict[str, Any]]:
    """Sample trend data points."""
    return [
        {
            "year": 2025,
            "month": 1,
            "entity": "BVD",
            "headcount": 40,
            "blue_collar": 22,
            "white_collar": 18,
            "internal_fte": 34.2,
            "external_fte": 7.8,
            "sick_days": 7,
            "working_days": 21,
            "sick_rate": 0.83,
            "turnover": 1,
            "reviews_completed": 14,
            "wages": 71333.95,
            "salaries": 93244.14,
            "temp_wages": 58592.64,
        },
        {
            "year": 2025,
            "month": 2,
            "entity": "BVD",
            "headcount": 42,
            "blue_collar": 24,
            "white_collar": 18,
            "internal_fte": 36.0,
            "external_fte": 8.0,
            "sick_days": 5,
            "working_days": 20,
            "sick_rate": 0.60,
            "turnover": 0,
            "reviews_completed": 16,
            "wages": 73000.00,
            "salaries": 95000.00,
            "temp_wages": 60000.00,
        },
    ]


@pytest.fixture
def mock_entity_breakdown() -> list[dict[str, Any]]:
    """Sample entity breakdown data."""
    return [
        {
            "entity": "BVD",
            "record_count": 12,
            "total_headcount": 480,
            "blue_collar": 264,
            "white_collar": 216,
        },
        {
            "entity": "VHH",
            "record_count": 12,
            "total_headcount": 360,
            "blue_collar": 180,
            "white_collar": 180,
        },
        {
            "entity": "VHO",
            "record_count": 12,
            "total_headcount": 240,
            "blue_collar": 144,
            "white_collar": 96,
        },
    ]


@pytest.fixture
def mock_user() -> dict[str, Any]:
    """Sample user data."""
    return {
        "id": "user-uuid-123",
        "name": "Test User",
        "email": "test@vollers.de",
        "role": "group_head",
        "entity": None,
        "created_at": "2025-01-01T00:00:00.000Z",
        "updated_at": "2025-01-01T00:00:00.000Z",
    }


@pytest.fixture
def mock_httpx_client() -> MagicMock:
    """Mock httpx client for testing."""
    mock_client = MagicMock(spec=httpx.Client)
    return mock_client


def create_mock_response(
    status_code: int = 200,
    json_data: dict[str, Any] | list[Any] | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Create a mock httpx Response."""
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.json.return_value = json_data or {}
    response.headers = headers or {}
    response.text = str(json_data) if json_data else ""
    response.is_success = 200 <= status_code < 300
    return response
