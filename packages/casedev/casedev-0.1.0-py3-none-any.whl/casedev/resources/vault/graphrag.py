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

__all__ = ["GraphragResource", "AsyncGraphragResource"]


class GraphragResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GraphragResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return GraphragResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GraphragResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return GraphragResourceWithStreamingResponse(self)

    def get_stats(
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
        """
        Retrieve GraphRAG (Graph Retrieval-Augmented Generation) statistics for a
        specific vault. This includes metrics about the knowledge graph structure,
        entity relationships, and processing status that enable advanced semantic search
        and AI-powered document analysis.

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
            f"/vault/{id}/graphrag/stats",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def init(
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
        """
        Initialize a GraphRAG workspace for a vault to enable advanced knowledge graph
        and retrieval-augmented generation capabilities. This creates the necessary
        infrastructure for semantic document analysis and graph-based querying within
        the vault.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/vault/{id}/graphrag/init",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncGraphragResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGraphragResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGraphragResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGraphragResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncGraphragResourceWithStreamingResponse(self)

    async def get_stats(
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
        """
        Retrieve GraphRAG (Graph Retrieval-Augmented Generation) statistics for a
        specific vault. This includes metrics about the knowledge graph structure,
        entity relationships, and processing status that enable advanced semantic search
        and AI-powered document analysis.

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
            f"/vault/{id}/graphrag/stats",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def init(
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
        """
        Initialize a GraphRAG workspace for a vault to enable advanced knowledge graph
        and retrieval-augmented generation capabilities. This creates the necessary
        infrastructure for semantic document analysis and graph-based querying within
        the vault.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/vault/{id}/graphrag/init",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class GraphragResourceWithRawResponse:
    def __init__(self, graphrag: GraphragResource) -> None:
        self._graphrag = graphrag

        self.get_stats = to_raw_response_wrapper(
            graphrag.get_stats,
        )
        self.init = to_raw_response_wrapper(
            graphrag.init,
        )


class AsyncGraphragResourceWithRawResponse:
    def __init__(self, graphrag: AsyncGraphragResource) -> None:
        self._graphrag = graphrag

        self.get_stats = async_to_raw_response_wrapper(
            graphrag.get_stats,
        )
        self.init = async_to_raw_response_wrapper(
            graphrag.init,
        )


class GraphragResourceWithStreamingResponse:
    def __init__(self, graphrag: GraphragResource) -> None:
        self._graphrag = graphrag

        self.get_stats = to_streamed_response_wrapper(
            graphrag.get_stats,
        )
        self.init = to_streamed_response_wrapper(
            graphrag.init,
        )


class AsyncGraphragResourceWithStreamingResponse:
    def __init__(self, graphrag: AsyncGraphragResource) -> None:
        self._graphrag = graphrag

        self.get_stats = async_to_streamed_response_wrapper(
            graphrag.get_stats,
        )
        self.init = async_to_streamed_response_wrapper(
            graphrag.init,
        )
