# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .task_object import TaskObject
from .jsonrpc_error import JsonrpcError

__all__ = ["TaskDeleteResponse"]


class TaskDeleteResponse(BaseModel):
    jsonrpc: Literal["2.0"]
    """JSON-RPC protocol version, always '2.0'."""

    id: Union[str, int, None] = None
    """请求/响应 ID，由客户端生成或服务器透传；可为字符串、整数或 null。"""

    error: Optional[JsonrpcError] = None
    """JSON-RPC 错误对象（如失败时）。"""

    result: Optional[TaskObject] = None
    """JSON-RPC result：任务对象。"""
