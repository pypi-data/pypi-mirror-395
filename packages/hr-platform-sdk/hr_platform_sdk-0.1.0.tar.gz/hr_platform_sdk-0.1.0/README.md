# hr-platform-sdk

Type-safe Python SDK for the HR Platform API with built-in retry logic, async support, and pandas integration.

## Installation

```bash
pip install hr-platform-sdk
```

For pandas DataFrame integration:

```bash
pip install hr-platform-sdk[pandas]
```

## Quick Start

### API Key Authentication (Service-to-Service)

For integrations with external systems like Microsoft D365 F&O:

```python
from hr_platform import HRPlatformClient

client = HRPlatformClient.with_api_key(
    "hrp_live_xxx...",
    base_url="https://hr-platform.vercel.app"
)

with client:
    # List all records
    records = client.records.list()

    # Get analytics summary
    summary = client.analytics.get_summary(entity="BVD")
```

### Cookie Authentication (Browser Apps)

For browser-based applications using session cookies:

```python
from hr_platform import HRPlatformClient

client = HRPlatformClient.with_cookie_auth(
    base_url="https://hr-platform.vercel.app"
)

with client:
    # Get current user profile
    profile = client.users.get_profile()
```

### Async Usage

```python
import asyncio
from hr_platform import AsyncHRPlatformClient

async def main():
    client = AsyncHRPlatformClient.with_api_key("hrp_live_xxx...")

    async with client:
        # Concurrent requests
        records, summary = await asyncio.gather(
            client.records.list(),
            client.analytics.get_summary()
        )

asyncio.run(main())
```

## Features

- **Type-Safe** - Full type hints with Pydantic v2 models
- **Async Support** - Native asyncio with `AsyncHRPlatformClient`
- **Retry Logic** - Automatic retries with exponential backoff for transient failures
- **Rate Limit Handling** - Respects `Retry-After` headers from rate limit responses
- **Error Classes** - Typed exception classes for different HTTP status codes
- **pandas Integration** - Convert records and analytics to DataFrames (optional dependency)
- **Python 3.9+** - Works with Python 3.9, 3.10, 3.11, and 3.12

## Configuration

### Full Configuration Options

```python
from hr_platform import HRPlatformClient
from hr_platform.core.config import RetryConfig

client = HRPlatformClient.with_api_key(
    "hrp_live_xxx...",
    base_url="https://hr-platform.vercel.app",
    api_version="v1",  # default: "v1"
    timeout=30.0,  # default: 30.0 seconds
    retry=RetryConfig(
        max_retries=3,  # default: 3
        initial_delay=1.0,  # default: 1.0 seconds
        max_delay=30.0,  # default: 30.0 seconds
        backoff_multiplier=2.0,  # default: 2.0
    ),
)
```

## Resources

The SDK provides typed access to all HR Platform API resources:

| Resource | Description |
|----------|-------------|
| `client.records` | HR records CRUD and workflow operations |
| `client.analytics` | Analytics, trends, and entity breakdowns |
| `client.users` | User management and profiles |
| `client.admin` | System administration (requires admin role) |
| `client.compliance` | GDPR compliance document flow |
| `client.webhooks` | Webhook subscription management |

## API Reference

### Records

```python
# List all records (respects entity scoping)
records = client.records.list()

# List with filters
filtered = client.records.list(
    entity="BVD",
    year="2025",
    month="10",
    status="APPROVED"
)

# Get single record
record = client.records.get("record-uuid")

# Create record
result = client.records.create({
    "entity": "BVD",
    "year": 2025,
    "month": 11,
    "working_days": 21,
    "workforce": {
        "bc_male": 20,
        "bc_female": 5,
        # ... other fields
    },
    # ... capacity, absences, turnover, performance, financials
})

# Update record (only DRAFT status)
client.records.update("record-uuid", {
    "working_days": 22,
    # ... updated fields
})

# Delete record (requires appropriate permissions)
client.records.delete("record-uuid")

# Workflow actions
client.records.submit("record-uuid")
client.records.approve("record-uuid")
client.records.reject("record-uuid", reason="Please correct the sick days")
```

### Analytics

```python
# Get summary metrics
summary = client.analytics.get_summary(
    entity="BVD",  # or "All"
    year="2025",
    month="10"
)
print(f"Total headcount: {summary.total_headcount}")
print(f"Total costs: EUR {summary.total_costs:,.2f}")

# Get trend data for charts
trends = client.analytics.get_trends(entity="BVD")
for trend in trends:
    print(f"{trend.month}/{trend.year}: {trend.headcount} employees")

# Get entity breakdown
breakdown = client.analytics.get_by_entity()
for entity in breakdown:
    print(f"{entity.entity}: {entity.total_headcount} headcount")
```

### Users

```python
# Get current user profile
profile = client.users.get_profile()
print(f"Logged in as: {profile.name} ({profile.role})")

# Change password
client.users.change_password(
    current_password="old-password",
    new_password="new-secure-password"
)

# Get password policy
policy = client.users.get_password_policy()
print(f"Min length: {policy.policy.min_length}")

# User management (requires system_admin role)
users = client.users.list()
user = client.users.get("user-uuid")
client.users.create({
    "name": "New User",
    "email": "user@example.com",
    "password": "SecurePass123!",
    "role": "local_partner",
    "entity": "BVD"
})
client.users.update("user-uuid", {"role": "group_head"})
client.users.delete("user-uuid")
```

### Admin (requires system_admin role)

```python
# System status
status = client.admin.get_status()
security = client.admin.get_security_dashboard()
print(f"Failed logins (24h): {security.failed_logins_24h}")

# User administration
client.admin.block_user("user-uuid")
client.admin.unblock_user("user-uuid")
result = client.admin.reset_password("user-uuid")
print(f"Temporary password: {result.temp_password}")

# Session management
sessions = client.admin.list_sessions()
client.admin.force_logout("user-uuid")

# Audit logs
logs = client.admin.get_audit_logs(
    page=1,
    limit=25,
    category="auth",
    severity="warning"
)

# API key management
keys = client.admin.list_api_keys()
result = client.admin.create_api_key({
    "name": "Integration Key",
    "userId": "user-uuid",
    "scopes": ["records:read", "analytics:read"],
    "expiresInDays": 365
})
print(f"API Key (save this!): {result.plain_text_key}")
client.admin.revoke_api_key("key-uuid")
new_key = client.admin.rotate_api_key("key-uuid")
```

### Compliance

```python
# Get compliance status
status = client.compliance.get_status()
if status.pending_documents:
    print(f"Documents pending: {len(status.pending_documents)}")

# Get compliance documents
documents = client.compliance.get_documents()
doc = client.compliance.get_document("privacy_notice")
print(f"Document: {doc.title} (v{doc.version})")

# Acknowledge document
client.compliance.acknowledge(
    document_type="privacy_notice",
    document_version="1.0.0",
    document_content_hash=doc.content_hash
)

# Complete compliance flow
client.compliance.complete()

# Admin: compliance overview (requires system_admin)
overview = client.compliance.get_admin_overview()
print(f"Completed: {overview.summary.completed_users}/{overview.summary.total_users}")
client.compliance.reset_user("user-uuid")
```

### Webhooks

```python
# List subscriptions
subscriptions = client.webhooks.list()

# Create subscription
webhook = client.webhooks.create({
    "name": "My Webhook",
    "url": "https://example.com/webhook",
    "events": ["record.created", "record.approved"]
})
print(f"Created webhook: {webhook.id}")

# Update subscription
client.webhooks.update("subscription-uuid", {"enabled": False})

# Delete subscription
client.webhooks.delete("subscription-uuid")

# Test webhook
result = client.webhooks.test("subscription-uuid")
print(f"Test result: {result.status_code}")

# Get delivery history
history = client.webhooks.get_delivery_history(
    "subscription-uuid",
    page=1,
    limit=50
)

# Get available event types
event_types = client.webhooks.get_event_types()
for event in event_types.events:
    print(f"{event.type}: {event.description}")
```

## Error Handling

The SDK provides typed exception classes for different failure scenarios:

```python
from hr_platform import HRPlatformClient
from hr_platform.exceptions import (
    HRPlatformError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    ServerError,
    NetworkError,
    TimeoutError,
)

try:
    record = client.records.get("invalid-id")
except NotFoundError as e:
    print(f"Record not found: {e.message}")
    print(f"Resource type: {e.resource_type}")
    print(f"Resource ID: {e.resource_id}")
except ValidationError as e:
    print(f"Validation errors on {len(e.fields)} fields:")
    for field in e.fields:
        print(f"  {field['field']}: {field['message']}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except AuthenticationError:
    print("Invalid or expired credentials")
except AuthorizationError:
    print("Insufficient permissions")
except ConflictError as e:
    print(f"Resource conflict: {e.message}")
except ServerError as e:
    print(f"Server error ({e.status}): {e.message}")
except NetworkError as e:
    print(f"Network error: {e.message}")
except TimeoutError as e:
    print(f"Request timed out after {e.timeout}s")
except HRPlatformError as e:
    # Base class for all SDK errors
    print(f"API error [{e.status}]: {e.message}")
```

### Exception Hierarchy

```
HRPlatformError (base class)
├── AuthenticationError (401)
├── AuthorizationError (403)
├── NotFoundError (404)
│   ├── resource_type: str | None
│   └── resource_id: str | None
├── ValidationError (400)
│   └── fields: list[dict]
├── RateLimitError (429)
│   ├── retry_after: int | None
│   └── limit: int | None
├── ConflictError (409)
├── ServerError (500-599)
├── NetworkError (connection issues)
│   └── __cause__: Exception
└── TimeoutError
    └── timeout: float
```

## pandas Integration

Install with pandas support:

```bash
pip install hr-platform-sdk[pandas]
```

Convert API responses to DataFrames:

```python
from hr_platform import HRPlatformClient
from hr_platform.utils import (
    records_to_dataframe,
    trends_to_dataframe,
    entity_breakdown_to_dataframe,
    summary_to_series,
)

with HRPlatformClient.with_api_key("hrp_live_xxx...") as client:
    # Records to DataFrame with flattened nested data
    records = client.records.list()
    df_records = records_to_dataframe(records, flatten=True)
    print(df_records.shape)
    print(df_records.columns.tolist())

    # Group by entity
    print(df_records.groupby("entity")["total_headcount"].sum())

    # Trends to DataFrame with period column
    trends = client.analytics.get_trends()
    df_trends = trends_to_dataframe(trends, include_period=True)
    # Period format: "2025-01", "2025-02", etc.

    # Pivot table for sick rate analysis
    pivot = df_trends.pivot_table(
        values="sick_rate",
        index="period",
        columns="entity",
        aggfunc="mean"
    )

    # Entity breakdown as indexed DataFrame
    breakdown = client.analytics.get_by_entity()
    df_entities = entity_breakdown_to_dataframe(breakdown)
    # Access: df_entities.loc["BVD", "total_headcount"]

    # Summary as pandas Series
    summary = client.analytics.get_summary()
    series = summary_to_series(summary, name="Overall")
    print(series)
```

### Export to CSV (German Excel format)

```python
# German format: semicolon delimiter, comma decimal
df_records.to_csv(
    "records.csv",
    sep=";",
    decimal=",",
    index=False,
    encoding="utf-8-sig",  # BOM for Excel
)
```

### Export to Excel

```python
import pandas as pd

with pd.ExcelWriter("hr_report.xlsx") as writer:
    df_records.to_excel(writer, sheet_name="Records")
    df_trends.to_excel(writer, sheet_name="Trends")
    df_entities.to_excel(writer, sheet_name="Entities")
```

## Async Examples

### Concurrent Requests

```python
import asyncio
from hr_platform import AsyncHRPlatformClient

async def fetch_all_data():
    client = AsyncHRPlatformClient.with_api_key("hrp_live_xxx...")

    async with client:
        # Run multiple requests concurrently - much faster than sequential!
        records, summary, trends, breakdown = await asyncio.gather(
            client.records.list(),
            client.analytics.get_summary(),
            client.analytics.get_trends(),
            client.analytics.get_by_entity(),
        )

        return records, summary, trends, breakdown

# Run
records, summary, trends, breakdown = asyncio.run(fetch_all_data())
```

### Error Handling in Concurrent Requests

```python
import asyncio
from hr_platform import AsyncHRPlatformClient

async def fetch_with_error_handling():
    client = AsyncHRPlatformClient.with_api_key("hrp_live_xxx...")

    async with client:
        # return_exceptions=True prevents one failure from canceling others
        results = await asyncio.gather(
            client.records.list(entity="BVD"),
            client.records.list(entity="VHH"),
            client.analytics.get_summary(),
            return_exceptions=True,
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Request {i} failed: {result}")
            else:
                print(f"Request {i} succeeded: {type(result).__name__}")

asyncio.run(fetch_with_error_handling())
```

### Fetch Multiple Records Concurrently

```python
import asyncio
from hr_platform import AsyncHRPlatformClient

async def fetch_records_by_ids(record_ids: list[str]):
    client = AsyncHRPlatformClient.with_api_key("hrp_live_xxx...")

    async with client:
        records = await asyncio.gather(
            *[client.records.get(rid) for rid in record_ids]
        )
        return records

# Fetch 10 records concurrently
record_ids = ["uuid-1", "uuid-2", "uuid-3", ...]
records = asyncio.run(fetch_records_by_ids(record_ids))
```

## Type Hints

The SDK provides full type hints via Pydantic models:

```python
from hr_platform.models import (
    # Records
    FullHRRecord,
    Workforce,
    Capacity,
    Absences,
    Turnover,
    Performance,
    Financials,

    # Analytics
    AnalyticsSummary,
    AnalyticsTrend,
    EntityBreakdown,

    # Users
    User,
    UserProfile,
    PasswordPolicy,

    # Admin
    SystemStatus,
    SecurityDashboard,
    AuditLogEntry,
    ApiKey,

    # Compliance
    ComplianceStatus,
    ComplianceDocument,

    # Webhooks
    WebhookSubscription,
    WebhookDelivery,
    WebhookEventType,
)

# Type checking works!
def process_records(records: list[FullHRRecord]) -> int:
    return sum(r.workforce.bc_male + r.workforce.bc_female for r in records)
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install hr-platform-sdk[dev]

# Run tests with coverage
pytest

# Type checking
mypy hr_platform

# Linting
ruff check hr_platform
ruff format hr_platform
```

## Requirements

- Python 3.9+
- httpx >= 0.27.0
- pydantic >= 2.0.0
- pandas >= 2.0.0 (optional, for DataFrame support)

## License

MIT
