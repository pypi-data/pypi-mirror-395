# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "TextContentItemParam",
    "Annotation",
    "AnnotationFileCitation",
    "AnnotationURLCitation",
    "AnnotationContainerFileCitation",
    "AnnotationFilePath",
    "Logprob",
    "LogprobTopLogprob",
]


class AnnotationFileCitation(TypedDict, total=False):
    file_id: Required[str]
    """The ID of the file."""

    filename: Required[str]
    """The filename of the file cited."""

    index: Required[int]
    """The index of the file in the list of files."""

    type: Required[Literal["file_citation"]]
    """The type of the file citation. Always `file_citation`."""


class AnnotationURLCitation(TypedDict, total=False):
    end_index: Required[int]
    """The index of the last character of the URL citation in the message."""

    start_index: Required[int]
    """The index of the first character of the URL citation in the message."""

    title: Required[str]
    """The title of the web resource."""

    type: Required[Literal["url_citation"]]
    """The type of the URL citation. Always `url_citation`."""

    url: Required[str]
    """The URL of the web resource."""


class AnnotationContainerFileCitation(TypedDict, total=False):
    container_id: Required[str]
    """The ID of the container file."""

    end_index: Required[int]
    """The index of the last character of the container file citation in the message."""

    file_id: Required[str]
    """The ID of the file."""

    filename: Required[str]
    """The filename of the container file cited."""

    start_index: Required[int]
    """The index of the first character of the container file citation in the message."""

    type: Required[Literal["container_file_citation"]]
    """The type of the container file citation. Always `container_file_citation`."""


class AnnotationFilePath(TypedDict, total=False):
    file_url: Required[str]
    """The URL of the file cited."""

    index: Required[int]
    """The index of the file in the list of files."""

    type: Required[Literal["file_path"]]
    """The type of the file citation. Always `file_path`."""


Annotation: TypeAlias = Union[
    AnnotationFileCitation, AnnotationURLCitation, AnnotationContainerFileCitation, AnnotationFilePath
]


class LogprobTopLogprob(TypedDict, total=False):
    token: Required[str]

    bytes: Required[Iterable[int]]

    logprob: Required[float]


class Logprob(TypedDict, total=False):
    token: Required[str]

    bytes: Required[Iterable[int]]

    logprob: Required[float]

    top_logprobs: Required[Iterable[LogprobTopLogprob]]


class TextContentItemParam(TypedDict, total=False):
    text: Required[str]
    """文本内容。"""

    type: Required[Literal["text", "input_text", "output_text", "reasoning_text", "summary_text", "refusal"]]
    """文本内容类型。"""

    id: int
    """可选的内容引用 ID。"""

    annotations: Iterable[Annotation]
    """文本注释（如引用、链接、文件路径等），与后端 Annotation 模型一致。"""

    logprobs: Iterable[Logprob]
    """每个 token 的对数概率信息（可选）。"""

    tags: SequenceNotStr[str]
    """可选标签，用于标记内容来源或用途（如 "added_by_reference_manager"）。"""
