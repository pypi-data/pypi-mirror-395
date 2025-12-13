# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["TemplateCreateResponse"]


class TemplateCreateResponse(BaseModel):
    id: Optional[str] = None
    """Template ID"""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Creation timestamp"""

    name: Optional[str] = None
    """Template name"""

    type: Optional[str] = None
    """Template type"""

    variables: Optional[List[str]] = None
    """Detected template variables"""
