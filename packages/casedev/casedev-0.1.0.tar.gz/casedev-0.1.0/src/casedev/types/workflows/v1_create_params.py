# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1CreateParams"]


class V1CreateParams(TypedDict, total=False):
    name: Required[str]
    """Workflow name"""

    description: str
    """Workflow description"""

    edges: Iterable[object]
    """React Flow edges"""

    nodes: Iterable[object]
    """React Flow nodes"""

    trigger_config: Annotated[object, PropertyInfo(alias="triggerConfig")]
    """Trigger configuration"""

    trigger_type: Annotated[Literal["manual", "webhook", "schedule", "vault_upload"], PropertyInfo(alias="triggerType")]

    visibility: Literal["private", "org", "public"]
    """Workflow visibility"""
