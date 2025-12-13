# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["V1ProcessParams"]


class V1ProcessParams(TypedDict, total=False):
    input_url: Required[str]
    """HTTPS URL to the FTR file (must be a valid S3 presigned URL)"""

    callback_url: str
    """Optional webhook URL to receive conversion completion notification"""
