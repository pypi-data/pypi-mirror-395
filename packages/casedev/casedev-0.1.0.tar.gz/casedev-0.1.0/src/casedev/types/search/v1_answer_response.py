# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1AnswerResponse", "Citation"]


class Citation(BaseModel):
    id: Optional[str] = None

    published_date: Optional[str] = FieldInfo(alias="publishedDate", default=None)

    text: Optional[str] = None

    title: Optional[str] = None

    url: Optional[str] = None


class V1AnswerResponse(BaseModel):
    answer: Optional[str] = None
    """The generated answer with citations"""

    citations: Optional[List[Citation]] = None
    """Sources used to generate the answer"""

    model: Optional[str] = None
    """Model used for answer generation"""

    search_type: Optional[str] = FieldInfo(alias="searchType", default=None)
    """Type of search performed"""
