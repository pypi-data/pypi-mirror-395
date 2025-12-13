# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1UpdateResponse"]


class V1UpdateResponse(BaseModel):
    id: Optional[str] = None

    name: Optional[str] = None

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)
