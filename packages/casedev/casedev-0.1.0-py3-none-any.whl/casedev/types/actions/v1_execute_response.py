# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["V1ExecuteResponse"]


class V1ExecuteResponse(BaseModel):
    duration_ms: Optional[float] = None
    """Execution duration in milliseconds (only for completed executions)"""

    execution_id: Optional[str] = None
    """Unique identifier for this execution"""

    message: Optional[str] = None
    """Human-readable status message"""

    output: Optional[Dict[str, object]] = None
    """Final output (only for synchronous/completed executions)"""

    status: Optional[Literal["completed", "running"]] = None
    """Current status of the execution"""

    step_results: Optional[List[Dict[str, object]]] = None
    """Results from each step (only for synchronous/completed executions)"""

    webhook_configured: Optional[bool] = None
    """Whether webhook notifications are configured"""
