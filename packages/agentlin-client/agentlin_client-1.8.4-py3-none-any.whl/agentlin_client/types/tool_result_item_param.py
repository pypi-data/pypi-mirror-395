# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .message_content_param import MessageContentParam

__all__ = ["ToolResultItemParam"]


class ToolResultItemParam(TypedDict, total=False):
    block_list: Required[Iterable[object]]
    """工具结果的渲染块列表。"""

    call_id: Required[str]
    """对应的工具调用 ID。"""

    message_content: Required[MessageContentParam]
    """消息内容，字符串或内容项数组，工具协议兼容的 message_content（保留字段）。"""

    type: Required[Literal["tool_result"]]
    """工具结果条目类型标识。"""

    id: str
    """工具结果条目 ID。"""

    status: Literal["in_progress", "completed", "incomplete"]
    """结果状态。"""
