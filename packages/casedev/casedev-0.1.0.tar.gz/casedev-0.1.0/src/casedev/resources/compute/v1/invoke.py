# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, cast
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.compute.v1 import invoke_run_params
from ....types.compute.v1.invoke_run_response import InvokeRunResponse

__all__ = ["InvokeResource", "AsyncInvokeResource"]


class InvokeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InvokeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return InvokeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InvokeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return InvokeResourceWithStreamingResponse(self)

    def run(
        self,
        function_id: str,
        *,
        input: Dict[str, object],
        async_: bool | Omit = omit,
        function_suffix: Literal["_modal", "_task", "_web", "_server"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InvokeRunResponse:
        """Execute a deployed compute function with custom input data.

        Supports both
        synchronous and asynchronous execution modes. Functions can be invoked by ID or
        name and can process various types of input data for legal document analysis,
        data processing, or other computational tasks.

        Args:
          input: Input data to pass to the function

          async_: If true, returns immediately with run ID for background execution

          function_suffix: Override the auto-detected function suffix

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not function_id:
            raise ValueError(f"Expected a non-empty value for `function_id` but received {function_id!r}")
        return cast(
            InvokeRunResponse,
            self._post(
                f"/compute/v1/invoke/{function_id}",
                body=maybe_transform(
                    {
                        "input": input,
                        "async_": async_,
                        "function_suffix": function_suffix,
                    },
                    invoke_run_params.InvokeRunParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, InvokeRunResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncInvokeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInvokeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInvokeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInvokeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncInvokeResourceWithStreamingResponse(self)

    async def run(
        self,
        function_id: str,
        *,
        input: Dict[str, object],
        async_: bool | Omit = omit,
        function_suffix: Literal["_modal", "_task", "_web", "_server"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InvokeRunResponse:
        """Execute a deployed compute function with custom input data.

        Supports both
        synchronous and asynchronous execution modes. Functions can be invoked by ID or
        name and can process various types of input data for legal document analysis,
        data processing, or other computational tasks.

        Args:
          input: Input data to pass to the function

          async_: If true, returns immediately with run ID for background execution

          function_suffix: Override the auto-detected function suffix

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not function_id:
            raise ValueError(f"Expected a non-empty value for `function_id` but received {function_id!r}")
        return cast(
            InvokeRunResponse,
            await self._post(
                f"/compute/v1/invoke/{function_id}",
                body=await async_maybe_transform(
                    {
                        "input": input,
                        "async_": async_,
                        "function_suffix": function_suffix,
                    },
                    invoke_run_params.InvokeRunParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, InvokeRunResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class InvokeResourceWithRawResponse:
    def __init__(self, invoke: InvokeResource) -> None:
        self._invoke = invoke

        self.run = to_raw_response_wrapper(
            invoke.run,
        )


class AsyncInvokeResourceWithRawResponse:
    def __init__(self, invoke: AsyncInvokeResource) -> None:
        self._invoke = invoke

        self.run = async_to_raw_response_wrapper(
            invoke.run,
        )


class InvokeResourceWithStreamingResponse:
    def __init__(self, invoke: InvokeResource) -> None:
        self._invoke = invoke

        self.run = to_streamed_response_wrapper(
            invoke.run,
        )


class AsyncInvokeResourceWithStreamingResponse:
    def __init__(self, invoke: AsyncInvokeResource) -> None:
        self._invoke = invoke

        self.run = async_to_streamed_response_wrapper(
            invoke.run,
        )
