# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .message_content import MessageContent

__all__ = ["ToolResultItem"]


class ToolResultItem(BaseModel):
    block_list: List[object]
    """工具结果的渲染块列表。"""

    call_id: str
    """对应的工具调用 ID。"""

    message_content: MessageContent
    """消息内容，字符串或内容项数组，工具协议兼容的 message_content（保留字段）。"""

    type: Literal["tool_result"]
    """工具结果条目类型标识。"""

    id: Optional[str] = None
    """工具结果条目 ID。"""

    status: Optional[Literal["in_progress", "completed", "incomplete"]] = None
    """结果状态。"""
