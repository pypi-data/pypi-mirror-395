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
from ..._base_client import make_request_options
from ...types.templates import v1_list_params, v1_search_params, v1_execute_params
from ...types.templates.v1_execute_response import V1ExecuteResponse

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
        """Retrieve metadata for a published workflow by ID.

        Returns workflow configuration
        including input/output schemas, but excludes the prompt template for security.

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
            f"/templates/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        *,
        category: str | Omit = omit,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        published: bool | Omit = omit,
        sub_category: str | Omit = omit,
        type: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Retrieve a paginated list of available workflows with optional filtering by
        category, subcategory, type, and publication status. Workflows are pre-built
        document processing pipelines optimized for legal use cases.

        Args:
          category: Filter workflows by category (e.g., 'legal', 'compliance', 'contract')

          limit: Maximum number of workflows to return

          offset: Number of workflows to skip for pagination

          published: Include only published workflows

          sub_category: Filter workflows by subcategory (e.g., 'due-diligence', 'litigation', 'mergers')

          type: Filter workflows by type (e.g., 'document-review', 'contract-analysis',
              'compliance-check')

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/templates/v1",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "category": category,
                        "limit": limit,
                        "offset": offset,
                        "published": published,
                        "sub_category": sub_category,
                        "type": type,
                    },
                    v1_list_params.V1ListParams,
                ),
            ),
            cast_to=NoneType,
        )

    def execute(
        self,
        id: str,
        *,
        input: object,
        options: v1_execute_params.Options | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ExecuteResponse:
        """Execute a pre-built workflow with custom input data.

        Workflows automate common
        legal document processing tasks like contract analysis, due diligence reviews,
        and document classification.

        **Available Workflows:**

        - Contract analysis and risk assessment
        - Document classification and tagging
        - Legal research and case summarization
        - Due diligence document review
        - Compliance checking and reporting

        Args:
          input: Input data for the workflow (structure varies by workflow type)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/templates/v1/{id}/execute",
            body=maybe_transform(
                {
                    "input": input,
                    "options": options,
                },
                v1_execute_params.V1ExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ExecuteResponse,
        )

    def retrieve_execution(
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
        """Retrieves the status and details of a workflow execution.

        This endpoint is
        designed for future asynchronous execution support and currently returns a 501
        Not Implemented status since all executions are synchronous.

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
            f"/templates/v1/executions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def search(
        self,
        *,
        query: str,
        category: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Perform semantic search across available workflows to find the most relevant
        pre-built document processing pipelines for your legal use case.

        Args:
          query: Search query to find relevant workflows

          category: Optional category filter to narrow results

          limit: Maximum number of results to return (default: 10, max: 50)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/templates/v1/search",
            body=maybe_transform(
                {
                    "query": query,
                    "category": category,
                    "limit": limit,
                },
                v1_search_params.V1SearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
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
        """Retrieve metadata for a published workflow by ID.

        Returns workflow configuration
        including input/output schemas, but excludes the prompt template for security.

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
            f"/templates/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        *,
        category: str | Omit = omit,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        published: bool | Omit = omit,
        sub_category: str | Omit = omit,
        type: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Retrieve a paginated list of available workflows with optional filtering by
        category, subcategory, type, and publication status. Workflows are pre-built
        document processing pipelines optimized for legal use cases.

        Args:
          category: Filter workflows by category (e.g., 'legal', 'compliance', 'contract')

          limit: Maximum number of workflows to return

          offset: Number of workflows to skip for pagination

          published: Include only published workflows

          sub_category: Filter workflows by subcategory (e.g., 'due-diligence', 'litigation', 'mergers')

          type: Filter workflows by type (e.g., 'document-review', 'contract-analysis',
              'compliance-check')

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/templates/v1",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "category": category,
                        "limit": limit,
                        "offset": offset,
                        "published": published,
                        "sub_category": sub_category,
                        "type": type,
                    },
                    v1_list_params.V1ListParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def execute(
        self,
        id: str,
        *,
        input: object,
        options: v1_execute_params.Options | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ExecuteResponse:
        """Execute a pre-built workflow with custom input data.

        Workflows automate common
        legal document processing tasks like contract analysis, due diligence reviews,
        and document classification.

        **Available Workflows:**

        - Contract analysis and risk assessment
        - Document classification and tagging
        - Legal research and case summarization
        - Due diligence document review
        - Compliance checking and reporting

        Args:
          input: Input data for the workflow (structure varies by workflow type)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/templates/v1/{id}/execute",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "options": options,
                },
                v1_execute_params.V1ExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ExecuteResponse,
        )

    async def retrieve_execution(
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
        """Retrieves the status and details of a workflow execution.

        This endpoint is
        designed for future asynchronous execution support and currently returns a 501
        Not Implemented status since all executions are synchronous.

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
            f"/templates/v1/executions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def search(
        self,
        *,
        query: str,
        category: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Perform semantic search across available workflows to find the most relevant
        pre-built document processing pipelines for your legal use case.

        Args:
          query: Search query to find relevant workflows

          category: Optional category filter to narrow results

          limit: Maximum number of results to return (default: 10, max: 50)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/templates/v1/search",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "category": category,
                    "limit": limit,
                },
                v1_search_params.V1SearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.retrieve = to_raw_response_wrapper(
            v1.retrieve,
        )
        self.list = to_raw_response_wrapper(
            v1.list,
        )
        self.execute = to_raw_response_wrapper(
            v1.execute,
        )
        self.retrieve_execution = to_raw_response_wrapper(
            v1.retrieve_execution,
        )
        self.search = to_raw_response_wrapper(
            v1.search,
        )


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.retrieve = async_to_raw_response_wrapper(
            v1.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            v1.list,
        )
        self.execute = async_to_raw_response_wrapper(
            v1.execute,
        )
        self.retrieve_execution = async_to_raw_response_wrapper(
            v1.retrieve_execution,
        )
        self.search = async_to_raw_response_wrapper(
            v1.search,
        )


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.retrieve = to_streamed_response_wrapper(
            v1.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            v1.list,
        )
        self.execute = to_streamed_response_wrapper(
            v1.execute,
        )
        self.retrieve_execution = to_streamed_response_wrapper(
            v1.retrieve_execution,
        )
        self.search = to_streamed_response_wrapper(
            v1.search,
        )


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.retrieve = async_to_streamed_response_wrapper(
            v1.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            v1.list,
        )
        self.execute = async_to_streamed_response_wrapper(
            v1.execute,
        )
        self.retrieve_execution = async_to_streamed_response_wrapper(
            v1.retrieve_execution,
        )
        self.search = async_to_streamed_response_wrapper(
            v1.search,
        )
