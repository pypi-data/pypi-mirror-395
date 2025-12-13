# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ToolCallItem"]


class ToolCallItem(BaseModel):
    arguments: str
    """工具调用参数（JSON 字符串）。"""

    call_id: str
    """工具调用唯一 ID（跨事件关联）。"""

    name: str
    """工具名称。"""

    type: Literal["tool_call"]
    """工具调用条目类型标识。"""

    id: Optional[str] = None
    """工具调用条目 ID。"""

    language: Optional[Literal["json", "yaml", "python", "javascript"]] = None
    """参数语言标注（可选）。"""

    status: Optional[Literal["in_progress", "completed", "incomplete"]] = None
    """调用状态。"""
