# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1SearchResponse", "Result"]


class Result(BaseModel):
    domain: Optional[str] = None
    """Domain of the source"""

    published_date: Optional[datetime] = FieldInfo(alias="publishedDate", default=None)
    """Publication date of the content"""

    snippet: Optional[str] = None
    """Brief excerpt from the content"""

    title: Optional[str] = None
    """Title of the search result"""

    url: Optional[str] = None
    """URL of the search result"""


class V1SearchResponse(BaseModel):
    query: Optional[str] = None
    """Original search query"""

    results: Optional[List[Result]] = None
    """Array of search results"""

    total_results: Optional[int] = FieldInfo(alias="totalResults", default=None)
    """Total number of results found"""
