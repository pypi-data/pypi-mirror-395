# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["V1ContentsResponse", "Result"]


class Result(BaseModel):
    highlights: Optional[List[str]] = None
    """Content highlights if requested"""

    metadata: Optional[object] = None
    """Additional metadata about the content"""

    summary: Optional[str] = None
    """Content summary if requested"""

    text: Optional[str] = None
    """Extracted text content"""

    title: Optional[str] = None
    """Page title"""

    url: Optional[str] = None
    """Source URL"""


class V1ContentsResponse(BaseModel):
    results: Optional[List[Result]] = None
