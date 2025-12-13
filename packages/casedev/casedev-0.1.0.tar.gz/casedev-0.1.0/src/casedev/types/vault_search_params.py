# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VaultSearchParams"]


class VaultSearchParams(TypedDict, total=False):
    query: Required[str]
    """Search query or question to find relevant documents"""

    filters: Dict[str, object]
    """Additional filters to apply to search results"""

    method: Literal["vector", "graph", "hybrid", "global", "local", "fast", "entity"]
    """
    Search method: 'global' for comprehensive questions, 'entity' for specific
    entities, 'fast' for quick similarity search, 'hybrid' for combined approach
    """

    top_k: Annotated[int, PropertyInfo(alias="topK")]
    """Maximum number of results to return"""
