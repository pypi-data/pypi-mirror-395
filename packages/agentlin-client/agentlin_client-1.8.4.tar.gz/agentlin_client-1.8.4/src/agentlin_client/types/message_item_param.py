# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .message_content_param import MessageContentParam

__all__ = ["MessageItemParam"]


class MessageItemParam(TypedDict, total=False):
    message_content: Required[MessageContentParam]
    """消息内容，字符串或内容项数组，工具协议兼容的 message_content（保留字段）。"""

    role: Required[Literal["user", "assistant", "system", "developer"]]
    """消息角色。"""

    type: Required[Literal["message"]]
    """消息条目类型标识。"""

    id: str
    """消息 ID。"""

    block_list: Iterable[object]
    """渲染块列表（图表/表格等富媒体）。"""

    name: str
    """角色名称（可选）。"""

    status: Literal["in_progress", "completed", "incomplete"]
    """消息生成状态。"""
