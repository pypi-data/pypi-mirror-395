# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["V1ExecuteParams", "Options"]


class V1ExecuteParams(TypedDict, total=False):
    input: Required[object]
    """Input data for the workflow (structure varies by workflow type)"""

    options: Options


class Options(TypedDict, total=False):
    format: Literal["json", "text"]
    """Output format preference"""

    model: str
    """LLM model to use for processing"""
