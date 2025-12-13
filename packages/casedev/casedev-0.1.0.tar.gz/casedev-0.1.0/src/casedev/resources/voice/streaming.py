# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NoneType, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["StreamingResource", "AsyncStreamingResource"]


class StreamingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StreamingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return StreamingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StreamingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return StreamingResourceWithStreamingResponse(self)

    def get_url(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Returns the WebSocket URL and connection details for real-time audio
        transcription. The returned URL can be used to establish a WebSocket connection
        for streaming audio data and receiving transcribed text in real-time.

        **Audio Requirements:**

        - Sample Rate: 16kHz
        - Encoding: PCM 16-bit little-endian
        - Channels: Mono (1 channel)

        **Pricing:** $0.30 per minute ($18.00 per hour)
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/voice/streaming/url",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncStreamingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStreamingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStreamingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStreamingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncStreamingResourceWithStreamingResponse(self)

    async def get_url(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Returns the WebSocket URL and connection details for real-time audio
        transcription. The returned URL can be used to establish a WebSocket connection
        for streaming audio data and receiving transcribed text in real-time.

        **Audio Requirements:**

        - Sample Rate: 16kHz
        - Encoding: PCM 16-bit little-endian
        - Channels: Mono (1 channel)

        **Pricing:** $0.30 per minute ($18.00 per hour)
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/voice/streaming/url",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class StreamingResourceWithRawResponse:
    def __init__(self, streaming: StreamingResource) -> None:
        self._streaming = streaming

        self.get_url = to_raw_response_wrapper(
            streaming.get_url,
        )


class AsyncStreamingResourceWithRawResponse:
    def __init__(self, streaming: AsyncStreamingResource) -> None:
        self._streaming = streaming

        self.get_url = async_to_raw_response_wrapper(
            streaming.get_url,
        )


class StreamingResourceWithStreamingResponse:
    def __init__(self, streaming: StreamingResource) -> None:
        self._streaming = streaming

        self.get_url = to_streamed_response_wrapper(
            streaming.get_url,
        )


class AsyncStreamingResourceWithStreamingResponse:
    def __init__(self, streaming: AsyncStreamingResource) -> None:
        self._streaming = streaming

        self.get_url = async_to_streamed_response_wrapper(
            streaming.get_url,
        )
