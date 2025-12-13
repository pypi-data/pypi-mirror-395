# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChatCreateCompletionParams", "Message"]


class ChatCreateCompletionParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]
    """List of messages comprising the conversation"""

    frequency_penalty: float
    """Frequency penalty parameter"""

    max_tokens: int
    """Maximum number of tokens to generate"""

    model: str
    """Model to use for completion. Defaults to casemark-core-1 if not specified"""

    presence_penalty: float
    """Presence penalty parameter"""

    stream: bool
    """Whether to stream back partial progress"""

    temperature: float
    """Sampling temperature between 0 and 2"""

    top_p: float
    """Nucleus sampling parameter"""


class Message(TypedDict, total=False):
    content: str
    """The contents of the message"""

    role: Literal["system", "user", "assistant"]
    """The role of the message author"""
