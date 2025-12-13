# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import TypeAlias

from .file_content_item import FileContentItem
from .text_content_item import TextContentItem
from .audio_content_item import AudioContentItem
from .image_content_item import ImageContentItem

__all__ = ["MessageContent", "ContentItemList"]

ContentItemList: TypeAlias = Union[TextContentItem, ImageContentItem, AudioContentItem, FileContentItem, str]

MessageContent: TypeAlias = Union[str, List[ContentItemList]]
