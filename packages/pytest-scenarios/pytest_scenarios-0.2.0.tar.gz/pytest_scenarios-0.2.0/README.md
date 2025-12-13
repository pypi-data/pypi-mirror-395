# Test Scenarios

**Test Scenarios** is a Python library designed to make integration testing with MongoDB effortless and maintainable. It enables you to define reusable data templates and quickly build test scenarios, so you can focus on writing meaningful tests instead of boilerplate setup code.

[![codecov](https://codecov.io/gh/carlosvin/pytest-scenarios/graph/badge.svg?token=6B9XMTWBH2)](https://codecov.io/gh/carlosvin/pytest-scenarios) [![PyPI version](https://badge.fury.io/py/pytest-scenarios.svg)](https://badge.fury.io/py/pytest-scenarios)

## Why use Test Scenarios?

- **Rapid scenario creation:** Define templates once, reuse them across tests, and override only what you need.
- **Consistent test data:** Ensure your integration tests always start with predictable, isolated data.
- **Flexible configuration:** Use environment variables or pytest config files to adapt to any project setup.
- **Seamless pytest integration:** Built for pytest, with fixtures and helpers ready to use.
- **Clean and readable tests:** Keep your test code focused on logic, not data plumbing.

## Installation

Install with pip:

```bash
pip install pytest-scenarios
```

Or with uv:

```bash
uv add pytest-scenarios --dev
```

Or with Poetry:

```bash
poetry add pytest-scenarios --group dev
```

## What are templates?

Templates are Python dictionaries representing MongoDB documents with default values. Each template module matches a MongoDB collection.

See [tests/templates](./tests/templates) for examples like `customers`, `orders`, and `products`.

Example template:

```python
# tests/templates/orders.py

# Each template should be assigned to a `TEMPLATE` var
TEMPLATE = {
    "id": "123456789abcdef01234567",
    "customer_id": "customer_001",
    "items": [
        {"product_id": "product_001", "quantity": 2, "price": 19.99},
        {"product_id": "product_002", "quantity": 1, "price": 9.99},
    ],
    "tax": 0.15,
}
```

## Configuration

Configure the library using environment variables or pytest config files.

### MongoDB Connection

Set your MongoDB URI and database name:

```bash
# Environment variables
DB_URL=mongodb://localhost:27017
DB_NAME=test_db
```

Or in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
db-url="mongodb://localhost:27017"
db-name="test_db"
```

Or in `pytest.ini`:

```ini
[pytest]
db-url=mongodb://localhost:27017
db-name=test_db
```

### Templates Path

Specify where your templates live:

```bash
# Environment variable
TEMPLATES_PATH=tests/templates
```

Or in config files:

```toml
[tool.pytest.ini_options]
templates-path="tests/templates"
```

```ini
[pytest]
templates-path=tests/templates
```

### Pytest Command-Line Options

All options can also be provided directly on the `pytest` command line:

```bash
pytest --templates-path=tests/templates \
    --db-url=mongodb://localhost:27017 \
    --db-name=test_db
```

These flags mirror the environment and config settings shown above, making it easy to override values per run.

## Quickstart

Get started in three steps:

1. **Configure your database and templates path** as shown above.
2. **Create your templates** in the configured templates-path.
3. **Write your test using the scenario builder fixture:**

```python
def test_example(
    scenario_builder: ScenarioBuilder, db: Database
):
    """
    Test that the scenario is created correctly.
    This example creates 2 customers and 2 orders, overriding template values.
    """
    inserted_ids_by_collection = scenario_builder.create(
        {
            "customers": [
                {"name": "Alice", "status": "inactive", "email": "alice@test.com"},
                {"name": "Louis", "age": 25, "email": "louis@test.com"},
            ],
            "orders": [
                {
                    "id": "order_001",
                    "items": [
                        {"price": 19.99, "product_id": "book_123", "quantity": 1}
                    ],
                },
                {
                    "id": "order_002",
                    "items": None,
                    "tax": 0.2,
                },
            ],
        }
    )
    for collection_name, inserted_ids in inserted_ids_by_collection:
        assert len(inserted_ids) == 2, collection_name
```

Check out generated documents in:

- [customers](./tests/__snapshots__/test_scenario_fixture/test_scenario_fixture_creation[customers].json)
- [orders](./tests/__snapshots__/test_scenario_fixture/test_scenario_fixture_creation[orders].json)

## Example Use Cases

- Integration tests for APIs and services using MongoDB
- End-to-end tests requiring complex, multi-collection data setups
- Rapid prototyping of test data for new features

## Contributing

Contributions welcome. Please add tests for new features and follow the project's coding standards.

## License

MIT
