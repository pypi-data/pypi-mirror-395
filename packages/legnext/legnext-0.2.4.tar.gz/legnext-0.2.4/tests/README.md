# Legnext SDK Tests

This directory contains tests for the Legnext Python SDK.

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=legnext --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_client.py
```

Run tests matching a pattern:
```bash
pytest -k "test_client"
```

## Test Structure

- `conftest.py` - Pytest configuration and shared fixtures
- `test_client.py` - Tests for Client and AsyncClient
- `test_types.py` - Tests for type models and validation
- `test_webhook.py` - Tests for webhook functionality
- `test_errors.py` - Tests for error handling
- `test_http_client.py` - Tests for HTTP client (to be added)
- `test_resources.py` - Tests for resource classes (to be added)

## Writing Tests

### Using Fixtures

```python
def test_something(api_key, mock_task_response):
    client = Client(api_key=api_key)
    # Use mock_task_response...
```

### Mocking HTTP Requests

```python
from unittest.mock import Mock, patch

def test_with_mock(api_key):
    with patch('legnext._internal.http_client.httpx.Client') as mock_client:
        mock_response = Mock()
        mock_response.json.return_value = {"job_id": "test"}
        mock_client.return_value.request.return_value = mock_response

        client = Client(api_key=api_key)
        # Test...
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_feature():
    # Test async code...
```

## Coverage

We aim for >80% code coverage. Check coverage with:

```bash
pytest --cov=legnext --cov-report=term-missing
```

View detailed HTML report:
```bash
open htmlcov/index.html
```
