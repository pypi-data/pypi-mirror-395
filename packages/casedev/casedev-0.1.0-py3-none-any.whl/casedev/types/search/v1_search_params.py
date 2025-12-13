# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["V1SearchParams"]


class V1SearchParams(TypedDict, total=False):
    query: Required[str]
    """Primary search query"""

    additional_queries: Annotated[SequenceNotStr[str], PropertyInfo(alias="additionalQueries")]
    """Additional related search queries to enhance results"""

    category: str
    """Category filter for search results"""

    contents: str
    """Specific content type to search for"""

    end_crawl_date: Annotated[Union[str, date], PropertyInfo(alias="endCrawlDate", format="iso8601")]
    """End date for crawl date filtering"""

    end_published_date: Annotated[Union[str, date], PropertyInfo(alias="endPublishedDate", format="iso8601")]
    """End date for published date filtering"""

    exclude_domains: Annotated[SequenceNotStr[str], PropertyInfo(alias="excludeDomains")]
    """Domains to exclude from search results"""

    include_domains: Annotated[SequenceNotStr[str], PropertyInfo(alias="includeDomains")]
    """Domains to include in search results"""

    include_text: Annotated[bool, PropertyInfo(alias="includeText")]
    """Whether to include full text content in results"""

    num_results: Annotated[int, PropertyInfo(alias="numResults")]
    """Number of search results to return"""

    start_crawl_date: Annotated[Union[str, date], PropertyInfo(alias="startCrawlDate", format="iso8601")]
    """Start date for crawl date filtering"""

    start_published_date: Annotated[Union[str, date], PropertyInfo(alias="startPublishedDate", format="iso8601")]
    """Start date for published date filtering"""

    type: Literal["auto", "search", "news"]
    """Type of search to perform"""

    user_location: Annotated[str, PropertyInfo(alias="userLocation")]
    """Geographic location for localized results"""
