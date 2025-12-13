"""Shared type definitions used across the SDK."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from .enums import ServiceMode, UsageType


class WebhookConfig(BaseModel):
    """Webhook configuration for callbacks."""

    endpoint: Optional[HttpUrl] = Field(None, description="Webhook URL for callbacks")
    secret: Optional[str] = Field(None, description="Webhook secret for validation")

    @field_validator("endpoint", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Any:
        """Convert empty string to None for URL fields."""
        if v == "":
            return None
        return v

    model_config = ConfigDict(populate_by_name=True)


class Config(BaseModel):
    """Configuration for API requests."""

    service_mode: Optional[ServiceMode] = Field(None, description="Service mode")
    webhook_config: Optional[WebhookConfig] = Field(None, description="Webhook configuration")

    model_config = ConfigDict(populate_by_name=True)


class Usage(BaseModel):
    """Usage information for a task."""

    type: UsageType = Field(description="Type of usage quota")
    frozen: int = Field(description="Frozen quota points")
    consume: int = Field(description="Consumed quota points")

    model_config = ConfigDict(populate_by_name=True)


class Meta(BaseModel):
    """Metadata about task execution."""

    created_at: datetime = Field(description="When the job was created")
    started_at: Optional[datetime] = Field(None, description="When processing started")
    ended_at: Optional[datetime] = Field(None, description="When processing completed")
    usage: Optional[Usage] = Field(None, description="Usage information")

    model_config = ConfigDict(populate_by_name=True)


class TaskOutput(BaseModel):
    """Output from task operations (image, video, or other).

    This unified output model supports multiple task types with varying structures:

    Image Generation (diffusion, blend, reroll):
    - image_url: Grid/composite image URL
    - image_urls: List of 4 generated images
    - seed: Generation seed
    - available_actions: Dict of available follow-up operations

    Single Image Operations (variation, upscale, remix, pan, etc.):
    - image_url: Single processed image URL
    - image_urls: List containing the single image URL
    - seed: Generation seed
    - available_actions: (optional) Dict of available operations

    Video Operations (video-diffusion, extend-video, video-upscale):
    - video_urls: List of video URLs
    - seed: Generation seed
    - available_actions: (optional) Dict of available operations

    Text Processing (shorten, describe):
    - promptEn: English prompt
    - description: Text description
    - finalPrompt: Formatted final prompt
    - prompts: List of alternative prompts

    Additional fields may be present depending on task_type and are preserved as-is.
    """

    # Image fields
    image_url: Optional[HttpUrl] = Field(
        None, description="Single image URL (for single image operations)"
    )
    image_urls: Optional[list[HttpUrl]] = Field(
        None, description="Array of image URLs (typically 4 images for generation)"
    )

    # Video fields
    video_urls: Optional[list[HttpUrl]] = Field(
        None, description="Array of video URLs (for video generation operations)"
    )

    # Shared fields
    seed: Optional[str] = Field(None, description="Seed used for generation (for reproducibility)")
    available_actions: Optional[dict[str, Any]] = Field(
        None, description="Available follow-up actions for this task (e.g., extend, upscale)"
    )

    # Text processing fields (for shorten, describe, etc.)
    prompt_en: Optional[str] = Field(
        None, alias="promptEn", description="English prompt (for text processing tasks)"
    )
    description: Optional[str] = Field(
        None, description="Text description (for text processing tasks)"
    )
    final_prompt: Optional[str] = Field(
        None, alias="finalPrompt", description="Formatted final prompt (for text processing tasks)"
    )
    prompts: Optional[list[str]] = Field(
        None, description="List of alternative prompts (for text processing tasks)"
    )

    @field_validator("image_url", "image_urls", "video_urls", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Any:
        """Convert empty string to None for URL fields."""
        if v == "":
            return None
        return v

    model_config = ConfigDict(populate_by_name=True, extra="allow")


# Alias for backward compatibility
ImageOutput = TaskOutput
