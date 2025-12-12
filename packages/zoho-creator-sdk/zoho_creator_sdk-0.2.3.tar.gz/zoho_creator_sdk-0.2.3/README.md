# Zoho Creator Python SDK

[![PyPI version](https://badge.fury.io/py/zoho-creator-sdk.svg)](https://badge.fury.io/py/zoho-creator-sdk)
[![Build Status](https://github.com/carlospaiva/zoho-creator-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/carlospaiva/zoho-creator-sdk/actions)
[![Coverage Status](https://coveralls.io/repos/github/carlospaiva/zoho-creator-sdk/badge.svg?branch=main)](https://coveralls.io/github/carlospaiva/zoho-creator-sdk?branch=main)
[![Python versions](https://img.shields.io/pypi/pyversions/zoho-creator-sdk.svg)](https://pypi.org/project/zoho-creator-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern Python SDK for interacting with the Zoho Creator API. This library provides a simple, intuitive, and fluent interface for managing your Zoho Creator applications, forms, records, and more. It is designed with a "zero-config" approach, making it easy to get started quickly and securely.

**Requires Python 3.8.1+.**

## Key Features

- **Fluent Interface**: Chain method calls for clean, readable, and intuitive API interactions.
- **Zero-Config Initialization**: Automatically loads configuration from environment variables—no need to hardcode credentials.
- **OAuth 2.0 Handling**: Robust OAuth2 authentication with automatic token refresh.
- **Pydantic Models**: Strongly typed data models for all Zoho Creator entities, ensuring data validation and type safety.
- **Automatic Pagination**: Generator-based pagination for effortlessly fetching all records without manual page handling.
- **Robust HTTP Client**: Built on `httpx` with automatic retries, exponential backoff, and rate limiting.
- **Comprehensive Error Handling**: A full suite of custom exception classes for predictable error handling.
- **Full Type Hinting**: Modern, fully type-hinted codebase for excellent editor support and static analysis.

## Installation

Install the SDK using `pip`:

```bash
pip install zoho-creator-sdk
```

## Quick Start

The SDK is designed for a simple, fluent workflow. With zero-config initialization, you can get started in just a few lines of code.

First, set your environment variables. The client will automatically pick them up.

```bash
# OAuth2 Credentials
export ZOHO_CLIENT_ID="your_client_id"
export ZOHO_CLIENT_SECRET="your_client_secret"
export ZOHO_REFRESH_TOKEN="your_refresh_token"

# Datacenter (e.g., US, EU, IN, AU, CN, JP)
export ZOHO_CREATOR_DATACENTER="US"
```

Now, you can use the client in your Python code:

````python
from zoho_creator_sdk import ZohoCreatorClient

# 1. Initialize the client with zero-config
# Credentials are automatically loaded from environment variables.
client = ZohoCreatorClient()

# 2. Discover your applications to find the correct owner and app link names
# The owner_name is typically your Zoho username.
applications = client.get_applications("your-owner-name")
print(f"Found {len(applications)} applications:")
for app in applications:
    print(f"  - {app.name} (Link Name: {app.link_name})")

# 3. Use the fluent interface to access a specific application and its components
# Replace with your actual app link name, owner name, and report link name.
app_context = client.app(app_link_name="my-app", owner_name="your-owner-name")
report_context = app_context.report("all-records")

# 4. Fetch records with automatic pagination
# The get_records() method returns a generator that handles pagination for you.
print("Fetching all records...")
for record in report_context.get_records():
    print(f"  - Record ID: {record.id}, Data: {record.data}")

# 5. Add a new record
form_context = app_context.form("my-form")
new_record_data = {"field1": "value1", "field2": "value2"}
response = form_context.add_record(data=new_record_data)
print(f"\nSuccessfully added new record with ID: {response['data']['id']}")

# 6. Update an existing record
update_data = {"field1": "new_value"}
# The record ID can be obtained from a previous get_records() call.
updated_response = report_context.update_record("RECORD_ID_HERE", data=update_data)
print(f"Successfully updated record: {updated_response['data']['id']}")

## Advanced Get Records options (field_config, fields, record_cursor)

The v2.1 "Get Records" API supports selecting which fields are returned and,
for some integration reports, paging large datasets using a `record_cursor`
header. The SDK exposes these features via typed helpers on `ReportContext`.

```python
from zoho_creator_sdk import ZohoCreatorClient
from zoho_creator_sdk.models import FieldConfig

client = ZohoCreatorClient()
report = client.report(
    app_link_name="my-app",
    owner_name="your-owner-name",
    report_link_name="All_Orders",
)

# Fetch only specific fields from the detail view layout
for record in report.get_records(
    field_config=FieldConfig.DETAIL_VIEW,
    fields=["Email", "Phone"],
    criteria='Status == "Open"',
):
    print(record.get_form_data())

# For integration form reports that return a record_cursor header, use the
# dedicated iterator to automatically follow the cursor across pages:
for record in report.iter_records_with_cursor(
    field_config=FieldConfig.ALL,
    fields=["Order_ID", "Total"],
):
    process(record)
````

## Examples

The `examples/` directory contains more complete scripts demonstrating:

- Basic usage (`examples/basic_usage.py`)
- Configuration and zero-config loading (`examples/configuration.py`)
- Datacenter configuration (`examples/datacenter_usage.py`)
- Error handling patterns (`examples/error_handling.py`)
- OAuth2 authentication details (`examples/oauth2_auth.py`)
- Record CRUD operations (`examples/record_management.py`)

## Configuration

The SDK is designed for "zero-config" initialization by loading all required settings from environment variables.

### Required Environment Variables

| Variable                  | Description                                                    |
| ------------------------- | -------------------------------------------------------------- |
| `ZOHO_CLIENT_ID`          | Your OAuth2 Client ID.                                         |
| `ZOHO_CLIENT_SECRET`      | Your OAuth2 Client Secret.                                     |
| `ZOHO_REFRESH_TOKEN`      | Your OAuth2 Refresh Token.                                     |
| `ZOHO_CREATOR_DATACENTER` | The Zoho datacenter for your account (e.g., `US`, `EU`, `IN`). |

### Optional Environment Variables

These variables enable environment-specific behavior and demo users, as
described in the Zoho Creator v2.1 API docs:

| Variable                      | Description                                                       |
| ----------------------------- | ----------------------------------------------------------------- |
| `ZOHO_CREATOR_ENVIRONMENT`    | Optional environment header value, e.g. `development` or `stage`. |
| `ZOHO_CREATOR_DEMO_USER_NAME` | Optional demo user name used together with `environment`.         |

The SDK exclusively uses **OAuth 2.0 authentication** for enhanced security. API key authentication is not supported.

## Development

This project uses `uv` for dependency management and task running.

### Development Setup

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/carlospaiva/zoho-creator-sdk.git
    cd zoho-creator-sdk
    ```

2.  **Install dependencies**:
    ```bash
    uv sync
    ```

### Running Tests

The project has a comprehensive test suite with 95%+ coverage across all modules. Our testing infrastructure includes unit tests, integration tests, and comprehensive coverage enforcement.

- **Run all tests with coverage**:

  ```bash
  uv run pytest --cov=zoho_creator_sdk --cov-report=term-missing --cov-report=html
  ```

- **Run tests with coverage verification (enforces 95% minimum)**:

  ```bash
  python scripts/verify_coverage.py
  ```

- **Run specific test categories**:

  ```bash
  # Unit tests only
  uv run pytest tests/unit/

  # Integration tests only
  uv run pytest tests/integration/

  # Model tests
  uv run pytest tests/models/unit/

  # Client tests
  uv run pytest tests/client/unit/
  ```

- **Run tests in parallel for faster execution**:
  ```bash
  uv run pytest -n auto
  ```

#### Coverage Requirements

- **Minimum Coverage**: 95% enforced in CI/CD
- **Current Coverage**: ~76% and actively improving
- **Coverage Reports**: Generated in XML, HTML, and terminal formats
- **Coverage Tracking**: Integrated with Codecov for visualization

#### Pre-commit Hooks

The project includes comprehensive pre-commit hooks that enforce code quality and test coverage:

```bash
# Install pre-commit hooks
pre-commit install

# Hooks will automatically run on each commit:
# - Code formatting (black, isort)
# - Linting (flake8, mypy)
# - Test collection validation
# - Coverage verification (95% minimum)
```

#### Test Structure

Tests are organized by feature and type:

```
tests/
├── auth/                 # Authentication handlers and OAuth2 tests
├── client/               # HTTP client and fluent client tests
├── config/               # Configuration loading and environment handling
├── integration/          # API integration and workflow tests
├── models/               # Model validation and behavior tests
├── utils/                # Utility and helper tests
└── workflows/            # Workflow models and execution tests
```

Each test file focuses on specific functionality with comprehensive edge case coverage, proper mocking, and deterministic test execution.

### Code Quality and Linting

The project uses comprehensive tooling to enforce code quality, type safety, and consistent style.

- **Format code**:

  ```bash
  uv run black .
  uv run isort .
  ```

- **Run linters and type checking**:

  ```bash
  # Run all quality checks
  uv run python scripts/run_lint.py

  # Individual tools
  uv run flake8 .
  uv run pylint src
  uv run mypy src
  ```

- **Check code coverage**:
  ```bash
  # Verify 95% coverage requirement
  python scripts/verify_coverage.py
  ```

#### Quality Standards

- **Code Formatting**: Black (88-character line length) + isort
- **Linting**: flake8 with comprehensive rule set
- **Type Checking**: mypy with strict optional checking
- **Test Coverage**: 95% minimum enforced in CI/CD
- **Pre-commit Hooks**: Automated quality checks on every commit

### Building the Package

To build the distributable package:

```bash
make build
# or, equivalently:
uv run python -m build
```

## Contributing

Contributions are welcome! Please follow the guidelines in our [Contributing Guide](https://github.com/carlospaiva/zoho-creator-sdk/blob/main/CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
