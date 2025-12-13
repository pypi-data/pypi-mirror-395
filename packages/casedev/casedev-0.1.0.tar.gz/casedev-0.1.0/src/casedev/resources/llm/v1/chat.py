# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

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
from ....types.llm.v1 import chat_create_completion_params
from ....types.llm.v1.chat_create_completion_response import ChatCreateCompletionResponse

__all__ = ["ChatResource", "AsyncChatResource"]


class ChatResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return ChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return ChatResourceWithStreamingResponse(self)

    def create_completion(
        self,
        *,
        messages: Iterable[chat_create_completion_params.Message],
        frequency_penalty: float | Omit = omit,
        max_tokens: int | Omit = omit,
        model: str | Omit = omit,
        presence_penalty: float | Omit = omit,
        stream: bool | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCreateCompletionResponse:
        """Create a completion for the provided prompt and parameters.

        Compatible with
        OpenAI's chat completions API. Supports 40+ models including GPT-4, Claude,
        Gemini, and CaseMark legal AI models. Includes streaming support, token
        counting, and usage tracking.

        Args:
          messages: List of messages comprising the conversation

          frequency_penalty: Frequency penalty parameter

          max_tokens: Maximum number of tokens to generate

          model: Model to use for completion. Defaults to casemark-core-1 if not specified

          presence_penalty: Presence penalty parameter

          stream: Whether to stream back partial progress

          temperature: Sampling temperature between 0 and 2

          top_p: Nucleus sampling parameter

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/llm/v1/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "frequency_penalty": frequency_penalty,
                    "max_tokens": max_tokens,
                    "model": model,
                    "presence_penalty": presence_penalty,
                    "stream": stream,
                    "temperature": temperature,
                    "top_p": top_p,
                },
                chat_create_completion_params.ChatCreateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCreateCompletionResponse,
        )


class AsyncChatResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncChatResourceWithStreamingResponse(self)

    async def create_completion(
        self,
        *,
        messages: Iterable[chat_create_completion_params.Message],
        frequency_penalty: float | Omit = omit,
        max_tokens: int | Omit = omit,
        model: str | Omit = omit,
        presence_penalty: float | Omit = omit,
        stream: bool | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCreateCompletionResponse:
        """Create a completion for the provided prompt and parameters.

        Compatible with
        OpenAI's chat completions API. Supports 40+ models including GPT-4, Claude,
        Gemini, and CaseMark legal AI models. Includes streaming support, token
        counting, and usage tracking.

        Args:
          messages: List of messages comprising the conversation

          frequency_penalty: Frequency penalty parameter

          max_tokens: Maximum number of tokens to generate

          model: Model to use for completion. Defaults to casemark-core-1 if not specified

          presence_penalty: Presence penalty parameter

          stream: Whether to stream back partial progress

          temperature: Sampling temperature between 0 and 2

          top_p: Nucleus sampling parameter

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/llm/v1/chat/completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "frequency_penalty": frequency_penalty,
                    "max_tokens": max_tokens,
                    "model": model,
                    "presence_penalty": presence_penalty,
                    "stream": stream,
                    "temperature": temperature,
                    "top_p": top_p,
                },
                chat_create_completion_params.ChatCreateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCreateCompletionResponse,
        )


class ChatResourceWithRawResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create_completion = to_raw_response_wrapper(
            chat.create_completion,
        )


class AsyncChatResourceWithRawResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create_completion = async_to_raw_response_wrapper(
            chat.create_completion,
        )


class ChatResourceWithStreamingResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create_completion = to_streamed_response_wrapper(
            chat.create_completion,
        )


class AsyncChatResourceWithStreamingResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create_completion = async_to_streamed_response_wrapper(
            chat.create_completion,
        )
