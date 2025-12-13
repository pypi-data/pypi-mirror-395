"""Tests for the main Client class."""

import pytest

from legnext import Client


def test_client_initialization(api_key):
    """Test client initialization."""
    client = Client(api_key=api_key)
    assert client._http.api_key == api_key
    assert client._http.base_url == "https://api.legnext.ai/api"


def test_client_custom_base_url(api_key):
    """Test client with custom base URL."""
    custom_url = "https://custom.api.com"
    client = Client(api_key=api_key, base_url=custom_url)
    assert client._http.base_url == custom_url


def test_client_has_resources(api_key):
    """Test that client has all resource attributes."""
    client = Client(api_key=api_key)
    assert hasattr(client, "midjourney")
    assert hasattr(client, "tasks")


def test_client_context_manager(api_key):
    """Test client as context manager."""
    with Client(api_key=api_key) as client:
        assert client._http._client is not None

    # After exiting, client should be closed
    assert client._http._client is None


@pytest.mark.asyncio
async def test_async_client_context_manager(api_key):
    """Test async client as context manager."""
    from legnext import AsyncClient

    async with AsyncClient(api_key=api_key) as client:
        assert client._http._client is not None

    # After exiting, client should be closed
    assert client._http._client is None
