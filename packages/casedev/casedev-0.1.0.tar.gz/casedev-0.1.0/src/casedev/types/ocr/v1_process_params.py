# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["V1ProcessParams", "Features"]


class V1ProcessParams(TypedDict, total=False):
    document_url: Required[str]
    """URL or S3 path to the document to process"""

    callback_url: str
    """URL to receive completion webhook"""

    document_id: str
    """Optional custom document identifier"""

    engine: Literal["doctr", "paddleocr"]
    """OCR engine to use"""

    features: Features
    """OCR features to extract"""

    result_bucket: str
    """S3 bucket to store results"""

    result_prefix: str
    """S3 key prefix for results"""


class Features(TypedDict, total=False):
    forms: bool
    """Detect form fields"""

    layout: bool
    """Preserve document layout"""

    tables: bool
    """Detect and extract tables"""

    text: bool
    """Extract text content"""
