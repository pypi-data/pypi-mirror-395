# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1ResearchParams"]


class V1ResearchParams(TypedDict, total=False):
    instructions: Required[str]
    """Research instructions or query"""

    model: Literal["fast", "normal", "pro"]
    """Research quality level - fast (quick), normal (balanced), pro (comprehensive)"""

    output_schema: Annotated[object, PropertyInfo(alias="outputSchema")]
    """Optional JSON schema to structure the research output"""

    query: str
    """Alias for instructions (for convenience)"""
