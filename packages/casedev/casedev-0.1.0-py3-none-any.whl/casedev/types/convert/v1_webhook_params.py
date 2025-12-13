# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["V1WebhookParams", "Result"]


class V1WebhookParams(TypedDict, total=False):
    job_id: Required[str]
    """Unique identifier for the conversion job"""

    status: Required[Literal["completed", "failed"]]
    """Status of the conversion job"""

    error: str
    """Error message for failed jobs"""

    result: Result
    """Result data for completed jobs"""


class Result(TypedDict, total=False):
    duration_seconds: float
    """Processing duration in seconds"""

    file_size_bytes: int
    """Size of processed file in bytes"""

    stored_filename: str
    """Filename where converted file is stored"""
