# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1DeployResponse"]


class V1DeployResponse(BaseModel):
    message: Optional[str] = None

    success: Optional[bool] = None

    webhook_secret: Optional[str] = FieldInfo(alias="webhookSecret", default=None)
    """Only returned once - save this!"""

    webhook_url: Optional[str] = FieldInfo(alias="webhookUrl", default=None)
