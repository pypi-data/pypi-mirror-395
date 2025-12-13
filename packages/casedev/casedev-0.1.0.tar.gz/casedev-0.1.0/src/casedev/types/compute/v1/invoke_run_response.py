# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["InvokeRunResponse", "SynchronousResponse", "AsynchronousResponse"]


class SynchronousResponse(BaseModel):
    duration: Optional[float] = None
    """Execution duration in milliseconds"""

    error: Optional[str] = None
    """Error message if status is failed"""

    output: Optional[object] = None
    """Function return value"""

    run_id: Optional[str] = FieldInfo(alias="runId", default=None)
    """Unique run identifier"""

    status: Optional[Literal["completed", "failed"]] = None


class AsynchronousResponse(BaseModel):
    logs_url: Optional[str] = FieldInfo(alias="logsUrl", default=None)
    """URL to check run status and logs"""

    run_id: Optional[str] = FieldInfo(alias="runId", default=None)
    """Unique run identifier"""

    status: Optional[Literal["running"]] = None


InvokeRunResponse: TypeAlias = Union[SynchronousResponse, AsynchronousResponse]
