# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["V1CreateEmbeddingParams"]


class V1CreateEmbeddingParams(TypedDict, total=False):
    input: Required[Union[str, SequenceNotStr[str]]]
    """Text or array of texts to create embeddings for"""

    model: Required[str]
    """Embedding model to use (e.g., text-embedding-ada-002, text-embedding-3-small)"""

    dimensions: int
    """Number of dimensions for the embeddings (model-specific)"""

    encoding_format: Literal["float", "base64"]
    """Format for returned embeddings"""

    user: str
    """Unique identifier for the end-user"""
