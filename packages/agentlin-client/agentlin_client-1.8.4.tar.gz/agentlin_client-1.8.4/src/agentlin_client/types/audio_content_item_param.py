# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["AudioContentItemParam", "InputAudio"]


class InputAudio(TypedDict, total=False):
    data: Required[str]
    """Base64-encoded audio bytes"""

    format: Required[Literal["wav", "mp3"]]


class AudioContentItemParam(TypedDict, total=False):
    input_audio: Required[InputAudio]
    """输入音频内容。"""

    type: Required[Literal["input_audio", "output_audio", "audio"]]
    """音频内容类型。"""
