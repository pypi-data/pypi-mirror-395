"""Response models for the Legnext SDK."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import JobStatus, TaskType
from .errors import Error
from .shared import Config, ImageOutput, Meta


class TaskResponse(BaseModel):
    """Response from task operations.

    Represents the result of any midjourney task (image, video, editing, etc.).
    The structure is unified, but the 'output' field content varies by task type:

    - Image Generation (diffusion, blend): output.image_urls (list)
    - Single Image Ops (upscale, remix, etc.): output.image_url (single)
    - Video Generation (video-diffusion): output.video_urls (list)
    - Other: output may be empty or contain task-specific data
    """

    job_id: str = Field(..., description="Unique job identifier")
    model: str = Field(..., description="Model used for processing")
    task_type: TaskType = Field(..., description="Type of task")
    status: JobStatus = Field(..., description="Current status")
    config: Optional[Config] = Field(None, description="Task configuration")
    input: Optional[dict[str, Any]] = Field(
        None, description="Input parameters (structure varies by task type)"
    )
    output: Optional[ImageOutput] = Field(
        None,
        description="Output results (null until completed). Structure varies by task_type - see ImageOutput/TaskOutput for details",
    )
    meta: Optional[Meta] = Field(None, description="Task metadata")
    detail: Optional[dict[str, Any]] = Field(None, description="Additional task details")
    logs: Optional[list[str]] = Field(None, description="Processing logs")
    error: Optional[Error] = Field(None, description="Error details if failed")

    @field_validator("task_type", mode="before")
    @classmethod
    def normalize_task_type(cls, v: Any) -> Any:
        """Convert underscore format to hyphen format for task_type enum.

        Handles API responses that may use 'video_diffusion' instead of 'video-diffusion'.
        """
        if isinstance(v, str):
            # Replace underscores with hyphens to match enum values
            return v.replace("_", "-")
        return v

    model_config = ConfigDict(populate_by_name=True)


class BalanceResponse(BaseModel):
    """Response from account balance query.

    Represents the account balance information returned by the API.
    """

    balance: Optional[float] = Field(None, description="Account balance")
    currency: Optional[str] = Field(None, description="Currency code (e.g., 'USD', 'CNY')")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ErrorResponse(BaseModel):
    """Error response from API."""

    error: Error = Field(..., description="Error details")

    model_config = ConfigDict(populate_by_name=True)
