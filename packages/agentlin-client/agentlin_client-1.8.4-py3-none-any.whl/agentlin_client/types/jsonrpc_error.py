# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union

from .._models import BaseModel

__all__ = ["JsonrpcError"]


class JsonrpcError(BaseModel):
    code: int
    """错误码（遵循 JSON-RPC 约定或服务端自定义）。"""

    message: str
    """错误信息。"""

    data: Union[List[object], str, float, bool, object, None] = None
    """自定义错误数据，任意 JSON 值或 null。"""
