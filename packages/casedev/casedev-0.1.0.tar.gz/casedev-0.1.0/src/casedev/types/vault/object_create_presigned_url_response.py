# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ObjectCreatePresignedURLResponse", "Metadata"]


class Metadata(BaseModel):
    bucket: Optional[str] = None

    content_type: Optional[str] = FieldInfo(alias="contentType", default=None)

    region: Optional[str] = None

    size_bytes: Optional[int] = FieldInfo(alias="sizeBytes", default=None)


class ObjectCreatePresignedURLResponse(BaseModel):
    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)
    """URL expiration timestamp"""

    expires_in: Optional[int] = FieldInfo(alias="expiresIn", default=None)
    """URL expiration time in seconds"""

    filename: Optional[str] = None
    """Original filename"""

    instructions: Optional[object] = None
    """Usage instructions and examples"""

    metadata: Optional[Metadata] = None

    object_id: Optional[str] = FieldInfo(alias="objectId", default=None)
    """The object identifier"""

    operation: Optional[str] = None
    """The operation type"""

    presigned_url: Optional[str] = FieldInfo(alias="presignedUrl", default=None)
    """The presigned URL for direct S3 access"""

    s3_key: Optional[str] = FieldInfo(alias="s3Key", default=None)
    """S3 object key"""

    vault_id: Optional[str] = FieldInfo(alias="vaultId", default=None)
    """The vault identifier"""
