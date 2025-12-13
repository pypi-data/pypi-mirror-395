# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypedDict

__all__ = ["V1CreateParams"]


class V1CreateParams(TypedDict, total=False):
    definition: Required[Union[str, object]]
    """Action definition in YAML string, JSON string, or JSON object format"""

    name: Required[str]
    """Unique name for the action"""

    description: str
    """Optional description of the action's purpose"""

    webhook_id: str
    """Optional webhook endpoint ID for action completion notifications"""
