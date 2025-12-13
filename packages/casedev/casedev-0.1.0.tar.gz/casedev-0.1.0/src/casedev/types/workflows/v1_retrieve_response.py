# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1RetrieveResponse"]


class V1RetrieveResponse(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    deployed_at: Optional[str] = FieldInfo(alias="deployedAt", default=None)

    deployment_url: Optional[str] = FieldInfo(alias="deploymentUrl", default=None)

    description: Optional[str] = None

    edges: Optional[List[object]] = None

    name: Optional[str] = None

    nodes: Optional[List[object]] = None

    trigger_config: Optional[object] = FieldInfo(alias="triggerConfig", default=None)

    trigger_type: Optional[str] = FieldInfo(alias="triggerType", default=None)

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)

    visibility: Optional[str] = None
