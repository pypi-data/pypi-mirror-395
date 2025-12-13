# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["V1ExecuteParams"]


class V1ExecuteParams(TypedDict, total=False):
    input: Required[Dict[str, object]]
    """Input data for the action execution"""

    webhook_id: str
    """Optional webhook endpoint ID to override the action's default webhook"""
