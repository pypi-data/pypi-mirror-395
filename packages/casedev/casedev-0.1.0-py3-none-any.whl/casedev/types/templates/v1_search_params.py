# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["V1SearchParams"]


class V1SearchParams(TypedDict, total=False):
    query: Required[str]
    """Search query to find relevant workflows"""

    category: str
    """Optional category filter to narrow results"""

    limit: int
    """Maximum number of results to return (default: 10, max: 50)"""
