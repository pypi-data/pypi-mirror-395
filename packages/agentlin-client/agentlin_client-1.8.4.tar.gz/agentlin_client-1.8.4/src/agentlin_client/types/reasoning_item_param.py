# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .text_content_item_param import TextContentItemParam

__all__ = ["ReasoningItemParam"]


class ReasoningItemParam(TypedDict, total=False):
    id: Required[str]
    """推理项 ID。"""

    summary: Required[Iterable[TextContentItemParam]]
    """推理摘要内容（结构化）。"""

    type: Required[Literal["reasoning"]]
    """推理项类型标识。"""

    content: Iterable[TextContentItemParam]
    """推理详细内容（可选）。"""

    status: Literal["in_progress", "completed", "incomplete"]
    """状态。"""
