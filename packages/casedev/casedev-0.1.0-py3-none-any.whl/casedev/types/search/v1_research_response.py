# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1ResearchResponse"]


class V1ResearchResponse(BaseModel):
    model: Optional[str] = None
    """Model used for research"""

    research_id: Optional[str] = FieldInfo(alias="researchId", default=None)
    """Unique identifier for this research"""

    results: Optional[object] = None
    """Research findings and analysis"""
