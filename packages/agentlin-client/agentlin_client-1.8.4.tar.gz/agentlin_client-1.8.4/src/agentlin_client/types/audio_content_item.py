# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AudioContentItem", "InputAudio"]


class InputAudio(BaseModel):
    data: str
    """Base64-encoded audio bytes"""

    format: Literal["wav", "mp3"]


class AudioContentItem(BaseModel):
    input_audio: InputAudio
    """输入音频内容。"""

    type: Literal["input_audio", "output_audio", "audio"]
    """音频内容类型。"""
