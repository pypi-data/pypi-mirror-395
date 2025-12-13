# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["TranscriptionRetrieveResponse", "Word"]


class Word(BaseModel):
    confidence: Optional[float] = None

    end: Optional[float] = None

    start: Optional[float] = None

    text: Optional[str] = None


class TranscriptionRetrieveResponse(BaseModel):
    id: str
    """Unique transcription job ID"""

    status: Literal["queued", "processing", "completed", "error"]
    """Current status of the transcription job"""

    audio_duration: Optional[float] = None
    """Duration of the audio file in seconds"""

    confidence: Optional[float] = None
    """Overall confidence score for the transcription"""

    error: Optional[str] = None
    """Error message (only present when status is error)"""

    text: Optional[str] = None
    """Full transcription text (only present when status is completed)"""

    words: Optional[List[Word]] = None
    """Word-level timestamps and confidence scores"""
