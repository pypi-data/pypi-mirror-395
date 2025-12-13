# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1DeployResponse"]


class V1DeployResponse(BaseModel):
    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Deployment timestamp"""

    deployment_id: Optional[str] = FieldInfo(alias="deploymentId", default=None)
    """Unique deployment identifier"""

    environment: Optional[str] = None
    """Environment name"""

    runtime: Optional[str] = None
    """Runtime used"""

    status: Optional[str] = None
    """Deployment status"""

    url: Optional[str] = None
    """Service endpoint URL (for web services)"""
