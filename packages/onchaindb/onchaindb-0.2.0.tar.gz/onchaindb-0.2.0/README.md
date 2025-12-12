# OnChainDB Python SDK

A Python SDK for OnChainDB - a decentralized database built on Celestia blockchain. Provides a fluent, Prisma-like interface for querying and storing data.

## Installation

```bash
pip install onchaindb
```

## Quick Start

```python
from onchaindb import OnChainDBClient

# Initialize the client
client = OnChainDBClient(
    endpoint="https://api.onchaindb.io",
    app_id="your-app-id",
    app_key="your-app-key",
    user_key="optional-user-key"  # Optional: enables Auto-Pay
)

# Find a single user
user = client.find_unique("users", {"email": "john@example.com"})

# Find multiple users
active_users = client.find_many("users", {"status": "active"}, limit=10)

# Count documents
count = client.count_documents("users", {"status": "active"})
```

## QueryBuilder API

The SDK provides a fluent query builder for complex queries:

```python
# Basic query with chaining
results = (client.query_builder()
    .collection("users")
    .where_field("status").equals("active")
    .where_field("age").greater_than(18)
    .select_all()
    .limit(10)
    .offset(0)
    .order_by("created_at", "desc")
    .execute())

# Get single record (most recent)
user = (client.query_builder()
    .collection("users")
    .where_field("email").equals("john@example.com")
    .execute_unique())
```

### Available Operators

| Method | Description |
|--------|-------------|
| `equals(value)` | Exact match |
| `not_equals(value)` | Not equal |
| `greater_than(value)` | Greater than |
| `greater_than_or_equal(value)` | Greater than or equal |
| `less_than(value)` | Less than |
| `less_than_or_equal(value)` | Less than or equal |
| `between(min, max)` | Range match |
| `contains(value)` | Substring match |
| `starts_with(value)` | Starts with |
| `ends_with(value)` | Ends with |
| `reg_exp_matches(pattern)` | Regex match |
| `is_in(values)` | In list |
| `not_in(values)` | Not in list |
| `exists()` | Field exists |
| `not_exists()` | Field doesn't exist |
| `is_null()` | Field is null |
| `is_not_null()` | Field is not null |
| `is_true()` | Field is true |
| `is_false()` | Field is false |
| `is_local_ip()` | IP is local |
| `is_external_ip()` | IP is external |
| `in_country(code)` | IP in country |
| `cidr(range)` | IP in CIDR range |

## Complex Conditions

Use the `find()` method with `ConditionBuilder` for AND/OR/NOT groups:

```python
results = (client.query_builder()
    .collection("users")
    .find(lambda c: c.and_group(lambda: [
        c.field("status").equals("active"),
        c.or_group(lambda: [
            c.field("role").equals("admin"),
            c.field("role").equals("moderator"),
        ]),
    ]))
    .execute())
```

## Aggregations

```python
# Simple aggregations
count = client.query_builder().collection("orders").count()
total = client.query_builder().collection("orders").sum_by("amount")
avg = client.query_builder().collection("orders").avg_by("amount")
max_val = client.query_builder().collection("orders").max_by("amount")
min_val = client.query_builder().collection("orders").min_by("amount")
distinct = client.query_builder().collection("orders").distinct_by("status")

# GroupBy aggregations
count_by_status = (client.query_builder()
    .collection("orders")
    .group_by("status")
    .count())
# Returns: {"pending": 10, "completed": 50, "cancelled": 5}

sum_by_category = (client.query_builder()
    .collection("orders")
    .group_by("category")
    .sum_by("amount"))
# Returns: {"electronics": 5000.0, "clothing": 2500.0}
```

## Server-Side JOINs

```python
# One-to-One JOIN
users = (client.query_builder()
    .collection("users")
    .join_one("profile", "profiles")
        .on_field("user_id").equals("$parent.id")
        .select_fields(["avatar", "bio"])
        .build()
    .execute())

# One-to-Many JOIN
users = (client.query_builder()
    .collection("users")
    .join_many("orders", "orders")
        .on_field("user_id").equals("$parent.id")
        .select_all()
        .build()
    .execute())
```

## Storing Data

```python
# Store with automatic wait for blockchain confirmation (default)
result = client.store(
    collection="users",
    data=[{"id": "user_1", "name": "Alice", "email": "alice@example.com"}],
    payment_proof={"payment_tx_hash": "...", "amount_utia": 10000}
)

# Store without waiting (returns ticket_id immediately)
result = client.store(
    collection="users",
    data=[{"id": "user_1", "name": "Alice"}],
    payment_proof=payment_proof,
    wait_for_confirmation=False
)

# Custom polling settings
result = client.store(
    collection="users",
    data=data,
    payment_proof=payment_proof,
    wait_for_confirmation=True,
    poll_interval_ms=1000,    # Poll every 1 second
    max_wait_time_ms=300000   # Wait up to 5 minutes
)
```

## Task Tracking

```python
# Get task status
task_info = client.get_task_status(ticket_id)
print(f"Status: {task_info['status']}")

# Wait for task to complete
result = client.wait_for_task_completion(
    ticket_id,
    poll_interval_ms=2000,   # Poll every 2 seconds
    max_wait_time_ms=600000  # Wait up to 10 minutes
)

if result['status'] == 'Completed':
    print(f"Transaction confirmed at height: {result['result']['celestia_height']}")
```

## Field Selection

```python
# Select specific fields
results = (client.query_builder()
    .collection("users")
    .select_fields(["id", "name", "email"])
    .execute())

# Select with builder
results = (client.query_builder()
    .collection("users")
    .select(lambda s: s
        .field("id")
        .field("name")
        .nested("profile", lambda n: n.field("avatar"))
    )
    .execute())
```

## Custom HTTP Client

You can provide your own HTTP client implementation:

```python
from onchaindb import OnChainDBClient, HttpClientInterface

class CustomHttpClient(HttpClientInterface):
    def post(self, url: str, data: dict) -> dict:
        # Your custom implementation
        pass

    def get(self, url: str) -> dict:
        # Your custom implementation
        pass

client = OnChainDBClient(
    endpoint="https://api.onchaindb.io",
    app_id="your-app-id",
    app_key="your-app-key",
    http_client=CustomHttpClient()
)
```

## Error Handling

```python
from onchaindb import OnChainDBClient
from onchaindb.exceptions import (
    OnChainDBException,
    QueryException,
    StoreException,
    TaskTimeoutException,
    HttpException,
)

try:
    result = client.store(...)
except TaskTimeoutException as e:
    print(f"Task timed out: {e}")
except StoreException as e:
    print(f"Store failed: {e}")
except QueryException as e:
    print(f"Query failed: {e}")
except HttpException as e:
    print(f"HTTP error (status {e.status_code}): {e}")
except OnChainDBException as e:
    print(f"General error: {e}")
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/list` | POST | Execute queries |
| `/store` | POST | Store data |
| `/task/{ticket_id}` | GET | Get task status |

## Required Headers

The SDK automatically includes these headers:

```
Content-Type: application/json
X-App-Key: {app_key}        # Required - authenticates the app
X-User-Key: {user_key}      # Optional - enables Auto-Pay for the user
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=onchaindb

# Format code
black onchaindb tests

# Type checking
mypy onchaindb

# Lint
ruff check onchaindb
```

## License

MIT License
