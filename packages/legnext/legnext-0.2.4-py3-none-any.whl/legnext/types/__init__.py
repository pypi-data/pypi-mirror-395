"""Type definitions for the Legnext SDK."""

from .canvas import Canvas, CanvasImg, Mask, Polygon
from .enums import JobStatus, PanDirection, TaskType, UsageType
from .errors import Error, LegnextAPIError, LegnextError
from .requests import (
    BlendRequest,
    DescribeRequest,
    DiffusionRequest,
    EditRequest,
    EnhanceRequest,
    ExtendVideoRequest,
    InpaintRequest,
    OutpaintRequest,
    PanRequest,
    RemixRequest,
    RemoveBackgroundRequest,
    RerollRequest,
    RetextureRequest,
    ShortenRequest,
    UploadPaintRequest,
    UpscaleRequest,
    VariationRequest,
    VideoDiffusionRequest,
    VideoUpscaleRequest,
)
from .responses import (
    BalanceResponse,
    ErrorResponse,
    TaskResponse,
)
from .shared import Config, ImageOutput, Meta, Usage, WebhookConfig

__all__ = [
    # Enums
    "JobStatus",
    "TaskType",
    "UsageType",
    "PanDirection",
    # Errors
    "LegnextError",
    "LegnextAPIError",
    "Error",
    # Requests
    "DiffusionRequest",
    "VariationRequest",
    "UpscaleRequest",
    "RerollRequest",
    "BlendRequest",
    "DescribeRequest",
    "ShortenRequest",
    "PanRequest",
    "OutpaintRequest",
    "InpaintRequest",
    "RemixRequest",
    "EditRequest",
    "UploadPaintRequest",
    "RetextureRequest",
    "RemoveBackgroundRequest",
    "EnhanceRequest",
    "VideoDiffusionRequest",
    "ExtendVideoRequest",
    "VideoUpscaleRequest",
    # Responses
    "TaskResponse",
    "BalanceResponse",
    "ErrorResponse",
    # Shared
    "ImageOutput",
    "Meta",
    "Usage",
    "WebhookConfig",
    "Config",
    # Canvas types
    "Canvas",
    "CanvasImg",
    "Mask",
    "Polygon",
]
