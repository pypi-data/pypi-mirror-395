# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "TextContentItem",
    "Annotation",
    "AnnotationFileCitation",
    "AnnotationURLCitation",
    "AnnotationContainerFileCitation",
    "AnnotationFilePath",
    "Logprob",
    "LogprobTopLogprob",
]


class AnnotationFileCitation(BaseModel):
    file_id: str
    """The ID of the file."""

    filename: str
    """The filename of the file cited."""

    index: int
    """The index of the file in the list of files."""

    type: Literal["file_citation"]
    """The type of the file citation. Always `file_citation`."""


class AnnotationURLCitation(BaseModel):
    end_index: int
    """The index of the last character of the URL citation in the message."""

    start_index: int
    """The index of the first character of the URL citation in the message."""

    title: str
    """The title of the web resource."""

    type: Literal["url_citation"]
    """The type of the URL citation. Always `url_citation`."""

    url: str
    """The URL of the web resource."""


class AnnotationContainerFileCitation(BaseModel):
    container_id: str
    """The ID of the container file."""

    end_index: int
    """The index of the last character of the container file citation in the message."""

    file_id: str
    """The ID of the file."""

    filename: str
    """The filename of the container file cited."""

    start_index: int
    """The index of the first character of the container file citation in the message."""

    type: Literal["container_file_citation"]
    """The type of the container file citation. Always `container_file_citation`."""


class AnnotationFilePath(BaseModel):
    file_url: str
    """The URL of the file cited."""

    index: int
    """The index of the file in the list of files."""

    type: Literal["file_path"]
    """The type of the file citation. Always `file_path`."""


Annotation: TypeAlias = Annotated[
    Union[AnnotationFileCitation, AnnotationURLCitation, AnnotationContainerFileCitation, AnnotationFilePath],
    PropertyInfo(discriminator="type"),
]


class LogprobTopLogprob(BaseModel):
    token: str

    bytes: List[int]

    logprob: float


class Logprob(BaseModel):
    token: str

    bytes: List[int]

    logprob: float

    top_logprobs: List[LogprobTopLogprob]


class TextContentItem(BaseModel):
    text: str
    """文本内容。"""

    type: Literal["text", "input_text", "output_text", "reasoning_text", "summary_text", "refusal"]
    """文本内容类型。"""

    id: Optional[int] = None
    """可选的内容引用 ID。"""

    annotations: Optional[List[Annotation]] = None
    """文本注释（如引用、链接、文件路径等），与后端 Annotation 模型一致。"""

    logprobs: Optional[List[Logprob]] = None
    """每个 token 的对数概率信息（可选）。"""

    tags: Optional[List[str]] = None
    """可选标签，用于标记内容来源或用途（如 "added_by_reference_manager"）。"""
