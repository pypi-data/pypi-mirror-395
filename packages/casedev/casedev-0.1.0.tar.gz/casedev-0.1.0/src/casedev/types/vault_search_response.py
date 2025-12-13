# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["VaultSearchResponse", "Chunk", "Source"]


class Chunk(BaseModel):
    score: Optional[float] = None

    source: Optional[str] = None

    text: Optional[str] = None


class Source(BaseModel):
    id: Optional[str] = None

    chunk_count: Optional[int] = FieldInfo(alias="chunkCount", default=None)

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)

    filename: Optional[str] = None

    ingestion_completed_at: Optional[datetime] = FieldInfo(alias="ingestionCompletedAt", default=None)

    page_count: Optional[int] = FieldInfo(alias="pageCount", default=None)

    text_length: Optional[int] = FieldInfo(alias="textLength", default=None)


class VaultSearchResponse(BaseModel):
    chunks: Optional[List[Chunk]] = None
    """Relevant text chunks with similarity scores"""

    method: Optional[str] = None
    """Search method used"""

    query: Optional[str] = None
    """Original search query"""

    response: Optional[str] = None
    """AI-generated answer based on search results (for global/entity methods)"""

    sources: Optional[List[Source]] = None

    vault_id: Optional[str] = None
    """ID of the searched vault"""
