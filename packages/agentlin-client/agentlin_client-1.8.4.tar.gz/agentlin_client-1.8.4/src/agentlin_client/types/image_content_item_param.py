# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ImageContentItemParam", "ImageURL"]


class ImageURL(TypedDict, total=False):
    url: Required[str]
    """图片的可访问 URL。"""

    detail: Optional[Literal["low", "high", "auto"]]
    """清晰度等级，可选 low/high/auto。"""


class ImageContentItemParam(TypedDict, total=False):
    image_url: Required[ImageURL]
    """图片 URL 信息。"""

    type: Required[Literal["image", "input_image", "output_image", "image_url"]]
    """图片内容类型。"""
