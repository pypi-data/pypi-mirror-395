# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1CreateResponse"]


class V1CreateResponse(BaseModel):
    id: Optional[str] = None
    """Unique webhook endpoint ID"""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Creation timestamp"""

    description: Optional[str] = None
    """Webhook description"""

    events: Optional[List[str]] = None
    """Subscribed event types"""

    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)
    """Whether webhook is active"""

    secret: Optional[str] = None
    """Webhook signing secret (only shown on creation)"""

    url: Optional[str] = None
    """Webhook destination URL"""
