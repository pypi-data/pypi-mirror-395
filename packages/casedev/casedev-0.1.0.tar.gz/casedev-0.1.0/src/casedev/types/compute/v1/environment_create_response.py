# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["EnvironmentCreateResponse"]


class EnvironmentCreateResponse(BaseModel):
    id: Optional[str] = None
    """Unique environment identifier"""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Environment creation timestamp"""

    domain: Optional[str] = None
    """Unique domain for this environment"""

    is_default: Optional[bool] = FieldInfo(alias="isDefault", default=None)
    """Whether this is the default environment"""

    name: Optional[str] = None
    """Environment name"""

    slug: Optional[str] = None
    """URL-friendly slug derived from name"""

    status: Optional[Literal["active", "inactive"]] = None
    """Environment status"""
