# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VaultCreateParams"]


class VaultCreateParams(TypedDict, total=False):
    name: Required[str]
    """Display name for the vault"""

    description: str
    """Optional description of the vault's purpose"""

    enable_graph: Annotated[bool, PropertyInfo(alias="enableGraph")]
    """Enable knowledge graph for entity relationship mapping"""
