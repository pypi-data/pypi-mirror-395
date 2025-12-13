# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["V1RetrieveResearchParams"]


class V1RetrieveResearchParams(TypedDict, total=False):
    events: str
    """Filter specific event types for streaming"""

    stream: bool
    """Enable streaming for real-time updates"""
