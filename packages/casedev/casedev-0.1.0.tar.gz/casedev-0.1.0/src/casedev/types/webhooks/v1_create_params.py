# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["V1CreateParams"]


class V1CreateParams(TypedDict, total=False):
    events: Required[SequenceNotStr[str]]
    """Array of event types to subscribe to"""

    url: Required[str]
    """HTTPS URL where webhook events will be sent"""

    description: str
    """Optional description for the webhook"""
