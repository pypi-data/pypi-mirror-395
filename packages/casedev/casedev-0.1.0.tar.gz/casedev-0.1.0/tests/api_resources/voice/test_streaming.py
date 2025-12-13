# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStreaming:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_url(self, client: Casedev) -> None:
        streaming = client.voice.streaming.get_url()
        assert streaming is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_url(self, client: Casedev) -> None:
        response = client.voice.streaming.with_raw_response.get_url()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        streaming = response.parse()
        assert streaming is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_url(self, client: Casedev) -> None:
        with client.voice.streaming.with_streaming_response.get_url() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            streaming = response.parse()
            assert streaming is None

        assert cast(Any, response.is_closed) is True


class TestAsyncStreaming:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_url(self, async_client: AsyncCasedev) -> None:
        streaming = await async_client.voice.streaming.get_url()
        assert streaming is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_url(self, async_client: AsyncCasedev) -> None:
        response = await async_client.voice.streaming.with_raw_response.get_url()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        streaming = await response.parse()
        assert streaming is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_url(self, async_client: AsyncCasedev) -> None:
        async with async_client.voice.streaming.with_streaming_response.get_url() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            streaming = await response.parse()
            assert streaming is None

        assert cast(Any, response.is_closed) is True
