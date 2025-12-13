# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

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
from ...types.ocr import v1_process_params
from ..._base_client import make_request_options
from ...types.ocr.v1_process_response import V1ProcessResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
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
    ) -> None:
        """Retrieve the status and results of an OCR job.

        Returns job progress, extracted
        text, and metadata when processing is complete.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/ocr/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def download(
        self,
        type: Literal["text", "json", "pdf", "original"],
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Download OCR processing results in various formats.

        Returns the processed
        document as text extraction, structured JSON with coordinates, searchable PDF
        with text layer, or the original uploaded document.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/ocr/v1/{id}/download/{type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def process(
        self,
        *,
        document_url: str,
        callback_url: str | Omit = omit,
        document_id: str | Omit = omit,
        engine: Literal["doctr", "paddleocr"] | Omit = omit,
        features: v1_process_params.Features | Omit = omit,
        result_bucket: str | Omit = omit,
        result_prefix: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ProcessResponse:
        """
        Submit a document for OCR processing to extract text, detect tables, forms, and
        other features. Supports PDFs, images, and scanned documents. Returns a job ID
        that can be used to track processing status.

        Args:
          document_url: URL or S3 path to the document to process

          callback_url: URL to receive completion webhook

          document_id: Optional custom document identifier

          engine: OCR engine to use

          features: OCR features to extract

          result_bucket: S3 bucket to store results

          result_prefix: S3 key prefix for results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/ocr/v1/process",
            body=maybe_transform(
                {
                    "document_url": document_url,
                    "callback_url": callback_url,
                    "document_id": document_id,
                    "engine": engine,
                    "features": features,
                    "result_bucket": result_bucket,
                    "result_prefix": result_prefix,
                },
                v1_process_params.V1ProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ProcessResponse,
        )


class AsyncV1Resource(AsyncAPIResource):
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
    ) -> None:
        """Retrieve the status and results of an OCR job.

        Returns job progress, extracted
        text, and metadata when processing is complete.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/ocr/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def download(
        self,
        type: Literal["text", "json", "pdf", "original"],
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Download OCR processing results in various formats.

        Returns the processed
        document as text extraction, structured JSON with coordinates, searchable PDF
        with text layer, or the original uploaded document.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/ocr/v1/{id}/download/{type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def process(
        self,
        *,
        document_url: str,
        callback_url: str | Omit = omit,
        document_id: str | Omit = omit,
        engine: Literal["doctr", "paddleocr"] | Omit = omit,
        features: v1_process_params.Features | Omit = omit,
        result_bucket: str | Omit = omit,
        result_prefix: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ProcessResponse:
        """
        Submit a document for OCR processing to extract text, detect tables, forms, and
        other features. Supports PDFs, images, and scanned documents. Returns a job ID
        that can be used to track processing status.

        Args:
          document_url: URL or S3 path to the document to process

          callback_url: URL to receive completion webhook

          document_id: Optional custom document identifier

          engine: OCR engine to use

          features: OCR features to extract

          result_bucket: S3 bucket to store results

          result_prefix: S3 key prefix for results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/ocr/v1/process",
            body=await async_maybe_transform(
                {
                    "document_url": document_url,
                    "callback_url": callback_url,
                    "document_id": document_id,
                    "engine": engine,
                    "features": features,
                    "result_bucket": result_bucket,
                    "result_prefix": result_prefix,
                },
                v1_process_params.V1ProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ProcessResponse,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.retrieve = to_raw_response_wrapper(
            v1.retrieve,
        )
        self.download = to_raw_response_wrapper(
            v1.download,
        )
        self.process = to_raw_response_wrapper(
            v1.process,
        )


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.retrieve = async_to_raw_response_wrapper(
            v1.retrieve,
        )
        self.download = async_to_raw_response_wrapper(
            v1.download,
        )
        self.process = async_to_raw_response_wrapper(
            v1.process,
        )


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.retrieve = to_streamed_response_wrapper(
            v1.retrieve,
        )
        self.download = to_streamed_response_wrapper(
            v1.download,
        )
        self.process = to_streamed_response_wrapper(
            v1.process,
        )


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.retrieve = async_to_streamed_response_wrapper(
            v1.retrieve,
        )
        self.download = async_to_streamed_response_wrapper(
            v1.download,
        )
        self.process = async_to_streamed_response_wrapper(
            v1.process,
        )
