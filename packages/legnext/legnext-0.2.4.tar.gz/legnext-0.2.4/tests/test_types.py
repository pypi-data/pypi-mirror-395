"""Tests for type models."""

import pytest
from pydantic import ValidationError

from legnext.types import (
    DiffusionRequest,
    JobStatus,
    TaskResponse,
    TaskType,
    VariationRequest,
)


def test_job_status_enum():
    """Test JobStatus enum values."""
    assert JobStatus.PENDING == "pending"
    assert JobStatus.COMPLETED == "completed"
    assert JobStatus.FAILED == "failed"


def test_task_type_enum():
    """Test TaskType enum values."""
    assert TaskType.DIFFUSION == "diffusion"
    assert TaskType.VARIATION == "variation"
    assert TaskType.UPSCALE == "upscale"


def test_diffusion_request_valid():
    """Test valid DiffusionRequest."""
    request = DiffusionRequest(text="a beautiful sunset")
    assert request.text == "a beautiful sunset"
    assert request.callback is None


def test_diffusion_request_validation():
    """Test DiffusionRequest validation."""
    # Text too short
    with pytest.raises(ValidationError):
        DiffusionRequest(text="")

    # Text too long
    with pytest.raises(ValidationError):
        DiffusionRequest(text="x" * 10000)


def test_variation_request_valid():
    """Test valid VariationRequest."""
    request = VariationRequest(job_id="test-job", image_no=0, type=1)
    assert request.job_id == "test-job"
    assert request.image_no == 0
    assert request.type == 1


def test_variation_request_validation():
    """Test VariationRequest validation."""
    # Invalid image_no (must be 0-3)
    with pytest.raises(ValidationError):
        VariationRequest(job_id="test", image_no=5, type=0)

    # Invalid type (must be 0-1)
    with pytest.raises(ValidationError):
        VariationRequest(job_id="test", image_no=0, type=2)


def test_task_response_parsing(mock_task_response):
    """Test TaskResponse parsing."""
    response = TaskResponse.model_validate(mock_task_response)
    assert response.job_id == mock_task_response["job_id"]
    assert response.status == JobStatus.COMPLETED
    assert len(response.output.image_urls) == 4


def test_task_response_with_empty_urls():
    """Test TaskResponse handles empty string URLs correctly."""
    # Simulate API response with empty string URLs
    response_data = {
        "job_id": "test-job-123",
        "model": "midjourney",
        "task_type": "diffusion",
        "status": "processing",
        "output": {
            "image_url": "",  # Empty string should be converted to None
            "image_urls": None,
            "seed": None,
        },
        "config": {
            "webhook_config": {
                "endpoint": "",  # Empty string should be converted to None
                "secret": None,
            }
        },
    }

    # Should not raise ValidationError
    response = TaskResponse.model_validate(response_data)
    assert response.output.image_url is None
    assert response.config.webhook_config.endpoint is None


def test_task_response_video_diffusion():
    """Test TaskResponse correctly parses video-diffusion API response.

    This tests the real-world scenario where video tasks return video_urls
    instead of image_urls, and include available_actions.
    """
    # Real API response from video-diffusion task
    video_response_data = {
        "job_id": "8201cd3e-6598-4763-9b3d-a337bb0f5f6f",
        "model": "midjourney",
        "task_type": "video_diffusion",  # Test underscore conversion
        "status": "completed",
        "config": {
            "service_mode": "public",
            "webhook_config": {
                "endpoint": "https://webhook.site/c98cb890-fb92-439f-8d60-42c8a51eb52d",
                "secret": "",
            },
        },
        "input": None,
        "output": {
            "video_urls": [
                "https://cdn.legnext.ai/temp/1761044022619.mp4",
                "https://cdn.legnext.ai/temp/1761044026224.mp4",
                "https://cdn.legnext.ai/temp/1761044029496.mp4",
                "https://cdn.legnext.ai/temp/1761044033272.mp4",
            ],
            "seed": "1723670005",
            "available_actions": {
                "extend": [0, 1, 2, 3],
                "upscale": [0, 1, 2, 3],
            },
        },
        "meta": {
            "created_at": "2025-10-21T10:51:46Z",
            "started_at": "2025-10-21T10:51:47Z",
            "ended_at": "2025-10-21T10:54:22Z",
            "usage": {"type": "point", "frozen": 480, "consume": 480},
        },
        "detail": None,
        "logs": [],
        "error": {"code": 0, "raw_message": "", "message": "", "detail": None},
    }

    # Should parse correctly without validation errors
    response = TaskResponse.model_validate(video_response_data)

    # Verify task_type is normalized from underscore to hyphen
    assert response.task_type == TaskType.VIDEO_DIFFUSION
    assert response.task_type == "video-diffusion"

    # Verify video_urls are parsed
    assert response.output.video_urls is not None
    assert len(response.output.video_urls) == 4
    assert str(response.output.video_urls[0]) == "https://cdn.legnext.ai/temp/1761044022619.mp4"

    # Verify seed is parsed
    assert response.output.seed == "1723670005"

    # Verify available_actions are parsed
    assert response.output.available_actions is not None
    assert "extend" in response.output.available_actions
    assert "upscale" in response.output.available_actions
    assert response.output.available_actions["extend"] == [0, 1, 2, 3]


def test_task_response_diffusion_with_available_actions():
    """Test image generation task with available_actions field."""
    diffusion_response = {
        "job_id": "9438247a-be09-48f4-87c9-262a6d8cc786",
        "model": "midjourney",
        "task_type": "diffusion",
        "status": "completed",
        "config": {"service_mode": "public", "webhook_config": {"endpoint": "", "secret": ""}},
        "input": None,
        "output": {
            "image_url": "https://cdn.legnext.ai/mj/9438247a-be09-48f4-87c9-262a6d8cc786_grid.png",
            "image_urls": [
                "https://cdn.legnext.ai/temp/1760990797887.png",
                "https://cdn.legnext.ai/temp/1760990798092.png",
                "https://cdn.legnext.ai/temp/1760990797964.png",
                "https://cdn.legnext.ai/temp/1760990798219.png",
            ],
            "seed": "56397499",
            "available_actions": {
                "edit": [0, 1, 2, 3],
                "inpaint": [0, 1, 2, 3],
                "outpaint": [0, 1, 2, 3],
                "pan": [0, 1, 2, 3],
                "remix": [0, 1, 2, 3],
                "reroll": True,
                "upscale": [0, 1, 2, 3],
                "variation": [0, 1, 2, 3],
            },
        },
        "meta": {
            "created_at": "2025-10-20T20:06:14Z",
            "started_at": "2025-10-20T20:06:15Z",
            "ended_at": "2025-10-20T20:06:45Z",
            "usage": {"type": "point", "frozen": 80, "consume": 80},
        },
        "detail": None,
        "logs": [],
        "error": {"code": 0, "raw_message": "", "message": "", "detail": None},
    }

    response = TaskResponse.model_validate(diffusion_response)
    assert response.task_type == TaskType.DIFFUSION
    assert len(response.output.image_urls) == 4
    assert response.output.available_actions["reroll"] is True
    assert len(response.output.available_actions["edit"]) == 4


def test_task_response_upscale_single_image():
    """Test upscale task with image_urls containing single image."""
    upscale_response = {
        "job_id": "92f8fbf6-0c8c-4fa9-9bf8-660d44fa0984",
        "model": "midjourney",
        "task_type": "upscale",
        "status": "completed",
        "config": {"service_mode": "public", "webhook_config": {"endpoint": "", "secret": ""}},
        "input": None,
        "output": {
            "image_url": "https://cdn.legnext.ai/temp/1761045304084.png",
            "image_urls": ["https://cdn.legnext.ai/temp/1761045304084.png"],
            "seed": "2890393493",
        },
        "meta": {
            "created_at": "2025-10-21T11:14:05Z",
            "started_at": "2025-10-21T11:14:06Z",
            "ended_at": "2025-10-21T11:15:07Z",
            "usage": {"type": "point", "frozen": 120, "consume": 120},
        },
        "detail": None,
        "logs": [],
        "error": {"code": 0, "raw_message": "", "message": "", "detail": None},
    }

    response = TaskResponse.model_validate(upscale_response)
    assert response.task_type == TaskType.UPSCALE
    # Both image_url and image_urls should be present
    assert response.output.image_url is not None
    assert len(response.output.image_urls) == 1
    assert response.output.image_url == response.output.image_urls[0]


def test_task_response_shorten_text_processing():
    """Test shorten task with text processing output structure."""
    shorten_response = {
        "job_id": "8af8a6e3-8daf-4224-a416-9c4f02a0469d",
        "model": "midjourney",
        "task_type": "shorten",
        "status": "completed",
        "config": {"service_mode": "public", "webhook_config": {"endpoint": "", "secret": ""}},
        "input": None,
        "output": {
            "promptEn": "A cyberpunk hacker workspace filled with holographic screens...",
            "description": "/shorten A cyberpunk hacker workspace...",
            "finalPrompt": "## Important tokens\nA **cyberpunk**...",
            "prompts": [
                "cyberpunk hacker workspace filled with holographic screens, mechanical keyboards...",
                "cyberpunk hacker workspace filled with holographic screens, mechanical...",
                "cyberpunk hacker workspace filled with holographic screens, neon...",
                "cyberpunk hacker workspace, holographic, neon...",
                "cyberpunk, workspace...",
            ],
        },
        "meta": {
            "created_at": "2025-10-21T11:26:05Z",
            "started_at": "2025-10-21T11:26:06Z",
            "ended_at": "2025-10-21T11:26:12Z",
            "usage": {"type": "point", "frozen": 20, "consume": 20},
        },
        "detail": None,
        "logs": [],
        "error": {"code": 0, "raw_message": "", "message": "", "detail": None},
    }

    response = TaskResponse.model_validate(shorten_response)
    assert response.task_type == TaskType.SHORTEN
    # Text processing fields
    assert response.output.prompt_en is not None
    assert response.output.description is not None
    assert response.output.final_prompt is not None
    assert len(response.output.prompts) == 5
    # Should not have image/video URLs
    assert response.output.image_url is None
    assert response.output.video_urls is None
