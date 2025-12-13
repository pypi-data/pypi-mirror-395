# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["FunctionGetLogsParams"]


class FunctionGetLogsParams(TypedDict, total=False):
    tail: int
    """Number of log lines to retrieve (default 200, max 1000)"""
