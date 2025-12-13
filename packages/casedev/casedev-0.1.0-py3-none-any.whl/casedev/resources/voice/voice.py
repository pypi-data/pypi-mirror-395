# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .v1.v1 import (
    V1Resource,
    AsyncV1Resource,
    V1ResourceWithRawResponse,
    AsyncV1ResourceWithRawResponse,
    V1ResourceWithStreamingResponse,
    AsyncV1ResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .streaming import (
    StreamingResource,
    AsyncStreamingResource,
    StreamingResourceWithRawResponse,
    AsyncStreamingResourceWithRawResponse,
    StreamingResourceWithStreamingResponse,
    AsyncStreamingResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .transcription import (
    TranscriptionResource,
    AsyncTranscriptionResource,
    TranscriptionResourceWithRawResponse,
    AsyncTranscriptionResourceWithRawResponse,
    TranscriptionResourceWithStreamingResponse,
    AsyncTranscriptionResourceWithStreamingResponse,
)

__all__ = ["VoiceResource", "AsyncVoiceResource"]


class VoiceResource(SyncAPIResource):
    @cached_property
    def streaming(self) -> StreamingResource:
        return StreamingResource(self._client)

    @cached_property
    def transcription(self) -> TranscriptionResource:
        return TranscriptionResource(self._client)

    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> VoiceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return VoiceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VoiceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return VoiceResourceWithStreamingResponse(self)


class AsyncVoiceResource(AsyncAPIResource):
    @cached_property
    def streaming(self) -> AsyncStreamingResource:
        return AsyncStreamingResource(self._client)

    @cached_property
    def transcription(self) -> AsyncTranscriptionResource:
        return AsyncTranscriptionResource(self._client)

    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVoiceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVoiceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVoiceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncVoiceResourceWithStreamingResponse(self)


class VoiceResourceWithRawResponse:
    def __init__(self, voice: VoiceResource) -> None:
        self._voice = voice

    @cached_property
    def streaming(self) -> StreamingResourceWithRawResponse:
        return StreamingResourceWithRawResponse(self._voice.streaming)

    @cached_property
    def transcription(self) -> TranscriptionResourceWithRawResponse:
        return TranscriptionResourceWithRawResponse(self._voice.transcription)

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._voice.v1)


class AsyncVoiceResourceWithRawResponse:
    def __init__(self, voice: AsyncVoiceResource) -> None:
        self._voice = voice

    @cached_property
    def streaming(self) -> AsyncStreamingResourceWithRawResponse:
        return AsyncStreamingResourceWithRawResponse(self._voice.streaming)

    @cached_property
    def transcription(self) -> AsyncTranscriptionResourceWithRawResponse:
        return AsyncTranscriptionResourceWithRawResponse(self._voice.transcription)

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._voice.v1)


class VoiceResourceWithStreamingResponse:
    def __init__(self, voice: VoiceResource) -> None:
        self._voice = voice

    @cached_property
    def streaming(self) -> StreamingResourceWithStreamingResponse:
        return StreamingResourceWithStreamingResponse(self._voice.streaming)

    @cached_property
    def transcription(self) -> TranscriptionResourceWithStreamingResponse:
        return TranscriptionResourceWithStreamingResponse(self._voice.transcription)

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._voice.v1)


class AsyncVoiceResourceWithStreamingResponse:
    def __init__(self, voice: AsyncVoiceResource) -> None:
        self._voice = voice

    @cached_property
    def streaming(self) -> AsyncStreamingResourceWithStreamingResponse:
        return AsyncStreamingResourceWithStreamingResponse(self._voice.streaming)

    @cached_property
    def transcription(self) -> AsyncTranscriptionResourceWithStreamingResponse:
        return AsyncTranscriptionResourceWithStreamingResponse(self._voice.transcription)

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._voice.v1)
