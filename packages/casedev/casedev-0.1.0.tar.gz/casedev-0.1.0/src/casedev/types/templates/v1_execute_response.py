# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["V1ExecuteResponse", "Usage"]


class Usage(BaseModel):
    completion_tokens: Optional[int] = None

    cost: Optional[float] = None
    """Total cost in USD"""

    prompt_tokens: Optional[int] = None

    total_tokens: Optional[int] = None


class V1ExecuteResponse(BaseModel):
    result: Optional[object] = None
    """Workflow output (structure varies by workflow type)"""

    status: Optional[Literal["completed", "failed"]] = None

    usage: Optional[Usage] = None

    workflow_name: Optional[str] = None
    """Name of the executed workflow"""
