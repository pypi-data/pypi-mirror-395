# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["VaultIngestResponse"]


class VaultIngestResponse(BaseModel):
    enable_graph_rag: bool = FieldInfo(alias="enableGraphRAG")
    """Whether GraphRAG is enabled for this vault"""

    message: str
    """Human-readable status message"""

    object_id: str = FieldInfo(alias="objectId")
    """ID of the vault object being processed"""

    status: Literal["processing"]
    """Current ingestion status"""

    workflow_id: str = FieldInfo(alias="workflowId")
    """Workflow run ID for tracking progress"""
