# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date
from typing_extensions import Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["V1SimilarParams"]


class V1SimilarParams(TypedDict, total=False):
    url: Required[str]
    """The URL to find similar content for"""

    contents: str
    """Additional content to consider for similarity matching"""

    end_crawl_date: Annotated[Union[str, date], PropertyInfo(alias="endCrawlDate", format="iso8601")]
    """Only include pages crawled before this date"""

    end_published_date: Annotated[Union[str, date], PropertyInfo(alias="endPublishedDate", format="iso8601")]
    """Only include pages published before this date"""

    exclude_domains: Annotated[SequenceNotStr[str], PropertyInfo(alias="excludeDomains")]
    """Exclude results from these domains"""

    include_domains: Annotated[SequenceNotStr[str], PropertyInfo(alias="includeDomains")]
    """Only search within these domains"""

    include_text: Annotated[bool, PropertyInfo(alias="includeText")]
    """Whether to include extracted text content in results"""

    num_results: Annotated[int, PropertyInfo(alias="numResults")]
    """Number of similar results to return"""

    start_crawl_date: Annotated[Union[str, date], PropertyInfo(alias="startCrawlDate", format="iso8601")]
    """Only include pages crawled after this date"""

    start_published_date: Annotated[Union[str, date], PropertyInfo(alias="startPublishedDate", format="iso8601")]
    """Only include pages published after this date"""
