"""Midjourney operations resource.

All methods directly map to API endpoints for clarity.
Method names and parameters match the API specification exactly.
"""

from typing import Any, BinaryIO, Coroutine, Dict, Literal, TypeVar, Union

from pydantic import BaseModel, HttpUrl

from legnext._internal.http_client import AsyncHTTPClient, HTTPClient
from legnext.types.canvas import Canvas, CanvasImg, Mask
from legnext.types.requests import (
    BlendRequest,
    DescribeRequest,
    DiffusionRequest,
    EditRequest,
    EnhanceRequest,
    ExtendVideoRequest,
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
from legnext.types.responses import TaskResponse

# Type variables for generic methods
T = TypeVar("T", bound=BaseModel)


class MidjourneyMixin:
    """Mixin class with shared methods for Midjourney resources.

    Provides common functionality used by both sync and async resources.
    """

    def _call_endpoint(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        path: str,
        request: Union[BaseModel, None],
        exclude_none: bool = False,
    ) -> Union[Dict[str, Any], Coroutine[Any, Any, Dict[str, Any]]]:
        """Call an API endpoint and return raw data.

        This method must be overridden by subclasses to provide
        actual HTTP client implementation (sync or async).
        """
        raise NotImplementedError

    @staticmethod
    def _prepare_request_data(request: BaseModel, exclude_none: bool = False) -> Dict[str, Any]:
        """Prepare request data for API call."""
        return request.model_dump(by_alias=True, exclude_none=exclude_none, mode="json")

    @staticmethod
    def _parse_response(data: Dict[str, Any]) -> TaskResponse:
        """Parse API response into TaskResponse."""
        return TaskResponse.model_validate(data)


class MidjourneyResource(MidjourneyMixin):
    """Synchronous Midjourney operations resource.

    All methods directly correspond to API endpoints.
    """

    def __init__(self, http: HTTPClient) -> None:
        """Initialize the Midjourney resource."""
        self._http = http

    def _call_endpoint(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        path: str,
        request: Union[BaseModel, None],
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        """Call an API endpoint and return raw data (sync)."""
        data = self._prepare_request_data(request, exclude_none=exclude_none) if request else {}
        return self._http.request(method, path, json=data if data else None)

    # Image Generation Endpoints

    def diffusion(self, text: str, callback: Union[HttpUrl, str, None] = None) -> TaskResponse:
        """Text to image generation (POST /diffusion).

        Args:
            text: Text prompt for image generation (1-8192 characters)
            callback: Optional webhook URL for completion notification

        Returns:
            Task response with job information

        Example:
            ```python
            response = client.midjourney.diffusion(
                text="a beautiful sunset over mountains"
            )
            ```
        """
        request = DiffusionRequest(text=text, callback=callback)
        data = self._call_endpoint("POST", "/v1/diffusion", request)
        return self._parse_response(data)

    def variation(
        self,
        job_id: str,
        image_no: int,
        type: int,
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Create image variation (POST /variation).

        Args:
            job_id: ID of the original image generation task
            image_no: Image number to vary (0-3)
            type: Variation type (0=Subtle, 1=Strong)
            remix_prompt: Optional additional prompt for guided variation
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = VariationRequest(
            job_id=job_id,
            image_no=image_no,
            type=type,
            remix_prompt=remix_prompt,
            callback=callback,
        )
        data = self._call_endpoint("POST", "/v1/variation", request)
        return self._parse_response(data)

    def upscale(
        self, job_id: str, image_no: int, type: int, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Upscale image (POST /upscale).

        Args:
            job_id: ID of the original image generation task
            image_no: Image number to upscale (0-3)
            type: Upscaling type (0=Subtle, 1=Creative)
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = UpscaleRequest(job_id=job_id, image_no=image_no, type=type, callback=callback)
        data = self._call_endpoint("POST", "/v1/upscale", request)
        return self._parse_response(data)

    def reroll(self, job_id: str, callback: Union[HttpUrl, str, None] = None) -> TaskResponse:
        """Re-execute task to generate new variations (POST /reroll).

        Args:
            job_id: ID of the task to reroll
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = RerollRequest(job_id=job_id, callback=callback)
        data = self._call_endpoint("POST", "/v1/reroll", request)
        return self._parse_response(data)

    def blend(
        self,
        img_urls: list[Union[HttpUrl, str]],
        aspect_ratio: str,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Blend 2-5 images together (POST /blend).

        Args:
            img_urls: 2-5 image URLs to blend
            aspect_ratio: Aspect ratio: 2:3, 1:1, or 3:2
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = BlendRequest(img_urls=img_urls, aspect_ratio=aspect_ratio, callback=callback)
        data = self._call_endpoint("POST", "/v1/blend", request)
        return self._parse_response(data)

    def describe(
        self, img_url: Union[HttpUrl, str], callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Generate text descriptions from an image (POST /describe).

        Args:
            img_url: URL of image to describe
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = DescribeRequest(img_url=img_url, callback=callback)
        data = self._call_endpoint("POST", "/v1/describe", request)
        return self._parse_response(data)

    def shorten(self, prompt: str, callback: Union[HttpUrl, str, None] = None) -> TaskResponse:
        """Simplify a prompt to essential elements (POST /shorten).

        Args:
            prompt: Prompt to shorten
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = ShortenRequest(prompt=prompt, callback=callback)
        data = self._call_endpoint("POST", "/v1/shorten", request)
        return self._parse_response(data)

    def pan(
        self,
        job_id: str,
        image_no: int,
        direction: int,
        scale: float,
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Extend image in a specific direction (POST /pan).

        Args:
            job_id: ID of the original image
            image_no: Image number to extend (0-3)
            direction: Extension direction (0-3: UP, DOWN, LEFT, RIGHT)
            scale: Extension scale ratio (1.1-3.0)
            remix_prompt: Optional text prompt for the extended area
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = PanRequest(
            job_id=job_id,
            image_no=image_no,
            direction=direction,
            scale=scale,
            remix_prompt=remix_prompt,
            callback=callback,
        )
        data = self._call_endpoint("POST", "/v1/pan", request)
        return self._parse_response(data)

    def outpaint(
        self,
        job_id: str,
        image_no: int,
        scale: float,
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Expand image in all directions (POST /outpaint).

        Args:
            job_id: ID of the original image
            image_no: Image number to expand (0-3)
            scale: Extension scale ratio (1.1-2.0)
            remix_prompt: Optional text prompt for the extended areas
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = OutpaintRequest(
            job_id=job_id,
            image_no=image_no,
            scale=scale,
            remix_prompt=remix_prompt,
            callback=callback,
        )
        data = self._call_endpoint("POST", "/v1/outpaint", request)
        return self._parse_response(data)

    def inpaint(
        self,
        job_id: str,
        image_no: int,
        mask: Union[bytes, BinaryIO],
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Selectively modify regions using masks (POST /inpaint).

        Args:
            job_id: ID of the original image
            image_no: Image number to edit (0-3)
            mask: Mask image (PNG) or file-like object
            remix_prompt: Optional text prompt for the masked region
            callback: Optional webhook URL

        Returns:
            Task response
        """
        files = {"mask": mask if isinstance(mask, bytes) else mask.read()}
        data_dict: Dict[str, Any] = {
            "jobId": job_id,
            "imageNo": str(image_no),
        }
        if remix_prompt:
            data_dict["remixPrompt"] = remix_prompt
        if callback:
            data_dict["callback"] = callback

        data = self._http.request("POST", "/v1/inpaint", data=data_dict, files=files)
        return self._parse_response(data)

    def remix(
        self,
        job_id: str,
        image_no: int,
        remix_prompt: str,
        mode: Union[int, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Transform images with new prompts (POST /remix).

        Args:
            job_id: ID of the original image
            image_no: Image number to remix (0-3)
            remix_prompt: New prompt for remix
            mode: Remix mode (0=Low, 1=High)
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = RemixRequest(
            job_id=job_id,
            image_no=image_no,
            remix_prompt=remix_prompt,
            mode=mode,
            callback=callback,
        )
        data = self._call_endpoint("POST", "/v1/remix", request)
        return self._parse_response(data)

    def edit(
        self,
        job_id: str,
        image_no: int,
        canvas: Canvas,
        img_pos: CanvasImg,
        remix_prompt: str,
        mask: Union[Mask, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Edit and repaint specific areas with canvas positioning (POST /edit).

        Args:
            job_id: ID of the original image generation task
            image_no: Image number to edit (0-3)
            canvas: Target canvas dimensions (width, height)
            img_pos: Image position and size on canvas (width, height, x, y)
            remix_prompt: Edit instructions and prompt
            mask: Optional mask defining areas to edit (either polygon areas or mask URL)
            callback: Optional webhook URL

        Returns:
            Task response

        Example:
            ```python
            from legnext.types import Canvas, CanvasImg, Mask, Polygon

            response = client.midjourney.edit(
                job_id="abc123",
                image_no=0,
                canvas=Canvas(width=1024, height=1024),
                img_pos=CanvasImg(width=512, height=512, x=256, y=256),
                remix_prompt="add a sunset sky",
                mask=Mask(
                    areas=[
                        Polygon(
                            width=1024,
                            height=1024,
                            points=[100, 100, 500, 100, 500, 500, 100, 500],
                        )
                    ]
                )
            )
            ```
        """
        request = EditRequest(
            job_id=job_id,
            image_no=image_no,
            canvas=canvas,
            img_pos=img_pos,
            remix_prompt=remix_prompt,
            mask=mask,
            callback=callback,
        )
        data = self._call_endpoint("POST", "/v1/edit", request, exclude_none=True)
        return self._parse_response(data)

    def upload_paint(
        self,
        img_url: Union[HttpUrl, str],
        canvas: Canvas,
        img_pos: CanvasImg,
        remix_prompt: str,
        mask: Mask,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Advanced editing with custom canvas positioning (POST /upload-paint).

        Args:
            img_url: URL of the image to edit
            canvas: Target canvas dimensions (width, height)
            img_pos: Image position and size on canvas (width, height, x, y)
            remix_prompt: Painting instructions and prompt
            mask: Mask defining areas to edit (required - either polygon areas or mask URL)
            callback: Optional webhook URL

        Returns:
            Task response

        Example:
            ```python
            from legnext.types import Canvas, CanvasImg, Mask, Polygon

            response = client.midjourney.upload_paint(
                img_url="https://example.com/image.png",
                canvas=Canvas(width=1024, height=1024),
                img_pos=CanvasImg(width=768, height=768, x=128, y=128),
                remix_prompt="paint a beautiful sky",
                mask=Mask(areas=[
                    Polygon(width=1024, height=1024, points=[0, 0, 1024, 0, 1024, 512, 0, 512])
                ])
            )
            ```
        """
        request = UploadPaintRequest(
            img_url=img_url,
            canvas=canvas,
            img_pos=img_pos,
            remix_prompt=remix_prompt,
            mask=mask,
            callback=callback,
        )
        data = self._call_endpoint("POST", "/v1/upload-paint", request)
        return self._parse_response(data)

    def retexture(
        self,
        img_url: Union[HttpUrl, str],
        remix_prompt: str,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Transform materials and textures (POST /retexture).

        Args:
            img_url: URL of the image to retexture
            remix_prompt: Text description of desired texture/material transformation
            callback: Optional webhook URL

        Returns:
            Task response

        Example:
            ```python
            response = client.midjourney.retexture(
                img_url="https://example.com/image.png",
                remix_prompt="marble texture"
            )
            ```
        """
        request = RetextureRequest(img_url=img_url, remix_prompt=remix_prompt, callback=callback)
        data = self._call_endpoint("POST", "/v1/retexture", request)
        return self._parse_response(data)

    def remove_background(
        self, img_url: Union[HttpUrl, str], callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Remove background from an image (POST /remove-background).

        Args:
            img_url: URL of the image to process
            callback: Optional webhook URL

        Returns:
            Task response

        Example:
            ```python
            response = client.midjourney.remove_background(
                img_url="https://example.com/image.png"
            )
            ```
        """
        request = RemoveBackgroundRequest(img_url=img_url, callback=callback)
        data = self._call_endpoint("POST", "/v1/remove-background", request)
        return self._parse_response(data)

    def enhance(
        self, job_id: str, image_no: int, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Improve image quality and detail (POST /enhance).

        Note: Requires original image created with `--v7 --draft`

        Args:
            job_id: ID of the draft mode image
            image_no: Image number to enhance (0-3)
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = EnhanceRequest(job_id=job_id, image_no=image_no, callback=callback)
        data = self._call_endpoint("POST", "/v1/enhance", request)
        return self._parse_response(data)

    # Video Generation Endpoints

    def video_diffusion(
        self,
        prompt: str,
        video_type: Union[int, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Generate video from text prompt (POST /video-diffusion).

        Args:
            prompt: Video generation prompt. Format: "[image_url] your prompt text"
                (1-8192 characters)
            video_type: Video quality type (0: 480p, 1: 720p). Optional.
            callback: Optional webhook URL

        Returns:
            Task response

        Example:
            ```python
            # Generate video with image URL in prompt
            response = client.midjourney.video_diffusion(
                prompt="https://example.com/image.png a flowing river through mountains",
                video_type=1  # 720p
            )
            ```
        """
        request = VideoDiffusionRequest(prompt=prompt, video_type=video_type, callback=callback)
        data = self._call_endpoint("POST", "/v1/video-diffusion", request, exclude_none=True)
        return self._parse_response(data)

    def extend_video(
        self,
        job_id: str,
        video_no: int,
        prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Extend existing video (POST /extend-video).

        Args:
            job_id: ID of the original video task
            video_no: Video number to extend (0 or 1)
            prompt: Optional additional prompt for the extension (1-8192 characters)
            callback: Optional webhook URL

        Returns:
            Task response

        Example:
            ```python
            response = client.midjourney.extend_video(
                job_id="abc123",
                video_no=0,
                prompt="continue with dramatic lighting"
            )
            ```
        """
        request = ExtendVideoRequest(
            job_id=job_id, video_no=video_no, prompt=prompt, callback=callback
        )
        data = self._call_endpoint("POST", "/v1/extend-video", request, exclude_none=True)
        return self._parse_response(data)

    def video_upscale(
        self, job_id: str, video_no: int, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Upscale video quality (POST /video-upscale).

        Args:
            job_id: ID of the original video task
            video_no: Video number to upscale (0 or 1)
            callback: Optional webhook URL

        Returns:
            Task response

        Example:
            ```python
            response = client.midjourney.video_upscale(
                job_id="abc123",
                video_no=0
            )
            ```
        """
        request = VideoUpscaleRequest(job_id=job_id, video_no=video_no, callback=callback)
        data = self._call_endpoint("POST", "/v1/video-upscale", request)
        return self._parse_response(data)


class AsyncMidjourneyResource(MidjourneyMixin):
    """Asynchronous Midjourney operations resource.

    All methods directly correspond to API endpoints.
    """

    def __init__(self, http: AsyncHTTPClient) -> None:
        """Initialize the async Midjourney resource."""
        self._http = http

    async def _call_endpoint(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        path: str,
        request: Union[BaseModel, None],
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        """Call an API endpoint and return raw data (async)."""
        data = self._prepare_request_data(request, exclude_none=exclude_none) if request else {}
        return await self._http.request(method, path, json=data if data else None)

    # Image Generation Endpoints

    async def diffusion(
        self, text: str, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Text to image generation (POST /diffusion) - async."""
        request = DiffusionRequest(text=text, callback=callback)
        data = await self._call_endpoint("POST", "/v1/diffusion", request)
        return self._parse_response(data)

    async def variation(
        self,
        job_id: str,
        image_no: int,
        type: int,
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Create image variation (POST /variation) - async."""
        request = VariationRequest(
            job_id=job_id,
            image_no=image_no,
            type=type,
            remix_prompt=remix_prompt,
            callback=callback,
        )
        data = await self._call_endpoint("POST", "/v1/variation", request)
        return self._parse_response(data)

    async def upscale(
        self, job_id: str, image_no: int, type: int, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Upscale image (POST /upscale) - async."""
        request = UpscaleRequest(job_id=job_id, image_no=image_no, type=type, callback=callback)
        data = await self._call_endpoint("POST", "/v1/upscale", request)
        return self._parse_response(data)

    async def reroll(self, job_id: str, callback: Union[HttpUrl, str, None] = None) -> TaskResponse:
        """Re-execute task (POST /reroll) - async."""
        request = RerollRequest(job_id=job_id, callback=callback)
        data = await self._call_endpoint("POST", "/v1/reroll", request)
        return self._parse_response(data)

    async def blend(
        self,
        img_urls: list[Union[HttpUrl, str]],
        aspect_ratio: str,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Blend 2-5 images together (POST /blend) - async."""
        request = BlendRequest(img_urls=img_urls, aspect_ratio=aspect_ratio, callback=callback)
        data = await self._call_endpoint("POST", "/v1/blend", request)
        return self._parse_response(data)

    async def describe(
        self, img_url: Union[HttpUrl, str], callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Generate text descriptions from an image (POST /describe) - async."""
        request = DescribeRequest(img_url=img_url, callback=callback)
        data = await self._call_endpoint("POST", "/v1/describe", request)
        return self._parse_response(data)

    async def shorten(
        self, prompt: str, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Shorten prompt (POST /shorten) - async."""
        request = ShortenRequest(prompt=prompt, callback=callback)
        data = await self._call_endpoint("POST", "/v1/shorten", request)
        return self._parse_response(data)

    async def pan(
        self,
        job_id: str,
        image_no: int,
        direction: int,
        scale: float,
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Extend image in a specific direction (POST /pan) - async."""
        request = PanRequest(
            job_id=job_id,
            image_no=image_no,
            direction=direction,
            scale=scale,
            remix_prompt=remix_prompt,
            callback=callback,
        )
        data = await self._call_endpoint("POST", "/v1/pan", request)
        return self._parse_response(data)

    async def outpaint(
        self,
        job_id: str,
        image_no: int,
        scale: float,
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Expand image in all directions (POST /outpaint) - async."""
        request = OutpaintRequest(
            job_id=job_id,
            image_no=image_no,
            scale=scale,
            remix_prompt=remix_prompt,
            callback=callback,
        )
        data = await self._call_endpoint("POST", "/v1/outpaint", request)
        return self._parse_response(data)

    async def inpaint(
        self,
        job_id: str,
        image_no: int,
        mask: Union[bytes, BinaryIO],
        remix_prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Selectively modify regions using masks (POST /inpaint) - async."""
        files = {"mask": mask if isinstance(mask, bytes) else mask.read()}
        data_dict: Dict[str, Any] = {
            "jobId": job_id,
            "imageNo": str(image_no),
        }
        if remix_prompt:
            data_dict["remixPrompt"] = remix_prompt
        if callback:
            data_dict["callback"] = callback

        data = await self._http.request("POST", "/v1/inpaint", data=data_dict, files=files)
        return self._parse_response(data)

    async def remix(
        self,
        job_id: str,
        image_no: int,
        remix_prompt: str,
        mode: Union[int, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Transform images with new prompts (POST /remix) - async."""
        request = RemixRequest(
            job_id=job_id,
            image_no=image_no,
            remix_prompt=remix_prompt,
            mode=mode,
            callback=callback,
        )
        data = await self._call_endpoint("POST", "/v1/remix", request)
        return self._parse_response(data)

    async def edit(
        self,
        job_id: str,
        image_no: int,
        canvas: Canvas,
        img_pos: CanvasImg,
        remix_prompt: str,
        mask: Union[Mask, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Edit and repaint specific areas with canvas positioning (POST /edit) - async."""
        request = EditRequest(
            job_id=job_id,
            image_no=image_no,
            canvas=canvas,
            img_pos=img_pos,
            remix_prompt=remix_prompt,
            mask=mask,
            callback=callback,
        )
        data = await self._call_endpoint("POST", "/v1/edit", request, exclude_none=True)
        return self._parse_response(data)

    async def upload_paint(
        self,
        img_url: Union[HttpUrl, str],
        canvas: Canvas,
        img_pos: CanvasImg,
        remix_prompt: str,
        mask: Mask,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Advanced editing with custom canvas positioning (POST /upload-paint) - async."""
        request = UploadPaintRequest(
            img_url=img_url,
            canvas=canvas,
            img_pos=img_pos,
            remix_prompt=remix_prompt,
            mask=mask,
            callback=callback,
        )
        data = await self._call_endpoint("POST", "/v1/upload-paint", request)
        return self._parse_response(data)

    async def retexture(
        self,
        img_url: Union[HttpUrl, str],
        remix_prompt: str,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Transform materials and textures (POST /retexture) - async."""
        request = RetextureRequest(img_url=img_url, remix_prompt=remix_prompt, callback=callback)
        data = await self._call_endpoint("POST", "/v1/retexture", request)
        return self._parse_response(data)

    async def remove_background(
        self, img_url: Union[HttpUrl, str], callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Remove background from an image (POST /remove-background) - async."""
        request = RemoveBackgroundRequest(img_url=img_url, callback=callback)
        data = await self._call_endpoint("POST", "/v1/remove-background", request)
        return self._parse_response(data)

    async def enhance(
        self, job_id: str, image_no: int, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Enhance (POST /enhance) - async."""
        request = EnhanceRequest(job_id=job_id, image_no=image_no, callback=callback)
        data = await self._call_endpoint("POST", "/v1/enhance", request)
        return self._parse_response(data)

    # Video Generation Endpoints

    async def video_diffusion(
        self,
        prompt: str,
        video_type: Union[int, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Generate video from text prompt (POST /video-diffusion) - async.

        Args:
            prompt: Video generation prompt. Format: "[image_url] your prompt text"
                (1-8192 characters)
            video_type: Video quality type (0: 480p, 1: 720p). Optional.
            callback: Optional webhook URL

        Returns:
            Task response
        """
        request = VideoDiffusionRequest(prompt=prompt, video_type=video_type, callback=callback)
        data = await self._call_endpoint("POST", "/v1/video-diffusion", request, exclude_none=True)
        return self._parse_response(data)

    async def extend_video(
        self,
        job_id: str,
        video_no: int,
        prompt: Union[str, None] = None,
        callback: Union[HttpUrl, str, None] = None,
    ) -> TaskResponse:
        """Extend existing video (POST /extend-video) - async."""
        request = ExtendVideoRequest(
            job_id=job_id, video_no=video_no, prompt=prompt, callback=callback
        )
        data = await self._call_endpoint("POST", "/v1/extend-video", request, exclude_none=True)
        return self._parse_response(data)

    async def video_upscale(
        self, job_id: str, video_no: int, callback: Union[HttpUrl, str, None] = None
    ) -> TaskResponse:
        """Upscale video quality (POST /video-upscale) - async."""
        request = VideoUpscaleRequest(job_id=job_id, video_no=video_no, callback=callback)
        data = await self._call_endpoint("POST", "/v1/video-upscale", request)
        return self._parse_response(data)
