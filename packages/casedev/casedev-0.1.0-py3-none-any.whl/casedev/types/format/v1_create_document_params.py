# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1CreateDocumentParams", "Options", "OptionsComponent"]


class V1CreateDocumentParams(TypedDict, total=False):
    content: Required[str]
    """The source content to format"""

    output_format: Required[Literal["pdf", "docx", "html_preview"]]
    """Desired output format"""

    input_format: Literal["md", "json", "text"]
    """Format of the input content"""

    options: Options


class OptionsComponent(TypedDict, total=False):
    content: str
    """Inline template content"""

    styles: object
    """Custom styling options"""

    template_id: Annotated[str, PropertyInfo(alias="templateId")]
    """ID of saved template component"""

    variables: object
    """Variables for template interpolation"""


class Options(TypedDict, total=False):
    components: Iterable[OptionsComponent]
    """Template components with variables"""
