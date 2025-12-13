# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["SecretUpdateGroupParams"]


class SecretUpdateGroupParams(TypedDict, total=False):
    secrets: Required[Dict[str, str]]
    """Key-value pairs of secrets to set"""

    env: str
    """Environment name (optional, uses default if not specified)"""
