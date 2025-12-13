# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["V1ListParams"]


class V1ListParams(TypedDict, total=False):
    category: str
    """Filter workflows by category (e.g., 'legal', 'compliance', 'contract')"""

    limit: int
    """Maximum number of workflows to return"""

    offset: int
    """Number of workflows to skip for pagination"""

    published: bool
    """Include only published workflows"""

    sub_category: str
    """
    Filter workflows by subcategory (e.g., 'due-diligence', 'litigation', 'mergers')
    """

    type: str
    """
    Filter workflows by type (e.g., 'document-review', 'contract-analysis',
    'compliance-check')
    """
