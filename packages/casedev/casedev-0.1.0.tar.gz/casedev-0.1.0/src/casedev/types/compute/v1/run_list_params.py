# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["RunListParams"]


class RunListParams(TypedDict, total=False):
    env: str
    """Environment name to filter runs by"""

    function: str
    """Function name to filter runs by"""

    limit: int
    """Maximum number of runs to return (1-100, default: 50)"""
