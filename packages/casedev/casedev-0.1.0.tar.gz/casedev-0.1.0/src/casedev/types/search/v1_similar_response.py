# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1SimilarResponse", "Result"]


class Result(BaseModel):
    domain: Optional[str] = None

    published_date: Optional[str] = FieldInfo(alias="publishedDate", default=None)

    similarity_score: Optional[float] = FieldInfo(alias="similarityScore", default=None)

    snippet: Optional[str] = None

    text: Optional[str] = None

    title: Optional[str] = None

    url: Optional[str] = None


class V1SimilarResponse(BaseModel):
    processing_time: Optional[float] = FieldInfo(alias="processingTime", default=None)

    results: Optional[List[Result]] = None

    total_results: Optional[int] = FieldInfo(alias="totalResults", default=None)
