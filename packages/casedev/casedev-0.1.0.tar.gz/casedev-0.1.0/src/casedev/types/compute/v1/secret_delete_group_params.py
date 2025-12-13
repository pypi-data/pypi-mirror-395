# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SecretDeleteGroupParams"]


class SecretDeleteGroupParams(TypedDict, total=False):
    env: str
    """Environment name. If not provided, uses the default environment"""

    key: str
    """Specific key to delete within the group.

    If not provided, the entire group is deleted
    """
