# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["V1ListExecutionsParams"]


class V1ListExecutionsParams(TypedDict, total=False):
    limit: int

    status: Literal["pending", "running", "completed", "failed", "cancelled"]
