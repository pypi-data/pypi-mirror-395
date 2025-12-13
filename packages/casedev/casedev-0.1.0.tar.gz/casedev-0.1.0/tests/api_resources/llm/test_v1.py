# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_embedding(self, client: Casedev) -> None:
        v1 = client.llm.v1.create_embedding(
            input="string",
            model="model",
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_embedding_with_all_params(self, client: Casedev) -> None:
        v1 = client.llm.v1.create_embedding(
            input="string",
            model="model",
            dimensions=0,
            encoding_format="float",
            user="user",
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_embedding(self, client: Casedev) -> None:
        response = client.llm.v1.with_raw_response.create_embedding(
            input="string",
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_embedding(self, client: Casedev) -> None:
        with client.llm.v1.with_streaming_response.create_embedding(
            input="string",
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_models(self, client: Casedev) -> None:
        v1 = client.llm.v1.list_models()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_models(self, client: Casedev) -> None:
        response = client.llm.v1.with_raw_response.list_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_models(self, client: Casedev) -> None:
        with client.llm.v1.with_streaming_response.list_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True


class TestAsyncV1:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_embedding(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.llm.v1.create_embedding(
            input="string",
            model="model",
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_embedding_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.llm.v1.create_embedding(
            input="string",
            model="model",
            dimensions=0,
            encoding_format="float",
            user="user",
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_embedding(self, async_client: AsyncCasedev) -> None:
        response = await async_client.llm.v1.with_raw_response.create_embedding(
            input="string",
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_embedding(self, async_client: AsyncCasedev) -> None:
        async with async_client.llm.v1.with_streaming_response.create_embedding(
            input="string",
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_models(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.llm.v1.list_models()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_models(self, async_client: AsyncCasedev) -> None:
        response = await async_client.llm.v1.with_raw_response.list_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_models(self, async_client: AsyncCasedev) -> None:
        async with async_client.llm.v1.with_streaming_response.list_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True
