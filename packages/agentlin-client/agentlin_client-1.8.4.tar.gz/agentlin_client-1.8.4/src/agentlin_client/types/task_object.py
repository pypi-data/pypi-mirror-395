# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .message_item import MessageItem
from .jsonrpc_error import JsonrpcError
from .reasoning_item import ReasoningItem
from .tool_call_item import ToolCallItem
from .tool_result_item import ToolResultItem

__all__ = ["TaskObject", "Output"]

Output: TypeAlias = Annotated[
    Union[ReasoningItem, MessageItem, ToolCallItem, ToolResultItem], PropertyInfo(discriminator="type")
]


class TaskObject(BaseModel):
    id: str
    """任务 ID。"""

    created_at: int
    """任务创建时间（Unix 秒）。"""

    object: Literal["task"]
    """固定为 task。"""

    output: List[Output]
    """模型/代理生成的输出条目集合（多类型）。"""

    session_id: str
    """会话 ID。"""

    status: Literal[
        "created", "queued", "working", "input-required", "paused", "completed", "canceled", "expired", "failed"
    ]
    """任务状态。"""

    user_id: str
    """用户 ID。"""

    error: Optional[JsonrpcError] = None
    """错误信息（失败时）。"""

    input_required: Optional[ToolCallItem] = None
    """若任务等待外部输入，则给出需要执行的工具调用（如等待用户参数）。"""

    metadata: Optional[Dict[str, builtins.object]] = None
    """扩展元数据。"""

    previous_task_id: Optional[str] = None
    """前置任务 ID（用于续写/衔接）。"""

    rollouts: Optional[List[Dict[str, builtins.object]]] = None
    """任务推演/回溯事件集合（可选）。"""

    usage: Optional[Dict[str, builtins.object]] = None
    """token 用量统计信息。"""
