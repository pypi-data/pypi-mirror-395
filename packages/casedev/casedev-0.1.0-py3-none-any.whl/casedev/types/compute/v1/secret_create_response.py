# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SecretCreateResponse"]


class SecretCreateResponse(BaseModel):
    id: Optional[str] = None
    """Unique identifier for the secret group"""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Creation timestamp"""

    description: Optional[str] = None
    """Description of the secret group"""

    name: Optional[str] = None
    """Name of the secret group"""
