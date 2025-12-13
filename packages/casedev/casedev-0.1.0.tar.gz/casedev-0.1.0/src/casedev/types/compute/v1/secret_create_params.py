# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SecretCreateParams"]


class SecretCreateParams(TypedDict, total=False):
    name: Required[str]
    """Unique name for the secret group.

    Must contain only letters, numbers, hyphens, and underscores.
    """

    description: str
    """Optional description of the secret group's purpose"""

    env: str
    """Environment name where the secret group will be created.

    Uses default environment if not specified.
    """
