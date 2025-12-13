# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["V1GetUsageParams"]


class V1GetUsageParams(TypedDict, total=False):
    month: int
    """Month to filter usage data (1-12, defaults to current month)"""

    year: int
    """Year to filter usage data (defaults to current year)"""
