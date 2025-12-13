# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1RetrieveExecutionResponse"]


class V1RetrieveExecutionResponse(BaseModel):
    id: Optional[str] = None

    completed_at: Optional[str] = FieldInfo(alias="completedAt", default=None)

    duration_ms: Optional[int] = FieldInfo(alias="durationMs", default=None)

    error: Optional[str] = None

    input: Optional[object] = None

    output: Optional[object] = None

    started_at: Optional[str] = FieldInfo(alias="startedAt", default=None)

    status: Optional[str] = None

    trigger_type: Optional[str] = FieldInfo(alias="triggerType", default=None)

    workflow_id: Optional[str] = FieldInfo(alias="workflowId", default=None)
