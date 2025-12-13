# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1UpdateParams"]


class V1UpdateParams(TypedDict, total=False):
    description: str

    edges: Iterable[object]

    name: str

    nodes: Iterable[object]

    trigger_config: Annotated[object, PropertyInfo(alias="triggerConfig")]

    trigger_type: Annotated[Literal["manual", "webhook", "schedule", "vault_upload"], PropertyInfo(alias="triggerType")]

    visibility: Literal["private", "org", "public"]
