# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.voice import transcription_create_params
from ..._base_client import make_request_options
from ...types.voice.transcription_retrieve_response import TranscriptionRetrieveResponse

__all__ = ["TranscriptionResource", "AsyncTranscriptionResource"]


class TranscriptionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TranscriptionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return TranscriptionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TranscriptionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return TranscriptionResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        audio_url: str,
        auto_highlights: bool | Omit = omit,
        content_safety_labels: bool | Omit = omit,
        format_text: bool | Omit = omit,
        language_code: str | Omit = omit,
        language_detection: bool | Omit = omit,
        punctuate: bool | Omit = omit,
        speaker_labels: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Creates an asynchronous transcription job for audio files.

        Supports various
        audio formats and advanced features like speaker identification, content
        moderation, and automatic highlights. Returns a job ID for checking
        transcription status and retrieving results.

        Args:
          audio_url: URL of the audio file to transcribe

          auto_highlights: Automatically extract key phrases and topics

          content_safety_labels: Enable content moderation and safety labeling

          format_text: Format text with proper capitalization

          language_code: Language code (e.g., 'en_us', 'es', 'fr'). If not specified, language will be
              auto-detected

          language_detection: Enable automatic language detection

          punctuate: Add punctuation to the transcript

          speaker_labels: Enable speaker identification and labeling

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/voice/transcription",
            body=maybe_transform(
                {
                    "audio_url": audio_url,
                    "auto_highlights": auto_highlights,
                    "content_safety_labels": content_safety_labels,
                    "format_text": format_text,
                    "language_code": language_code,
                    "language_detection": language_detection,
                    "punctuate": punctuate,
                    "speaker_labels": speaker_labels,
                },
                transcription_create_params.TranscriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TranscriptionRetrieveResponse:
        """Retrieve the status and result of an audio transcription job.

        Returns the
        transcription text when complete, or status information for pending jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/voice/transcription/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TranscriptionRetrieveResponse,
        )


class AsyncTranscriptionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTranscriptionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTranscriptionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTranscriptionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncTranscriptionResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        audio_url: str,
        auto_highlights: bool | Omit = omit,
        content_safety_labels: bool | Omit = omit,
        format_text: bool | Omit = omit,
        language_code: str | Omit = omit,
        language_detection: bool | Omit = omit,
        punctuate: bool | Omit = omit,
        speaker_labels: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Creates an asynchronous transcription job for audio files.

        Supports various
        audio formats and advanced features like speaker identification, content
        moderation, and automatic highlights. Returns a job ID for checking
        transcription status and retrieving results.

        Args:
          audio_url: URL of the audio file to transcribe

          auto_highlights: Automatically extract key phrases and topics

          content_safety_labels: Enable content moderation and safety labeling

          format_text: Format text with proper capitalization

          language_code: Language code (e.g., 'en_us', 'es', 'fr'). If not specified, language will be
              auto-detected

          language_detection: Enable automatic language detection

          punctuate: Add punctuation to the transcript

          speaker_labels: Enable speaker identification and labeling

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/voice/transcription",
            body=await async_maybe_transform(
                {
                    "audio_url": audio_url,
                    "auto_highlights": auto_highlights,
                    "content_safety_labels": content_safety_labels,
                    "format_text": format_text,
                    "language_code": language_code,
                    "language_detection": language_detection,
                    "punctuate": punctuate,
                    "speaker_labels": speaker_labels,
                },
                transcription_create_params.TranscriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TranscriptionRetrieveResponse:
        """Retrieve the status and result of an audio transcription job.

        Returns the
        transcription text when complete, or status information for pending jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/voice/transcription/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TranscriptionRetrieveResponse,
        )


class TranscriptionResourceWithRawResponse:
    def __init__(self, transcription: TranscriptionResource) -> None:
        self._transcription = transcription

        self.create = to_raw_response_wrapper(
            transcription.create,
        )
        self.retrieve = to_raw_response_wrapper(
            transcription.retrieve,
        )


class AsyncTranscriptionResourceWithRawResponse:
    def __init__(self, transcription: AsyncTranscriptionResource) -> None:
        self._transcription = transcription

        self.create = async_to_raw_response_wrapper(
            transcription.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            transcription.retrieve,
        )


class TranscriptionResourceWithStreamingResponse:
    def __init__(self, transcription: TranscriptionResource) -> None:
        self._transcription = transcription

        self.create = to_streamed_response_wrapper(
            transcription.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            transcription.retrieve,
        )


class AsyncTranscriptionResourceWithStreamingResponse:
    def __init__(self, transcription: AsyncTranscriptionResource) -> None:
        self._transcription = transcription

        self.create = async_to_streamed_response_wrapper(
            transcription.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            transcription.retrieve,
        )
