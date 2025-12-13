# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["V1ContentsParams"]


class V1ContentsParams(TypedDict, total=False):
    urls: Required[SequenceNotStr[str]]
    """Array of URLs to scrape and extract content from"""

    context: str
    """Context to guide content extraction and summarization"""

    extras: object
    """Additional extraction options"""

    highlights: bool
    """Whether to include content highlights"""

    livecrawl: bool
    """Whether to perform live crawling for dynamic content"""

    livecrawl_timeout: Annotated[int, PropertyInfo(alias="livecrawlTimeout")]
    """Timeout in seconds for live crawling"""

    subpages: bool
    """Whether to extract content from linked subpages"""

    subpage_target: Annotated[int, PropertyInfo(alias="subpageTarget")]
    """Maximum number of subpages to crawl"""

    summary: bool
    """Whether to generate content summaries"""

    text: bool
    """Whether to extract text content"""
