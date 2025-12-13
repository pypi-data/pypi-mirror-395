# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1ExecuteResponse"]


class V1ExecuteResponse(BaseModel):
    duration: Optional[int] = None

    error: Optional[str] = None

    execution_id: Optional[str] = FieldInfo(alias="executionId", default=None)

    outputs: Optional[object] = None

    status: Optional[Literal["completed", "failed"]] = None
