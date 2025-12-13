# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev
from tests.utils import assert_matches_type
from casedev.types.llm.v1 import ChatCreateCompletionResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_completion(self, client: Casedev) -> None:
        chat = client.llm.v1.chat.create_completion(
            messages=[{}],
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_completion_with_all_params(self, client: Casedev) -> None:
        chat = client.llm.v1.chat.create_completion(
            messages=[
                {
                    "content": "content",
                    "role": "system",
                }
            ],
            frequency_penalty=0,
            max_tokens=1000,
            model="gpt-4o",
            presence_penalty=0,
            stream=False,
            temperature=0.7,
            top_p=0,
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_completion(self, client: Casedev) -> None:
        response = client.llm.v1.chat.with_raw_response.create_completion(
            messages=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_completion(self, client: Casedev) -> None:
        with client.llm.v1.chat.with_streaming_response.create_completion(
            messages=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChat:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_completion(self, async_client: AsyncCasedev) -> None:
        chat = await async_client.llm.v1.chat.create_completion(
            messages=[{}],
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_completion_with_all_params(self, async_client: AsyncCasedev) -> None:
        chat = await async_client.llm.v1.chat.create_completion(
            messages=[
                {
                    "content": "content",
                    "role": "system",
                }
            ],
            frequency_penalty=0,
            max_tokens=1000,
            model="gpt-4o",
            presence_penalty=0,
            stream=False,
            temperature=0.7,
            top_p=0,
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_completion(self, async_client: AsyncCasedev) -> None:
        response = await async_client.llm.v1.chat.with_raw_response.create_completion(
            messages=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_completion(self, async_client: AsyncCasedev) -> None:
        async with async_client.llm.v1.chat.with_streaming_response.create_completion(
            messages=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True
