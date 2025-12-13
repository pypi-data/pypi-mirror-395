# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["VaultListResponse", "Vault"]


class Vault(BaseModel):
    id: Optional[str] = None
    """Vault identifier"""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Vault creation timestamp"""

    description: Optional[str] = None
    """Vault description"""

    enable_graph: Optional[bool] = FieldInfo(alias="enableGraph", default=None)
    """Whether GraphRAG is enabled"""

    name: Optional[str] = None
    """Vault name"""

    total_bytes: Optional[int] = FieldInfo(alias="totalBytes", default=None)
    """Total storage size in bytes"""

    total_objects: Optional[int] = FieldInfo(alias="totalObjects", default=None)
    """Number of stored documents"""


class VaultListResponse(BaseModel):
    total: Optional[int] = None
    """Total number of vaults"""

    vaults: Optional[List[Vault]] = None
