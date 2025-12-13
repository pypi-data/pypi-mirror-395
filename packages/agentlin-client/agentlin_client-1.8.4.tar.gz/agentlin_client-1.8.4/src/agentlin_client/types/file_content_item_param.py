# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["FileContentItemParam", "File"]


class File(TypedDict, total=False):
    file_url: Required[str]
    """远程文件的可访问 URL；与 file_data 二选一，可同时提供以便存档。"""

    filename: Required[str]
    """文件名（含扩展名），用于渲染与调试追踪。"""

    file_data: str
    """Optional Base64-encoded file content"""


class FileContentItemParam(TypedDict, total=False):
    file: Required[File]
    """文件详情。"""

    type: Required[Literal["file"]]
    """文件内容类型。"""
