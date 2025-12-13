# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["FileContentItem", "File"]


class File(BaseModel):
    file_url: str
    """远程文件的可访问 URL；与 file_data 二选一，可同时提供以便存档。"""

    filename: str
    """文件名（含扩展名），用于渲染与调试追踪。"""

    file_data: Optional[str] = None
    """Optional Base64-encoded file content"""


class FileContentItem(BaseModel):
    file: File
    """文件详情。"""

    type: Literal["file"]
    """文件内容类型。"""
