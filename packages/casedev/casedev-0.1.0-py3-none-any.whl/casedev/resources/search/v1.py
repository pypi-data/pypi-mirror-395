# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
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
from ...types.search import (
    v1_answer_params,
    v1_search_params,
    v1_similar_params,
    v1_contents_params,
    v1_research_params,
    v1_retrieve_research_params,
)
from ...types.search.v1_answer_response import V1AnswerResponse
from ...types.search.v1_search_response import V1SearchResponse
from ...types.search.v1_similar_response import V1SimilarResponse
from ...types.search.v1_contents_response import V1ContentsResponse
from ...types.search.v1_research_response import V1ResearchResponse

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

    def answer(
        self,
        *,
        query: str,
        exclude_domains: SequenceNotStr[str] | Omit = omit,
        include_domains: SequenceNotStr[str] | Omit = omit,
        max_tokens: int | Omit = omit,
        model: str | Omit = omit,
        num_results: int | Omit = omit,
        search_type: Literal["auto", "web", "news", "academic"] | Omit = omit,
        stream: bool | Omit = omit,
        temperature: float | Omit = omit,
        text: bool | Omit = omit,
        use_custom_llm: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1AnswerResponse:
        """Generate comprehensive answers to questions using web search results.

        Supports
        two modes: native provider answers or custom LLM-powered answers using
        Case.dev's AI gateway. Perfect for legal research, fact-checking, and gathering
        supporting evidence for cases.

        Args:
          query: The question or topic to research and answer

          exclude_domains: Exclude these domains from search

          include_domains: Only search within these domains

          max_tokens: Maximum tokens for LLM response

          model: LLM model to use when useCustomLLM is true

          num_results: Number of search results to consider

          search_type: Type of search to perform

          stream: Stream the response (only for native provider answers)

          temperature: LLM temperature for answer generation

          text: Include text content in response

          use_custom_llm: Use Case.dev LLM for answer generation instead of provider's native answer

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/search/v1/answer",
            body=maybe_transform(
                {
                    "query": query,
                    "exclude_domains": exclude_domains,
                    "include_domains": include_domains,
                    "max_tokens": max_tokens,
                    "model": model,
                    "num_results": num_results,
                    "search_type": search_type,
                    "stream": stream,
                    "temperature": temperature,
                    "text": text,
                    "use_custom_llm": use_custom_llm,
                },
                v1_answer_params.V1AnswerParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1AnswerResponse,
        )

    def contents(
        self,
        *,
        urls: SequenceNotStr[str],
        context: str | Omit = omit,
        extras: object | Omit = omit,
        highlights: bool | Omit = omit,
        livecrawl: bool | Omit = omit,
        livecrawl_timeout: int | Omit = omit,
        subpages: bool | Omit = omit,
        subpage_target: int | Omit = omit,
        summary: bool | Omit = omit,
        text: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ContentsResponse:
        """Scrapes and extracts text content from web pages, PDFs, and documents.

        Useful
        for legal research, evidence collection, and document analysis. Supports live
        crawling, subpage extraction, and content summarization.

        Args:
          urls: Array of URLs to scrape and extract content from

          context: Context to guide content extraction and summarization

          extras: Additional extraction options

          highlights: Whether to include content highlights

          livecrawl: Whether to perform live crawling for dynamic content

          livecrawl_timeout: Timeout in seconds for live crawling

          subpages: Whether to extract content from linked subpages

          subpage_target: Maximum number of subpages to crawl

          summary: Whether to generate content summaries

          text: Whether to extract text content

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/search/v1/contents",
            body=maybe_transform(
                {
                    "urls": urls,
                    "context": context,
                    "extras": extras,
                    "highlights": highlights,
                    "livecrawl": livecrawl,
                    "livecrawl_timeout": livecrawl_timeout,
                    "subpages": subpages,
                    "subpage_target": subpage_target,
                    "summary": summary,
                    "text": text,
                },
                v1_contents_params.V1ContentsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ContentsResponse,
        )

    def research(
        self,
        *,
        instructions: str,
        model: Literal["fast", "normal", "pro"] | Omit = omit,
        output_schema: object | Omit = omit,
        query: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ResearchResponse:
        """
        Performs deep research by conducting multi-step analysis, gathering information
        from multiple sources, and providing comprehensive insights. Ideal for legal
        research, case analysis, and due diligence investigations.

        Args:
          instructions: Research instructions or query

          model: Research quality level - fast (quick), normal (balanced), pro (comprehensive)

          output_schema: Optional JSON schema to structure the research output

          query: Alias for instructions (for convenience)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/search/v1/research",
            body=maybe_transform(
                {
                    "instructions": instructions,
                    "model": model,
                    "output_schema": output_schema,
                    "query": query,
                },
                v1_research_params.V1ResearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ResearchResponse,
        )

    def retrieve_research(
        self,
        id: str,
        *,
        events: str | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Retrieve the status and results of a deep research task by ID.

        Supports both
        standard JSON responses and streaming for real-time updates as the research
        progresses. Research tasks analyze topics comprehensively using web search and
        AI synthesis.

        Args:
          events: Filter specific event types for streaming

          stream: Enable streaming for real-time updates

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/search/v1/research/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "events": events,
                        "stream": stream,
                    },
                    v1_retrieve_research_params.V1RetrieveResearchParams,
                ),
            ),
            cast_to=NoneType,
        )

    def search(
        self,
        *,
        query: str,
        additional_queries: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        contents: str | Omit = omit,
        end_crawl_date: Union[str, date] | Omit = omit,
        end_published_date: Union[str, date] | Omit = omit,
        exclude_domains: SequenceNotStr[str] | Omit = omit,
        include_domains: SequenceNotStr[str] | Omit = omit,
        include_text: bool | Omit = omit,
        num_results: int | Omit = omit,
        start_crawl_date: Union[str, date] | Omit = omit,
        start_published_date: Union[str, date] | Omit = omit,
        type: Literal["auto", "search", "news"] | Omit = omit,
        user_location: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1SearchResponse:
        """
        Executes intelligent web search queries with advanced filtering and
        customization options. Ideal for legal research, case law discovery, and
        gathering supporting documentation for litigation or compliance matters.

        Args:
          query: Primary search query

          additional_queries: Additional related search queries to enhance results

          category: Category filter for search results

          contents: Specific content type to search for

          end_crawl_date: End date for crawl date filtering

          end_published_date: End date for published date filtering

          exclude_domains: Domains to exclude from search results

          include_domains: Domains to include in search results

          include_text: Whether to include full text content in results

          num_results: Number of search results to return

          start_crawl_date: Start date for crawl date filtering

          start_published_date: Start date for published date filtering

          type: Type of search to perform

          user_location: Geographic location for localized results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/search/v1/search",
            body=maybe_transform(
                {
                    "query": query,
                    "additional_queries": additional_queries,
                    "category": category,
                    "contents": contents,
                    "end_crawl_date": end_crawl_date,
                    "end_published_date": end_published_date,
                    "exclude_domains": exclude_domains,
                    "include_domains": include_domains,
                    "include_text": include_text,
                    "num_results": num_results,
                    "start_crawl_date": start_crawl_date,
                    "start_published_date": start_published_date,
                    "type": type,
                    "user_location": user_location,
                },
                v1_search_params.V1SearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1SearchResponse,
        )

    def similar(
        self,
        *,
        url: str,
        contents: str | Omit = omit,
        end_crawl_date: Union[str, date] | Omit = omit,
        end_published_date: Union[str, date] | Omit = omit,
        exclude_domains: SequenceNotStr[str] | Omit = omit,
        include_domains: SequenceNotStr[str] | Omit = omit,
        include_text: bool | Omit = omit,
        num_results: int | Omit = omit,
        start_crawl_date: Union[str, date] | Omit = omit,
        start_published_date: Union[str, date] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1SimilarResponse:
        """Find web pages and documents similar to a given URL.

        Useful for legal research
        to discover related case law, statutes, or legal commentary that shares similar
        themes or content structure.

        Args:
          url: The URL to find similar content for

          contents: Additional content to consider for similarity matching

          end_crawl_date: Only include pages crawled before this date

          end_published_date: Only include pages published before this date

          exclude_domains: Exclude results from these domains

          include_domains: Only search within these domains

          include_text: Whether to include extracted text content in results

          num_results: Number of similar results to return

          start_crawl_date: Only include pages crawled after this date

          start_published_date: Only include pages published after this date

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/search/v1/similar",
            body=maybe_transform(
                {
                    "url": url,
                    "contents": contents,
                    "end_crawl_date": end_crawl_date,
                    "end_published_date": end_published_date,
                    "exclude_domains": exclude_domains,
                    "include_domains": include_domains,
                    "include_text": include_text,
                    "num_results": num_results,
                    "start_crawl_date": start_crawl_date,
                    "start_published_date": start_published_date,
                },
                v1_similar_params.V1SimilarParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1SimilarResponse,
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

    async def answer(
        self,
        *,
        query: str,
        exclude_domains: SequenceNotStr[str] | Omit = omit,
        include_domains: SequenceNotStr[str] | Omit = omit,
        max_tokens: int | Omit = omit,
        model: str | Omit = omit,
        num_results: int | Omit = omit,
        search_type: Literal["auto", "web", "news", "academic"] | Omit = omit,
        stream: bool | Omit = omit,
        temperature: float | Omit = omit,
        text: bool | Omit = omit,
        use_custom_llm: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1AnswerResponse:
        """Generate comprehensive answers to questions using web search results.

        Supports
        two modes: native provider answers or custom LLM-powered answers using
        Case.dev's AI gateway. Perfect for legal research, fact-checking, and gathering
        supporting evidence for cases.

        Args:
          query: The question or topic to research and answer

          exclude_domains: Exclude these domains from search

          include_domains: Only search within these domains

          max_tokens: Maximum tokens for LLM response

          model: LLM model to use when useCustomLLM is true

          num_results: Number of search results to consider

          search_type: Type of search to perform

          stream: Stream the response (only for native provider answers)

          temperature: LLM temperature for answer generation

          text: Include text content in response

          use_custom_llm: Use Case.dev LLM for answer generation instead of provider's native answer

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/search/v1/answer",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "exclude_domains": exclude_domains,
                    "include_domains": include_domains,
                    "max_tokens": max_tokens,
                    "model": model,
                    "num_results": num_results,
                    "search_type": search_type,
                    "stream": stream,
                    "temperature": temperature,
                    "text": text,
                    "use_custom_llm": use_custom_llm,
                },
                v1_answer_params.V1AnswerParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1AnswerResponse,
        )

    async def contents(
        self,
        *,
        urls: SequenceNotStr[str],
        context: str | Omit = omit,
        extras: object | Omit = omit,
        highlights: bool | Omit = omit,
        livecrawl: bool | Omit = omit,
        livecrawl_timeout: int | Omit = omit,
        subpages: bool | Omit = omit,
        subpage_target: int | Omit = omit,
        summary: bool | Omit = omit,
        text: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ContentsResponse:
        """Scrapes and extracts text content from web pages, PDFs, and documents.

        Useful
        for legal research, evidence collection, and document analysis. Supports live
        crawling, subpage extraction, and content summarization.

        Args:
          urls: Array of URLs to scrape and extract content from

          context: Context to guide content extraction and summarization

          extras: Additional extraction options

          highlights: Whether to include content highlights

          livecrawl: Whether to perform live crawling for dynamic content

          livecrawl_timeout: Timeout in seconds for live crawling

          subpages: Whether to extract content from linked subpages

          subpage_target: Maximum number of subpages to crawl

          summary: Whether to generate content summaries

          text: Whether to extract text content

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/search/v1/contents",
            body=await async_maybe_transform(
                {
                    "urls": urls,
                    "context": context,
                    "extras": extras,
                    "highlights": highlights,
                    "livecrawl": livecrawl,
                    "livecrawl_timeout": livecrawl_timeout,
                    "subpages": subpages,
                    "subpage_target": subpage_target,
                    "summary": summary,
                    "text": text,
                },
                v1_contents_params.V1ContentsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ContentsResponse,
        )

    async def research(
        self,
        *,
        instructions: str,
        model: Literal["fast", "normal", "pro"] | Omit = omit,
        output_schema: object | Omit = omit,
        query: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ResearchResponse:
        """
        Performs deep research by conducting multi-step analysis, gathering information
        from multiple sources, and providing comprehensive insights. Ideal for legal
        research, case analysis, and due diligence investigations.

        Args:
          instructions: Research instructions or query

          model: Research quality level - fast (quick), normal (balanced), pro (comprehensive)

          output_schema: Optional JSON schema to structure the research output

          query: Alias for instructions (for convenience)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/search/v1/research",
            body=await async_maybe_transform(
                {
                    "instructions": instructions,
                    "model": model,
                    "output_schema": output_schema,
                    "query": query,
                },
                v1_research_params.V1ResearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ResearchResponse,
        )

    async def retrieve_research(
        self,
        id: str,
        *,
        events: str | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Retrieve the status and results of a deep research task by ID.

        Supports both
        standard JSON responses and streaming for real-time updates as the research
        progresses. Research tasks analyze topics comprehensively using web search and
        AI synthesis.

        Args:
          events: Filter specific event types for streaming

          stream: Enable streaming for real-time updates

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/search/v1/research/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "events": events,
                        "stream": stream,
                    },
                    v1_retrieve_research_params.V1RetrieveResearchParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def search(
        self,
        *,
        query: str,
        additional_queries: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        contents: str | Omit = omit,
        end_crawl_date: Union[str, date] | Omit = omit,
        end_published_date: Union[str, date] | Omit = omit,
        exclude_domains: SequenceNotStr[str] | Omit = omit,
        include_domains: SequenceNotStr[str] | Omit = omit,
        include_text: bool | Omit = omit,
        num_results: int | Omit = omit,
        start_crawl_date: Union[str, date] | Omit = omit,
        start_published_date: Union[str, date] | Omit = omit,
        type: Literal["auto", "search", "news"] | Omit = omit,
        user_location: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1SearchResponse:
        """
        Executes intelligent web search queries with advanced filtering and
        customization options. Ideal for legal research, case law discovery, and
        gathering supporting documentation for litigation or compliance matters.

        Args:
          query: Primary search query

          additional_queries: Additional related search queries to enhance results

          category: Category filter for search results

          contents: Specific content type to search for

          end_crawl_date: End date for crawl date filtering

          end_published_date: End date for published date filtering

          exclude_domains: Domains to exclude from search results

          include_domains: Domains to include in search results

          include_text: Whether to include full text content in results

          num_results: Number of search results to return

          start_crawl_date: Start date for crawl date filtering

          start_published_date: Start date for published date filtering

          type: Type of search to perform

          user_location: Geographic location for localized results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/search/v1/search",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "additional_queries": additional_queries,
                    "category": category,
                    "contents": contents,
                    "end_crawl_date": end_crawl_date,
                    "end_published_date": end_published_date,
                    "exclude_domains": exclude_domains,
                    "include_domains": include_domains,
                    "include_text": include_text,
                    "num_results": num_results,
                    "start_crawl_date": start_crawl_date,
                    "start_published_date": start_published_date,
                    "type": type,
                    "user_location": user_location,
                },
                v1_search_params.V1SearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1SearchResponse,
        )

    async def similar(
        self,
        *,
        url: str,
        contents: str | Omit = omit,
        end_crawl_date: Union[str, date] | Omit = omit,
        end_published_date: Union[str, date] | Omit = omit,
        exclude_domains: SequenceNotStr[str] | Omit = omit,
        include_domains: SequenceNotStr[str] | Omit = omit,
        include_text: bool | Omit = omit,
        num_results: int | Omit = omit,
        start_crawl_date: Union[str, date] | Omit = omit,
        start_published_date: Union[str, date] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1SimilarResponse:
        """Find web pages and documents similar to a given URL.

        Useful for legal research
        to discover related case law, statutes, or legal commentary that shares similar
        themes or content structure.

        Args:
          url: The URL to find similar content for

          contents: Additional content to consider for similarity matching

          end_crawl_date: Only include pages crawled before this date

          end_published_date: Only include pages published before this date

          exclude_domains: Exclude results from these domains

          include_domains: Only search within these domains

          include_text: Whether to include extracted text content in results

          num_results: Number of similar results to return

          start_crawl_date: Only include pages crawled after this date

          start_published_date: Only include pages published after this date

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/search/v1/similar",
            body=await async_maybe_transform(
                {
                    "url": url,
                    "contents": contents,
                    "end_crawl_date": end_crawl_date,
                    "end_published_date": end_published_date,
                    "exclude_domains": exclude_domains,
                    "include_domains": include_domains,
                    "include_text": include_text,
                    "num_results": num_results,
                    "start_crawl_date": start_crawl_date,
                    "start_published_date": start_published_date,
                },
                v1_similar_params.V1SimilarParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1SimilarResponse,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.answer = to_raw_response_wrapper(
            v1.answer,
        )
        self.contents = to_raw_response_wrapper(
            v1.contents,
        )
        self.research = to_raw_response_wrapper(
            v1.research,
        )
        self.retrieve_research = to_raw_response_wrapper(
            v1.retrieve_research,
        )
        self.search = to_raw_response_wrapper(
            v1.search,
        )
        self.similar = to_raw_response_wrapper(
            v1.similar,
        )


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.answer = async_to_raw_response_wrapper(
            v1.answer,
        )
        self.contents = async_to_raw_response_wrapper(
            v1.contents,
        )
        self.research = async_to_raw_response_wrapper(
            v1.research,
        )
        self.retrieve_research = async_to_raw_response_wrapper(
            v1.retrieve_research,
        )
        self.search = async_to_raw_response_wrapper(
            v1.search,
        )
        self.similar = async_to_raw_response_wrapper(
            v1.similar,
        )


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.answer = to_streamed_response_wrapper(
            v1.answer,
        )
        self.contents = to_streamed_response_wrapper(
            v1.contents,
        )
        self.research = to_streamed_response_wrapper(
            v1.research,
        )
        self.retrieve_research = to_streamed_response_wrapper(
            v1.retrieve_research,
        )
        self.search = to_streamed_response_wrapper(
            v1.search,
        )
        self.similar = to_streamed_response_wrapper(
            v1.similar,
        )


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.answer = async_to_streamed_response_wrapper(
            v1.answer,
        )
        self.contents = async_to_streamed_response_wrapper(
            v1.contents,
        )
        self.research = async_to_streamed_response_wrapper(
            v1.research,
        )
        self.retrieve_research = async_to_streamed_response_wrapper(
            v1.retrieve_research,
        )
        self.search = async_to_streamed_response_wrapper(
            v1.search,
        )
        self.similar = async_to_streamed_response_wrapper(
            v1.similar,
        )
