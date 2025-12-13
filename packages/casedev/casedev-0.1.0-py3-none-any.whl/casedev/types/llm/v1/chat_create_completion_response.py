# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ...._models import BaseModel

__all__ = ["ChatCreateCompletionResponse", "Choice", "ChoiceMessage", "Usage"]


class ChoiceMessage(BaseModel):
    content: Optional[str] = None

    role: Optional[str] = None


class Choice(BaseModel):
    finish_reason: Optional[str] = None

    index: Optional[int] = None

    message: Optional[ChoiceMessage] = None


class Usage(BaseModel):
    completion_tokens: Optional[int] = None

    cost: Optional[float] = None
    """Cost in USD"""

    prompt_tokens: Optional[int] = None

    total_tokens: Optional[int] = None


class ChatCreateCompletionResponse(BaseModel):
    id: Optional[str] = None
    """Unique identifier for the completion"""

    choices: Optional[List[Choice]] = None

    created: Optional[int] = None
    """Unix timestamp of completion creation"""

    model: Optional[str] = None
    """Model used for completion"""

    object: Optional[str] = None

    usage: Optional[Usage] = None
