# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TranscriptionCreateParams"]


class TranscriptionCreateParams(TypedDict, total=False):
    audio_url: Required[str]
    """URL of the audio file to transcribe"""

    auto_highlights: bool
    """Automatically extract key phrases and topics"""

    content_safety_labels: bool
    """Enable content moderation and safety labeling"""

    format_text: bool
    """Format text with proper capitalization"""

    language_code: str
    """Language code (e.g., 'en_us', 'es', 'fr').

    If not specified, language will be auto-detected
    """

    language_detection: bool
    """Enable automatic language detection"""

    punctuate: bool
    """Add punctuation to the transcript"""

    speaker_labels: bool
    """Enable speaker identification and labeling"""
