# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .._types import SequenceNotStr
from .file_content_item_param import FileContentItemParam
from .text_content_item_param import TextContentItemParam
from .audio_content_item_param import AudioContentItemParam
from .image_content_item_param import ImageContentItemParam

__all__ = ["MessageContentParam", "ContentItemList"]

ContentItemList: TypeAlias = Union[
    TextContentItemParam, ImageContentItemParam, AudioContentItemParam, FileContentItemParam, str
]

MessageContentParam: TypeAlias = Union[str, SequenceNotStr[ContentItemList]]
