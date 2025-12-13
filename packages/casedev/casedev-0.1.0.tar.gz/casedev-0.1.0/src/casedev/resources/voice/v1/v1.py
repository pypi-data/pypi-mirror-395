# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .speak import (
    SpeakResource,
    AsyncSpeakResource,
    SpeakResourceWithRawResponse,
    AsyncSpeakResourceWithRawResponse,
    SpeakResourceWithStreamingResponse,
    AsyncSpeakResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....types.voice import v1_list_voices_params
from ...._base_client import make_request_options

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def speak(self) -> SpeakResource:
        return SpeakResource(self._client)

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

    def list_voices(
        self,
        *,
        category: str | Omit = omit,
        collection_id: str | Omit = omit,
        include_total_count: bool | Omit = omit,
        next_page_token: str | Omit = omit,
        page_size: int | Omit = omit,
        search: str | Omit = omit,
        sort: Literal["name", "created_at", "updated_at"] | Omit = omit,
        sort_direction: Literal["asc", "desc"] | Omit = omit,
        voice_type: Literal["premade", "cloned", "professional"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Retrieve a list of available voices for text-to-speech synthesis.

        This endpoint
        provides access to a comprehensive catalog of voices with various
        characteristics, languages, and styles suitable for legal document narration,
        client presentations, and accessibility purposes.

        Args:
          category: Filter by voice category

          collection_id: Filter by voice collection ID

          include_total_count: Whether to include total count in response

          next_page_token: Token for retrieving the next page of results

          page_size: Number of voices to return per page (max 100)

          search: Search term to filter voices by name or description

          sort: Field to sort by

          sort_direction: Sort direction

          voice_type: Filter by voice type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/voice/v1/voices",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "category": category,
                        "collection_id": collection_id,
                        "include_total_count": include_total_count,
                        "next_page_token": next_page_token,
                        "page_size": page_size,
                        "search": search,
                        "sort": sort,
                        "sort_direction": sort_direction,
                        "voice_type": voice_type,
                    },
                    v1_list_voices_params.V1ListVoicesParams,
                ),
            ),
            cast_to=NoneType,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def speak(self) -> AsyncSpeakResource:
        return AsyncSpeakResource(self._client)

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

    async def list_voices(
        self,
        *,
        category: str | Omit = omit,
        collection_id: str | Omit = omit,
        include_total_count: bool | Omit = omit,
        next_page_token: str | Omit = omit,
        page_size: int | Omit = omit,
        search: str | Omit = omit,
        sort: Literal["name", "created_at", "updated_at"] | Omit = omit,
        sort_direction: Literal["asc", "desc"] | Omit = omit,
        voice_type: Literal["premade", "cloned", "professional"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Retrieve a list of available voices for text-to-speech synthesis.

        This endpoint
        provides access to a comprehensive catalog of voices with various
        characteristics, languages, and styles suitable for legal document narration,
        client presentations, and accessibility purposes.

        Args:
          category: Filter by voice category

          collection_id: Filter by voice collection ID

          include_total_count: Whether to include total count in response

          next_page_token: Token for retrieving the next page of results

          page_size: Number of voices to return per page (max 100)

          search: Search term to filter voices by name or description

          sort: Field to sort by

          sort_direction: Sort direction

          voice_type: Filter by voice type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/voice/v1/voices",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "category": category,
                        "collection_id": collection_id,
                        "include_total_count": include_total_count,
                        "next_page_token": next_page_token,
                        "page_size": page_size,
                        "search": search,
                        "sort": sort,
                        "sort_direction": sort_direction,
                        "voice_type": voice_type,
                    },
                    v1_list_voices_params.V1ListVoicesParams,
                ),
            ),
            cast_to=NoneType,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.list_voices = to_raw_response_wrapper(
            v1.list_voices,
        )

    @cached_property
    def speak(self) -> SpeakResourceWithRawResponse:
        return SpeakResourceWithRawResponse(self._v1.speak)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.list_voices = async_to_raw_response_wrapper(
            v1.list_voices,
        )

    @cached_property
    def speak(self) -> AsyncSpeakResourceWithRawResponse:
        return AsyncSpeakResourceWithRawResponse(self._v1.speak)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.list_voices = to_streamed_response_wrapper(
            v1.list_voices,
        )

    @cached_property
    def speak(self) -> SpeakResourceWithStreamingResponse:
        return SpeakResourceWithStreamingResponse(self._v1.speak)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.list_voices = async_to_streamed_response_wrapper(
            v1.list_voices,
        )

    @cached_property
    def speak(self) -> AsyncSpeakResourceWithStreamingResponse:
        return AsyncSpeakResourceWithStreamingResponse(self._v1.speak)
