# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ToolCallItemParam"]


class ToolCallItemParam(TypedDict, total=False):
    arguments: Required[str]
    """工具调用参数（JSON 字符串）。"""

    call_id: Required[str]
    """工具调用唯一 ID（跨事件关联）。"""

    name: Required[str]
    """工具名称。"""

    type: Required[Literal["tool_call"]]
    """工具调用条目类型标识。"""

    id: str
    """工具调用条目 ID。"""

    language: Literal["json", "yaml", "python", "javascript"]
    """参数语言标注（可选）。"""

    status: Literal["in_progress", "completed", "incomplete"]
    """调用状态。"""
