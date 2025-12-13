# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1ListExecutionsResponse", "Execution"]


class Execution(BaseModel):
    id: Optional[str] = None

    completed_at: Optional[str] = FieldInfo(alias="completedAt", default=None)

    duration_ms: Optional[int] = FieldInfo(alias="durationMs", default=None)

    started_at: Optional[str] = FieldInfo(alias="startedAt", default=None)

    status: Optional[str] = None

    trigger_type: Optional[str] = FieldInfo(alias="triggerType", default=None)


class V1ListExecutionsResponse(BaseModel):
    executions: Optional[List[Execution]] = None
