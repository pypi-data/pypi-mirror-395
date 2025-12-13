# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .jobs import (
    JobsResource,
    AsyncJobsResource,
    JobsResourceWithRawResponse,
    AsyncJobsResourceWithRawResponse,
    JobsResourceWithStreamingResponse,
    AsyncJobsResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.convert import v1_process_params, v1_webhook_params
from ....types.convert.v1_process_response import V1ProcessResponse
from ....types.convert.v1_webhook_response import V1WebhookResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def jobs(self) -> JobsResource:
        return JobsResource(self._client)

    @cached_property
    def with_raw_response(self) -> V1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return V1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return V1ResourceWithStreamingResponse(self)

    def download(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """Download the converted M4A audio file from a completed FTR conversion job.

        The
        file is streamed directly to the client with appropriate headers for audio
        playback or download.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "audio/mp4", **(extra_headers or {})}
        return self._get(
            f"/convert/v1/download/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def process(
        self,
        *,
        input_url: str,
        callback_url: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ProcessResponse:
        """
        Submit an FTR (ForensicTech Recording) file for conversion to M4A audio format.
        This endpoint is commonly used to convert court recording files into standard
        audio formats for transcription or playback. The conversion is processed
        asynchronously - you'll receive a job ID to track the conversion status.

        **Supported Input**: FTR files via S3 presigned URLs **Output Format**: M4A
        audio **Processing**: Asynchronous with webhook callbacks

        Args:
          input_url: HTTPS URL to the FTR file (must be a valid S3 presigned URL)

          callback_url: Optional webhook URL to receive conversion completion notification

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/convert/v1/process",
            body=maybe_transform(
                {
                    "input_url": input_url,
                    "callback_url": callback_url,
                },
                v1_process_params.V1ProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ProcessResponse,
        )

    def webhook(
        self,
        *,
        job_id: str,
        status: Literal["completed", "failed"],
        error: str | Omit = omit,
        result: v1_webhook_params.Result | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1WebhookResponse:
        """
        Internal webhook endpoint that receives completion notifications from the Modal
        FTR converter service. This endpoint handles status updates for file conversion
        jobs, including success and failure notifications. Requires valid Bearer token
        authentication.

        Args:
          job_id: Unique identifier for the conversion job

          status: Status of the conversion job

          error: Error message for failed jobs

          result: Result data for completed jobs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/convert/v1/webhook",
            body=maybe_transform(
                {
                    "job_id": job_id,
                    "status": status,
                    "error": error,
                    "result": result,
                },
                v1_webhook_params.V1WebhookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1WebhookResponse,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def jobs(self) -> AsyncJobsResource:
        return AsyncJobsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncV1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncV1ResourceWithStreamingResponse(self)

    async def download(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """Download the converted M4A audio file from a completed FTR conversion job.

        The
        file is streamed directly to the client with appropriate headers for audio
        playback or download.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "audio/mp4", **(extra_headers or {})}
        return await self._get(
            f"/convert/v1/download/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def process(
        self,
        *,
        input_url: str,
        callback_url: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ProcessResponse:
        """
        Submit an FTR (ForensicTech Recording) file for conversion to M4A audio format.
        This endpoint is commonly used to convert court recording files into standard
        audio formats for transcription or playback. The conversion is processed
        asynchronously - you'll receive a job ID to track the conversion status.

        **Supported Input**: FTR files via S3 presigned URLs **Output Format**: M4A
        audio **Processing**: Asynchronous with webhook callbacks

        Args:
          input_url: HTTPS URL to the FTR file (must be a valid S3 presigned URL)

          callback_url: Optional webhook URL to receive conversion completion notification

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/convert/v1/process",
            body=await async_maybe_transform(
                {
                    "input_url": input_url,
                    "callback_url": callback_url,
                },
                v1_process_params.V1ProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ProcessResponse,
        )

    async def webhook(
        self,
        *,
        job_id: str,
        status: Literal["completed", "failed"],
        error: str | Omit = omit,
        result: v1_webhook_params.Result | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1WebhookResponse:
        """
        Internal webhook endpoint that receives completion notifications from the Modal
        FTR converter service. This endpoint handles status updates for file conversion
        jobs, including success and failure notifications. Requires valid Bearer token
        authentication.

        Args:
          job_id: Unique identifier for the conversion job

          status: Status of the conversion job

          error: Error message for failed jobs

          result: Result data for completed jobs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/convert/v1/webhook",
            body=await async_maybe_transform(
                {
                    "job_id": job_id,
                    "status": status,
                    "error": error,
                    "result": result,
                },
                v1_webhook_params.V1WebhookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1WebhookResponse,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.download = to_custom_raw_response_wrapper(
            v1.download,
            BinaryAPIResponse,
        )
        self.process = to_raw_response_wrapper(
            v1.process,
        )
        self.webhook = to_raw_response_wrapper(
            v1.webhook,
        )

    @cached_property
    def jobs(self) -> JobsResourceWithRawResponse:
        return JobsResourceWithRawResponse(self._v1.jobs)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.download = async_to_custom_raw_response_wrapper(
            v1.download,
            AsyncBinaryAPIResponse,
        )
        self.process = async_to_raw_response_wrapper(
            v1.process,
        )
        self.webhook = async_to_raw_response_wrapper(
            v1.webhook,
        )

    @cached_property
    def jobs(self) -> AsyncJobsResourceWithRawResponse:
        return AsyncJobsResourceWithRawResponse(self._v1.jobs)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.download = to_custom_streamed_response_wrapper(
            v1.download,
            StreamedBinaryAPIResponse,
        )
        self.process = to_streamed_response_wrapper(
            v1.process,
        )
        self.webhook = to_streamed_response_wrapper(
            v1.webhook,
        )

    @cached_property
    def jobs(self) -> JobsResourceWithStreamingResponse:
        return JobsResourceWithStreamingResponse(self._v1.jobs)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.download = async_to_custom_streamed_response_wrapper(
            v1.download,
            AsyncStreamedBinaryAPIResponse,
        )
        self.process = async_to_streamed_response_wrapper(
            v1.process,
        )
        self.webhook = async_to_streamed_response_wrapper(
            v1.webhook,
        )

    @cached_property
    def jobs(self) -> AsyncJobsResourceWithStreamingResponse:
        return AsyncJobsResourceWithStreamingResponse(self._v1.jobs)
