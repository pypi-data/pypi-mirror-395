# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["TemplateCreateParams"]


class TemplateCreateParams(TypedDict, total=False):
    content: Required[str]
    """Template content with {{variable}} placeholders"""

    name: Required[str]
    """Template name"""

    type: Required[Literal["caption", "signature", "letterhead", "certificate", "footer", "custom"]]
    """Template type"""

    description: str
    """Template description"""

    styles: object
    """CSS styles for the template"""

    tags: SequenceNotStr[str]
    """Template tags for organization"""

    variables: SequenceNotStr[str]
    """Template variables (auto-detected if not provided)"""
