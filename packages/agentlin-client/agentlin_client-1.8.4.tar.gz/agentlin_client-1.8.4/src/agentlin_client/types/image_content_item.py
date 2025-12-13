# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ImageContentItem", "ImageURL"]


class ImageURL(BaseModel):
    url: str
    """图片的可访问 URL。"""

    detail: Optional[Literal["low", "high", "auto"]] = None
    """清晰度等级，可选 low/high/auto。"""


class ImageContentItem(BaseModel):
    image_url: ImageURL
    """图片 URL 信息。"""

    type: Literal["image", "input_image", "output_image", "image_url"]
    """图片内容类型。"""
