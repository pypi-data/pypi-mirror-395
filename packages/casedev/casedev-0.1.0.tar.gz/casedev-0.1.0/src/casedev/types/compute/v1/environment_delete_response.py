# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["EnvironmentDeleteResponse"]


class EnvironmentDeleteResponse(BaseModel):
    message: str

    success: bool
