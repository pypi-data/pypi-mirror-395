"""Request models for the Legnext SDK."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from legnext.types.canvas import Canvas, CanvasImg, Mask

# ==================== Image Generation ====================


class DiffusionRequest(BaseModel):
    """Request for text-to-image generation."""

    text: str = Field(
        ..., min_length=1, max_length=8192, description="Text prompt for image generation"
    )
    callback: Optional[HttpUrl] = Field(
        None, description="Optional webhook URL for completion notification"
    )

    model_config = ConfigDict(populate_by_name=True)


class VariationRequest(BaseModel):
    """Request for creating image variations."""

    job_id: str = Field(..., alias="jobId", description="ID of the original image generation task")
    image_no: int = Field(
        ..., alias="imageNo", ge=0, le=3, description="Image number to vary (0-3)"
    )
    type: int = Field(..., ge=0, le=1, description="Variation intensity (0=Subtle, 1=Strong)")
    remix_prompt: Optional[str] = Field(
        None,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="Optional additional prompt for guided variation",
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class UpscaleRequest(BaseModel):
    """Request for upscaling images."""

    job_id: str = Field(..., alias="jobId", description="ID of the original image generation task")
    image_no: int = Field(..., alias="imageNo", ge=0, le=3, description="Image number to upscale")
    type: int = Field(..., ge=0, le=1, description="Upscaling type (0=Subtle, 1=Creative)")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class RerollRequest(BaseModel):
    """Request for rerolling a task."""

    job_id: str = Field(..., alias="jobId", description="ID of the task to reroll")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


# ==================== Image Composition ====================


class BlendRequest(BaseModel):
    """Request for blending multiple images."""

    img_urls: list[HttpUrl] = Field(
        ..., alias="imgUrls", min_length=2, max_length=5, description="2-5 image URLs to blend"
    )
    aspect_ratio: str = Field(
        ..., alias="aspect_ratio", description="Aspect ratio: 2:3, 1:1, or 3:2"
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class DescribeRequest(BaseModel):
    """Request for describing an image."""

    img_url: HttpUrl = Field(..., alias="imgUrl", description="URL of image to describe")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class ShortenRequest(BaseModel):
    """Request for shortening a prompt."""

    prompt: str = Field(..., min_length=1, max_length=8192, description="Prompt to shorten")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


# ==================== Image Extension ====================


class PanRequest(BaseModel):
    """Request for pan/extend operation."""

    job_id: str = Field(..., alias="jobId", description="ID of the original image")
    image_no: int = Field(..., alias="imageNo", ge=0, le=3, description="Image number to extend")
    direction: int = Field(..., ge=0, le=3, description="Extension direction (0-3)")
    scale: float = Field(..., ge=1.1, le=3.0, description="Extension scale ratio (1.1-3.0)")
    remix_prompt: Optional[str] = Field(
        None,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="Text prompt for the extended area",
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class OutpaintRequest(BaseModel):
    """Request for outpaint operation."""

    job_id: str = Field(..., alias="jobId", description="ID of the original image")
    image_no: int = Field(..., alias="imageNo", ge=0, le=3, description="Image number to extend")
    scale: float = Field(..., ge=1.1, le=2.0, description="Extension scale ratio (1.1-2.0)")
    remix_prompt: Optional[str] = Field(
        None,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="Text prompt for the extended areas",
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


# ==================== Image Editing ====================


class InpaintRequest(BaseModel):
    """Request for inpaint operation."""

    job_id: str = Field(..., alias="jobId", description="ID of the original image")
    image_no: int = Field(..., alias="imageNo", ge=0, le=3, description="Image number to edit")
    mask: Any = Field(..., description="Mask regions to repaint")
    remix_prompt: Optional[str] = Field(
        None,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="Text prompt for the repaint area",
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class RemixRequest(BaseModel):
    """Request for remix operation."""

    job_id: str = Field(..., alias="jobId", description="ID of the original image")
    image_no: int = Field(..., alias="imageNo", ge=0, le=3, description="Image number to remix")
    remix_prompt: str = Field(
        ...,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="New text prompt for transformation",
    )
    mode: Optional[int] = Field(None, ge=0, le=1, description="Remix intensity mode (0 or 1)")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class EditRequest(BaseModel):
    """Request for edit operation."""

    job_id: str = Field(..., alias="jobId", description="ID of the original image generation task")
    image_no: int = Field(
        ..., alias="imageNo", ge=0, le=3, description="Image number to edit (0/1/2/3)"
    )
    canvas: Canvas = Field(..., description="Target canvas dimensions")
    img_pos: CanvasImg = Field(..., alias="imgPos", description="Image position relative to canvas")
    remix_prompt: str = Field(
        ...,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="Text prompt for the edit",
    )
    mask: Optional[Mask] = Field(None, description="Areas to repaint on the original image")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class UploadPaintRequest(BaseModel):
    """Request for upload paint operation."""

    img_url: str = Field(
        ..., alias="imgUrl", max_length=1024, description="URL of the source image"
    )
    canvas: Canvas = Field(..., description="Target canvas dimensions")
    img_pos: CanvasImg = Field(..., alias="imgPos", description="Image position and size on canvas")
    remix_prompt: str = Field(
        ...,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="Text prompt for the editing operation",
    )
    mask: Mask = Field(..., description="Areas to edit on the original image")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


# ==================== Image Enhancement ====================


class RetextureRequest(BaseModel):
    """Request for retexture operation."""

    img_url: HttpUrl = Field(
        ..., alias="imgUrl", max_length=1024, description="URL of the source image"
    )
    remix_prompt: str = Field(
        ...,
        alias="remixPrompt",
        min_length=1,
        max_length=8192,
        description="Text description of desired texture/material transformation",
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class RemoveBackgroundRequest(BaseModel):
    """Request for background removal."""

    img_url: HttpUrl = Field(
        ..., alias="imgUrl", max_length=1024, description="URL of the image to process"
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class EnhanceRequest(BaseModel):
    """Request for enhance operation."""

    job_id: str = Field(..., alias="jobId", description="ID of the draft mode image to enhance")
    image_no: int = Field(..., alias="imageNo", ge=0, le=3, description="Image number to enhance")
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


# ==================== Video Generation ====================


class VideoDiffusionRequest(BaseModel):
    """Request for video generation."""

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=8192,
        description='Video generation prompt. Format: "[image_url] your prompt text"',
    )
    video_type: Optional[int] = Field(
        None,
        alias="videoType",
        ge=0,
        le=1,
        description="Video quality type (0: 480p, 1: 720p)",
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class ExtendVideoRequest(BaseModel):
    """Request for extending video."""

    job_id: str = Field(..., alias="jobId", description="ID of the original video task")
    video_no: int = Field(
        ..., alias="videoNo", ge=0, le=3, description="Video number to extend (0-3)"
    )
    prompt: Optional[str] = Field(
        None,
        min_length=1,
        max_length=8192,
        description="Text prompt to guide the extension",
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)


class VideoUpscaleRequest(BaseModel):
    """Request for video upscaling."""

    job_id: str = Field(..., alias="jobId", description="ID of the original video task")
    video_no: int = Field(
        ..., alias="videoNo", ge=0, le=3, description="Video number to upscale (0-3)"
    )
    callback: Optional[HttpUrl] = Field(None, description="Optional webhook URL")

    model_config = ConfigDict(populate_by_name=True)
