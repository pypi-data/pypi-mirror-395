# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["V1ProcessResponse"]


class V1ProcessResponse(BaseModel):
    id: Optional[str] = None
    """Unique job identifier"""

    created_at: Optional[datetime] = None
    """Job creation timestamp"""

    document_id: Optional[str] = None
    """Document identifier"""

    engine: Optional[str] = None
    """OCR engine used"""

    estimated_completion: Optional[datetime] = None
    """Estimated completion time"""

    page_count: Optional[int] = None
    """Number of pages detected"""

    status: Optional[Literal["queued", "processing", "completed", "failed"]] = None
    """Current job status"""
