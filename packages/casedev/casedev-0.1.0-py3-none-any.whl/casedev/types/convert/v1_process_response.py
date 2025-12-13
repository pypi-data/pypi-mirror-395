# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["V1ProcessResponse"]


class V1ProcessResponse(BaseModel):
    job_id: Optional[str] = None
    """Unique identifier for the conversion job"""

    message: Optional[str] = None
    """Instructions for checking job status"""

    status: Optional[Literal["queued", "processing", "completed", "failed"]] = None
    """Current status of the conversion job"""
