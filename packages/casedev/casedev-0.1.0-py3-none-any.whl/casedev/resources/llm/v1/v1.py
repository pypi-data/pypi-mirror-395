# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal

import httpx

from .chat import (
    ChatResource,
    AsyncChatResource,
    ChatResourceWithRawResponse,
    AsyncChatResourceWithRawResponse,
    ChatResourceWithStreamingResponse,
    AsyncChatResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....types.llm import v1_create_embedding_params
from ...._base_client import make_request_options

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def chat(self) -> ChatResource:
        return ChatResource(self._client)

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

    def create_embedding(
        self,
        *,
        input: Union[str, SequenceNotStr[str]],
        model: str,
        dimensions: int | Omit = omit,
        encoding_format: Literal["float", "base64"] | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Create vector embeddings from text using OpenAI-compatible models.

        Perfect for
        semantic search, document similarity, and building RAG systems for legal
        documents.

        Args:
          input: Text or array of texts to create embeddings for

          model: Embedding model to use (e.g., text-embedding-ada-002, text-embedding-3-small)

          dimensions: Number of dimensions for the embeddings (model-specific)

          encoding_format: Format for returned embeddings

          user: Unique identifier for the end-user

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/llm/v1/embeddings",
            body=maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "dimensions": dimensions,
                    "encoding_format": encoding_format,
                    "user": user,
                },
                v1_create_embedding_params.V1CreateEmbeddingParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list_models(
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
        Retrieve a list of all available language models from 40+ providers including
        OpenAI, Anthropic, Google, and Case.dev's specialized legal models. Returns
        OpenAI-compatible model metadata with pricing information.

        This endpoint is compatible with OpenAI's models API format, making it easy to
        integrate with existing applications.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/llm/v1/models",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def chat(self) -> AsyncChatResource:
        return AsyncChatResource(self._client)

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

    async def create_embedding(
        self,
        *,
        input: Union[str, SequenceNotStr[str]],
        model: str,
        dimensions: int | Omit = omit,
        encoding_format: Literal["float", "base64"] | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Create vector embeddings from text using OpenAI-compatible models.

        Perfect for
        semantic search, document similarity, and building RAG systems for legal
        documents.

        Args:
          input: Text or array of texts to create embeddings for

          model: Embedding model to use (e.g., text-embedding-ada-002, text-embedding-3-small)

          dimensions: Number of dimensions for the embeddings (model-specific)

          encoding_format: Format for returned embeddings

          user: Unique identifier for the end-user

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/llm/v1/embeddings",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "dimensions": dimensions,
                    "encoding_format": encoding_format,
                    "user": user,
                },
                v1_create_embedding_params.V1CreateEmbeddingParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list_models(
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
        Retrieve a list of all available language models from 40+ providers including
        OpenAI, Anthropic, Google, and Case.dev's specialized legal models. Returns
        OpenAI-compatible model metadata with pricing information.

        This endpoint is compatible with OpenAI's models API format, making it easy to
        integrate with existing applications.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/llm/v1/models",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_embedding = to_raw_response_wrapper(
            v1.create_embedding,
        )
        self.list_models = to_raw_response_wrapper(
            v1.list_models,
        )

    @cached_property
    def chat(self) -> ChatResourceWithRawResponse:
        return ChatResourceWithRawResponse(self._v1.chat)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_embedding = async_to_raw_response_wrapper(
            v1.create_embedding,
        )
        self.list_models = async_to_raw_response_wrapper(
            v1.list_models,
        )

    @cached_property
    def chat(self) -> AsyncChatResourceWithRawResponse:
        return AsyncChatResourceWithRawResponse(self._v1.chat)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_embedding = to_streamed_response_wrapper(
            v1.create_embedding,
        )
        self.list_models = to_streamed_response_wrapper(
            v1.list_models,
        )

    @cached_property
    def chat(self) -> ChatResourceWithStreamingResponse:
        return ChatResourceWithStreamingResponse(self._v1.chat)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_embedding = async_to_streamed_response_wrapper(
            v1.create_embedding,
        )
        self.list_models = async_to_streamed_response_wrapper(
            v1.list_models,
        )

    @cached_property
    def chat(self) -> AsyncChatResourceWithStreamingResponse:
        return AsyncChatResourceWithStreamingResponse(self._v1.chat)
