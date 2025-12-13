# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["VaultUploadResponse", "Instructions"]


class Instructions(BaseModel):
    headers: Optional[object] = None

    method: Optional[str] = None

    note: Optional[str] = None


class VaultUploadResponse(BaseModel):
    auto_index: Optional[bool] = None
    """Whether the file will be automatically indexed"""

    expires_in: Optional[float] = FieldInfo(alias="expiresIn", default=None)
    """URL expiration time in seconds"""

    instructions: Optional[Instructions] = None

    next_step: Optional[str] = None
    """Next API endpoint to call for processing"""

    object_id: Optional[str] = FieldInfo(alias="objectId", default=None)
    """Unique identifier for the uploaded object"""

    s3_key: Optional[str] = FieldInfo(alias="s3Key", default=None)
    """S3 object key for the file"""

    upload_url: Optional[str] = FieldInfo(alias="uploadUrl", default=None)
    """Presigned URL for uploading the file"""
