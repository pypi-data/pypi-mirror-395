# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SecretRetrieveGroupParams"]


class SecretRetrieveGroupParams(TypedDict, total=False):
    env: str
    """Environment name. If not specified, uses the default environment"""
