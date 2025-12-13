# Changelog

All notable changes to the `hr-platform-sdk` Python package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-06

### Added

- Initial release of the HR Platform Python SDK
- **Client Classes**
  - `HRPlatformClient` - Synchronous client with context manager support
  - `AsyncHRPlatformClient` - Asynchronous client with native asyncio support
  - Factory methods: `with_api_key()` and `with_cookie_auth()`
  
- **Resource Classes**
  - `RecordsResource` - HR record CRUD and workflow operations (list, get, create, update, delete, submit, approve, reject)
  - `AnalyticsResource` - Analytics endpoints (get_summary, get_trends, get_by_entity)
  - `UsersResource` - User management and profiles (list, get, create, update, delete, get_profile, change_password, get_password_policy)
  - `AdminResource` - System administration functions (status, security dashboard, user blocking, session management, audit logs, API key management)
  - `ComplianceResource` - GDPR compliance document flow (status, documents, acknowledge, complete, admin overview, reset)
  - `WebhooksResource` - Webhook subscription management (list, get, create, update, delete, test, delivery history, event types)

- **Pydantic v2 Models**
  - Full type-safe models for all API requests and responses
  - Models generated from OpenAPI specification
  - Support for field aliases (camelCase to snake_case)

- **Error Handling**
  - `HRPlatformError` - Base exception class
  - `AuthenticationError` - 401 errors
  - `AuthorizationError` - 403 errors  
  - `NotFoundError` - 404 errors with resource type/id
  - `ValidationError` - 400 errors with field-level details
  - `RateLimitError` - 429 errors with retry_after support
  - `ConflictError` - 409 errors
  - `ServerError` - 5xx errors
  - `NetworkError` - Connection failures
  - `TimeoutError` - Request timeout with duration

- **HTTP Client Features**
  - Built on httpx for both sync and async support
  - Automatic retry with exponential backoff
  - Configurable retry parameters (max_retries, delays, backoff)
  - Rate limit handling with Retry-After header support
  - Request timeout configuration
  - Custom headers support

- **pandas Integration** (optional)
  - `records_to_dataframe()` - Convert records to DataFrame with optional flattening
  - `trends_to_dataframe()` - Convert trends with period column
  - `entity_breakdown_to_dataframe()` - Entity-indexed DataFrame
  - `summary_to_series()` - Convert summary to pandas Series
  - Install with: `pip install hr-platform-sdk[pandas]`

- **Examples**
  - `basic_usage.py` - Sync client usage patterns
  - `async_usage.py` - Async client with concurrent requests
  - `error_handling.py` - Exception handling patterns
  - `pandas_integration.py` - DataFrame conversion examples

- **Testing**
  - 138 unit tests with pytest
  - 72% code coverage
  - pytest-asyncio for async tests
  - pytest-httpx for HTTP mocking

### Technical Details

- Requires Python 3.9+
- Dependencies: httpx>=0.27.0, pydantic>=2.0.0
- Optional: pandas>=2.0.0
- PEP 561 compatible (py.typed marker included)
- Full mypy strict mode support

[0.1.0]: https://github.com/vollers-group/hr-platform/releases/tag/sdk-python-v0.1.0
