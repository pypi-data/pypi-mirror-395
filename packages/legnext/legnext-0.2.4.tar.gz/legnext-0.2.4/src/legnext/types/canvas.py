"""Canvas and mask type definitions for advanced editing operations."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Canvas(BaseModel):
    """Canvas dimensions for editing operations."""

    width: int = Field(..., description="Canvas width in pixels")
    height: int = Field(..., description="Canvas height in pixels")

    model_config = ConfigDict(populate_by_name=True)


class CanvasImg(BaseModel):
    """Image position and size on canvas."""

    width: int = Field(..., description="Image width in pixels")
    height: int = Field(..., description="Image height in pixels")
    x: int = Field(..., description="Horizontal offset from canvas top-left")
    y: int = Field(..., description="Vertical offset from canvas top-left")

    model_config = ConfigDict(populate_by_name=True)


class Polygon(BaseModel):
    """Polygon area definition for mask operations."""

    width: int = Field(..., ge=500, le=4096, description="Image width in pixels (500-4096)")
    height: int = Field(..., ge=500, le=4096, description="Image height in pixels (500-4096)")
    points: List[int] = Field(
        ..., description="Polygon coordinates in XYXY format, clockwise from top-left"
    )

    model_config = ConfigDict(populate_by_name=True)


class Mask(BaseModel):
    """Mask definition for editing operations."""

    areas: Optional[List[Polygon]] = Field(None, description="Polygonal areas to edit")
    url: Optional[str] = Field(None, description="Black and white mask image URL")

    model_config = ConfigDict(populate_by_name=True)
