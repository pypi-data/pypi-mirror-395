# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["TemplateListParams"]


class TemplateListParams(TypedDict, total=False):
    type: str
    """Filter templates by type (e.g., contract, pleading, letter)"""
