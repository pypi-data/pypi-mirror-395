# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["V1AnswerParams"]


class V1AnswerParams(TypedDict, total=False):
    query: Required[str]
    """The question or topic to research and answer"""

    exclude_domains: Annotated[SequenceNotStr[str], PropertyInfo(alias="excludeDomains")]
    """Exclude these domains from search"""

    include_domains: Annotated[SequenceNotStr[str], PropertyInfo(alias="includeDomains")]
    """Only search within these domains"""

    max_tokens: Annotated[int, PropertyInfo(alias="maxTokens")]
    """Maximum tokens for LLM response"""

    model: str
    """LLM model to use when useCustomLLM is true"""

    num_results: Annotated[int, PropertyInfo(alias="numResults")]
    """Number of search results to consider"""

    search_type: Annotated[Literal["auto", "web", "news", "academic"], PropertyInfo(alias="searchType")]
    """Type of search to perform"""

    stream: bool
    """Stream the response (only for native provider answers)"""

    temperature: float
    """LLM temperature for answer generation"""

    text: bool
    """Include text content in response"""

    use_custom_llm: Annotated[bool, PropertyInfo(alias="useCustomLLM")]
    """Use Case.dev LLM for answer generation instead of provider's native answer"""
