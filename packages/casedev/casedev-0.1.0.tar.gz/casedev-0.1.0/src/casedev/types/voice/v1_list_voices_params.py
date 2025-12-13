# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["V1ListVoicesParams"]


class V1ListVoicesParams(TypedDict, total=False):
    category: str
    """Filter by voice category"""

    collection_id: str
    """Filter by voice collection ID"""

    include_total_count: bool
    """Whether to include total count in response"""

    next_page_token: str
    """Token for retrieving the next page of results"""

    page_size: int
    """Number of voices to return per page (max 100)"""

    search: str
    """Search term to filter voices by name or description"""

    sort: Literal["name", "created_at", "updated_at"]
    """Field to sort by"""

    sort_direction: Literal["asc", "desc"]
    """Sort direction"""

    voice_type: Literal["premade", "cloned", "professional"]
    """Filter by voice type"""
