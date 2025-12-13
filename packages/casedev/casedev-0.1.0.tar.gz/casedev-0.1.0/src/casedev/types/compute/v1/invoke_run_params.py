# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["InvokeRunParams"]


class InvokeRunParams(TypedDict, total=False):
    input: Required[Dict[str, object]]
    """Input data to pass to the function"""

    async_: Annotated[bool, PropertyInfo(alias="async")]
    """If true, returns immediately with run ID for background execution"""

    function_suffix: Annotated[Literal["_modal", "_task", "_web", "_server"], PropertyInfo(alias="functionSuffix")]
    """Override the auto-detected function suffix"""
