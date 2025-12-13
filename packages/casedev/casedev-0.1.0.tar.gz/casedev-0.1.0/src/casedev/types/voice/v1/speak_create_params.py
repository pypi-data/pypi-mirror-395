# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SpeakCreateParams", "VoiceSettings"]


class SpeakCreateParams(TypedDict, total=False):
    text: Required[str]
    """Text to convert to speech"""

    apply_text_normalization: bool
    """Apply automatic text normalization"""

    enable_logging: bool
    """Enable request logging"""

    language_code: str
    """Language code for multilingual models"""

    model_id: Literal["eleven_multilingual_v2", "eleven_turbo_v2", "eleven_monolingual_v1"]
    """ElevenLabs model ID"""

    next_text: str
    """Next context for better pronunciation"""

    optimize_streaming_latency: int
    """Optimize for streaming latency (0-4)"""

    output_format: Literal["mp3_44100_128", "mp3_44100_192", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"]
    """Audio output format"""

    previous_text: str
    """Previous context for better pronunciation"""

    seed: int
    """Seed for reproducible generation"""

    voice_id: str
    """ElevenLabs voice ID (defaults to Rachel - professional, clear)"""

    voice_settings: VoiceSettings
    """Voice customization settings"""


class VoiceSettings(TypedDict, total=False):
    similarity_boost: float
    """Similarity boost (0-1)"""

    stability: float
    """Voice stability (0-1)"""

    style: float
    """Style exaggeration (0-1)"""

    use_speaker_boost: bool
    """Enable speaker boost"""
