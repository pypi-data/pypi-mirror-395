# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1ListResponse", "Workflow"]


class Workflow(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    deployed_at: Optional[str] = FieldInfo(alias="deployedAt", default=None)

    description: Optional[str] = None

    name: Optional[str] = None

    trigger_type: Optional[str] = FieldInfo(alias="triggerType", default=None)

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)

    visibility: Optional[str] = None


class V1ListResponse(BaseModel):
    limit: Optional[int] = None

    offset: Optional[int] = None

    total: Optional[int] = None

    workflows: Optional[List[Workflow]] = None
