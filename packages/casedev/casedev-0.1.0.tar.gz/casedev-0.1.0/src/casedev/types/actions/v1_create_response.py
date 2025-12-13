# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1CreateResponse"]


class V1CreateResponse(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)

    definition: Optional[object] = None

    description: Optional[str] = None

    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)

    name: Optional[str] = None

    organization_id: Optional[str] = FieldInfo(alias="organizationId", default=None)

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)

    version: Optional[float] = None

    webhook_endpoint_id: Optional[str] = FieldInfo(alias="webhookEndpointId", default=None)
