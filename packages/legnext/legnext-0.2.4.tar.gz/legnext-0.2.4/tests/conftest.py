"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def api_key():
    """Test API key fixture."""
    return "test_api_key_12345"


@pytest.fixture
def mock_job_id():
    """Mock job ID fixture."""
    return "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture
def mock_task_response():
    """Mock task response fixture."""
    return {
        "job_id": "550e8400-e29b-41d4-a716-446655440000",
        "model": "midjourney",
        "task_type": "diffusion",
        "status": "completed",
        "output": {
            "image_urls": [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg",
                "https://example.com/image3.jpg",
                "https://example.com/image4.jpg",
            ],
            "seed": "123456",
        },
        "meta": {
            "created_at": "2025-01-20T10:00:00Z",
            "started_at": "2025-01-20T10:00:05Z",
            "ended_at": "2025-01-20T10:01:30Z",
        },
    }
