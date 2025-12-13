# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .message_content import MessageContent

__all__ = ["MessageItem"]


class MessageItem(BaseModel):
    message_content: MessageContent
    """消息内容，字符串或内容项数组，工具协议兼容的 message_content（保留字段）。"""

    role: Literal["user", "assistant", "system", "developer"]
    """消息角色。"""

    type: Literal["message"]
    """消息条目类型标识。"""

    id: Optional[str] = None
    """消息 ID。"""

    block_list: Optional[List[object]] = None
    """渲染块列表（图表/表格等富媒体）。"""

    name: Optional[str] = None
    """角色名称（可选）。"""

    status: Optional[Literal["in_progress", "completed", "incomplete"]] = None
    """消息生成状态。"""
