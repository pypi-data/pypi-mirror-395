# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .text_content_item import TextContentItem

__all__ = ["ReasoningItem"]


class ReasoningItem(BaseModel):
    id: str
    """推理项 ID。"""

    summary: List[TextContentItem]
    """推理摘要内容（结构化）。"""

    type: Literal["reasoning"]
    """推理项类型标识。"""

    content: Optional[List[TextContentItem]] = None
    """推理详细内容（可选）。"""

    status: Optional[Literal["in_progress", "completed", "incomplete"]] = None
    """状态。"""
