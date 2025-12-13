# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ObjectCreatePresignedURLParams"]


class ObjectCreatePresignedURLParams(TypedDict, total=False):
    id: Required[str]

    content_type: Annotated[str, PropertyInfo(alias="contentType")]
    """Content type for PUT operations (optional, defaults to object's content type)"""

    expires_in: Annotated[int, PropertyInfo(alias="expiresIn")]
    """URL expiration time in seconds (1 minute to 7 days)"""

    operation: Literal["GET", "PUT", "DELETE", "HEAD"]
    """The S3 operation to generate URL for"""
