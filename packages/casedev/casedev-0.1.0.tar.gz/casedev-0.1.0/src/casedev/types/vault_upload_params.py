# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VaultUploadParams"]


class VaultUploadParams(TypedDict, total=False):
    content_type: Required[Annotated[str, PropertyInfo(alias="contentType")]]
    """MIME type of the file (e.g., application/pdf, image/jpeg)"""

    filename: Required[str]
    """Name of the file to upload"""

    auto_index: bool
    """Whether to automatically process and index the file for search"""

    metadata: object
    """Additional metadata to associate with the file"""

    size_bytes: Annotated[float, PropertyInfo(alias="sizeBytes")]
    """Estimated file size in bytes for cost calculation"""
