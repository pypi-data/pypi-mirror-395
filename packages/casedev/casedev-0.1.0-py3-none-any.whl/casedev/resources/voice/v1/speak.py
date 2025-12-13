# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.voice.v1 import speak_create_params, speak_stream_params

__all__ = ["SpeakResource", "AsyncSpeakResource"]


class SpeakResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpeakResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return SpeakResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpeakResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return SpeakResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        text: str,
        apply_text_normalization: bool | Omit = omit,
        enable_logging: bool | Omit = omit,
        language_code: str | Omit = omit,
        model_id: Literal["eleven_multilingual_v2", "eleven_turbo_v2", "eleven_monolingual_v1"] | Omit = omit,
        next_text: str | Omit = omit,
        optimize_streaming_latency: int | Omit = omit,
        output_format: Literal["mp3_44100_128", "mp3_44100_192", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"]
        | Omit = omit,
        previous_text: str | Omit = omit,
        seed: int | Omit = omit,
        voice_id: str | Omit = omit,
        voice_settings: speak_create_params.VoiceSettings | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """Convert text to natural-sounding audio using ElevenLabs voices.

        Ideal for
        creating audio summaries of legal documents, client presentations, or
        accessibility features. Supports multiple languages and voice customization.

        Args:
          text: Text to convert to speech

          apply_text_normalization: Apply automatic text normalization

          enable_logging: Enable request logging

          language_code: Language code for multilingual models

          model_id: ElevenLabs model ID

          next_text: Next context for better pronunciation

          optimize_streaming_latency: Optimize for streaming latency (0-4)

          output_format: Audio output format

          previous_text: Previous context for better pronunciation

          seed: Seed for reproducible generation

          voice_id: ElevenLabs voice ID (defaults to Rachel - professional, clear)

          voice_settings: Voice customization settings

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return self._post(
            "/voice/v1/speak",
            body=maybe_transform(
                {
                    "text": text,
                    "apply_text_normalization": apply_text_normalization,
                    "enable_logging": enable_logging,
                    "language_code": language_code,
                    "model_id": model_id,
                    "next_text": next_text,
                    "optimize_streaming_latency": optimize_streaming_latency,
                    "output_format": output_format,
                    "previous_text": previous_text,
                    "seed": seed,
                    "voice_id": voice_id,
                    "voice_settings": voice_settings,
                },
                speak_create_params.SpeakCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def stream(
        self,
        *,
        text: str,
        apply_text_normalization: bool | Omit = omit,
        enable_logging: bool | Omit = omit,
        language_code: str | Omit = omit,
        model_id: Literal[
            "eleven_monolingual_v1", "eleven_multilingual_v1", "eleven_multilingual_v2", "eleven_turbo_v2"
        ]
        | Omit = omit,
        next_text: str | Omit = omit,
        optimize_streaming_latency: int | Omit = omit,
        output_format: Literal["mp3_44100_128", "mp3_22050_32", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"]
        | Omit = omit,
        previous_text: str | Omit = omit,
        seed: int | Omit = omit,
        voice_id: str | Omit = omit,
        voice_settings: speak_stream_params.VoiceSettings | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """
        Convert text to speech using ElevenLabs AI voices with streaming for real-time
        playback. Returns audio data as an MP3 stream for immediate playback with
        minimal latency. Perfect for legal document narration, client presentations, or
        accessibility features.

        Args:
          text: Text to convert to speech

          apply_text_normalization: Apply text normalization

          enable_logging: Enable request logging

          language_code: Language code (e.g., 'en', 'es', 'fr')

          model_id: TTS model to use

          next_text: Next text for context

          optimize_streaming_latency: Optimize for streaming latency (0-4)

          output_format: Audio output format

          previous_text: Previous text for context

          seed: Random seed for reproducible generation

          voice_id: ElevenLabs voice ID (defaults to Rachel for professional clarity)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return self._post(
            "/voice/v1/speak/stream",
            body=maybe_transform(
                {
                    "text": text,
                    "apply_text_normalization": apply_text_normalization,
                    "enable_logging": enable_logging,
                    "language_code": language_code,
                    "model_id": model_id,
                    "next_text": next_text,
                    "optimize_streaming_latency": optimize_streaming_latency,
                    "output_format": output_format,
                    "previous_text": previous_text,
                    "seed": seed,
                    "voice_id": voice_id,
                    "voice_settings": voice_settings,
                },
                speak_stream_params.SpeakStreamParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncSpeakResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpeakResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSpeakResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpeakResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncSpeakResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        text: str,
        apply_text_normalization: bool | Omit = omit,
        enable_logging: bool | Omit = omit,
        language_code: str | Omit = omit,
        model_id: Literal["eleven_multilingual_v2", "eleven_turbo_v2", "eleven_monolingual_v1"] | Omit = omit,
        next_text: str | Omit = omit,
        optimize_streaming_latency: int | Omit = omit,
        output_format: Literal["mp3_44100_128", "mp3_44100_192", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"]
        | Omit = omit,
        previous_text: str | Omit = omit,
        seed: int | Omit = omit,
        voice_id: str | Omit = omit,
        voice_settings: speak_create_params.VoiceSettings | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """Convert text to natural-sounding audio using ElevenLabs voices.

        Ideal for
        creating audio summaries of legal documents, client presentations, or
        accessibility features. Supports multiple languages and voice customization.

        Args:
          text: Text to convert to speech

          apply_text_normalization: Apply automatic text normalization

          enable_logging: Enable request logging

          language_code: Language code for multilingual models

          model_id: ElevenLabs model ID

          next_text: Next context for better pronunciation

          optimize_streaming_latency: Optimize for streaming latency (0-4)

          output_format: Audio output format

          previous_text: Previous context for better pronunciation

          seed: Seed for reproducible generation

          voice_id: ElevenLabs voice ID (defaults to Rachel - professional, clear)

          voice_settings: Voice customization settings

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return await self._post(
            "/voice/v1/speak",
            body=await async_maybe_transform(
                {
                    "text": text,
                    "apply_text_normalization": apply_text_normalization,
                    "enable_logging": enable_logging,
                    "language_code": language_code,
                    "model_id": model_id,
                    "next_text": next_text,
                    "optimize_streaming_latency": optimize_streaming_latency,
                    "output_format": output_format,
                    "previous_text": previous_text,
                    "seed": seed,
                    "voice_id": voice_id,
                    "voice_settings": voice_settings,
                },
                speak_create_params.SpeakCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def stream(
        self,
        *,
        text: str,
        apply_text_normalization: bool | Omit = omit,
        enable_logging: bool | Omit = omit,
        language_code: str | Omit = omit,
        model_id: Literal[
            "eleven_monolingual_v1", "eleven_multilingual_v1", "eleven_multilingual_v2", "eleven_turbo_v2"
        ]
        | Omit = omit,
        next_text: str | Omit = omit,
        optimize_streaming_latency: int | Omit = omit,
        output_format: Literal["mp3_44100_128", "mp3_22050_32", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"]
        | Omit = omit,
        previous_text: str | Omit = omit,
        seed: int | Omit = omit,
        voice_id: str | Omit = omit,
        voice_settings: speak_stream_params.VoiceSettings | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """
        Convert text to speech using ElevenLabs AI voices with streaming for real-time
        playback. Returns audio data as an MP3 stream for immediate playback with
        minimal latency. Perfect for legal document narration, client presentations, or
        accessibility features.

        Args:
          text: Text to convert to speech

          apply_text_normalization: Apply text normalization

          enable_logging: Enable request logging

          language_code: Language code (e.g., 'en', 'es', 'fr')

          model_id: TTS model to use

          next_text: Next text for context

          optimize_streaming_latency: Optimize for streaming latency (0-4)

          output_format: Audio output format

          previous_text: Previous text for context

          seed: Random seed for reproducible generation

          voice_id: ElevenLabs voice ID (defaults to Rachel for professional clarity)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return await self._post(
            "/voice/v1/speak/stream",
            body=await async_maybe_transform(
                {
                    "text": text,
                    "apply_text_normalization": apply_text_normalization,
                    "enable_logging": enable_logging,
                    "language_code": language_code,
                    "model_id": model_id,
                    "next_text": next_text,
                    "optimize_streaming_latency": optimize_streaming_latency,
                    "output_format": output_format,
                    "previous_text": previous_text,
                    "seed": seed,
                    "voice_id": voice_id,
                    "voice_settings": voice_settings,
                },
                speak_stream_params.SpeakStreamParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class SpeakResourceWithRawResponse:
    def __init__(self, speak: SpeakResource) -> None:
        self._speak = speak

        self.create = to_custom_raw_response_wrapper(
            speak.create,
            BinaryAPIResponse,
        )
        self.stream = to_custom_raw_response_wrapper(
            speak.stream,
            BinaryAPIResponse,
        )


class AsyncSpeakResourceWithRawResponse:
    def __init__(self, speak: AsyncSpeakResource) -> None:
        self._speak = speak

        self.create = async_to_custom_raw_response_wrapper(
            speak.create,
            AsyncBinaryAPIResponse,
        )
        self.stream = async_to_custom_raw_response_wrapper(
            speak.stream,
            AsyncBinaryAPIResponse,
        )


class SpeakResourceWithStreamingResponse:
    def __init__(self, speak: SpeakResource) -> None:
        self._speak = speak

        self.create = to_custom_streamed_response_wrapper(
            speak.create,
            StreamedBinaryAPIResponse,
        )
        self.stream = to_custom_streamed_response_wrapper(
            speak.stream,
            StreamedBinaryAPIResponse,
        )


class AsyncSpeakResourceWithStreamingResponse:
    def __init__(self, speak: AsyncSpeakResource) -> None:
        self._speak = speak

        self.create = async_to_custom_streamed_response_wrapper(
            speak.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.stream = async_to_custom_streamed_response_wrapper(
            speak.stream,
            AsyncStreamedBinaryAPIResponse,
        )
