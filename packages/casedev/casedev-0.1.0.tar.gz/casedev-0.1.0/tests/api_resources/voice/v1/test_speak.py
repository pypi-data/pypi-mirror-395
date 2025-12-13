# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from casedev import Casedev, AsyncCasedev
from casedev._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpeak:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = client.voice.v1.speak.create(
            text="text",
        )
        assert speak.is_closed
        assert speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = client.voice.v1.speak.create(
            text="text",
            apply_text_normalization=True,
            enable_logging=True,
            language_code="en",
            model_id="eleven_multilingual_v2",
            next_text="next_text",
            optimize_streaming_latency=0,
            output_format="mp3_44100_128",
            previous_text="previous_text",
            seed=0,
            voice_id="voice_id",
            voice_settings={
                "similarity_boost": 0,
                "stability": 0,
                "style": 0,
                "use_speaker_boost": True,
            },
        )
        assert speak.is_closed
        assert speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        speak = client.voice.v1.speak.with_raw_response.create(
            text="text",
        )

        assert speak.is_closed is True
        assert speak.http_request.headers.get("X-Stainless-Lang") == "python"
        assert speak.json() == {"foo": "bar"}
        assert isinstance(speak, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.voice.v1.speak.with_streaming_response.create(
            text="text",
        ) as speak:
            assert not speak.is_closed
            assert speak.http_request.headers.get("X-Stainless-Lang") == "python"

            assert speak.json() == {"foo": "bar"}
            assert cast(Any, speak.is_closed) is True
            assert isinstance(speak, StreamedBinaryAPIResponse)

        assert cast(Any, speak.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_stream(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = client.voice.v1.speak.stream(
            text="text",
        )
        assert speak.is_closed
        assert speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_stream_with_all_params(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = client.voice.v1.speak.stream(
            text="text",
            apply_text_normalization=True,
            enable_logging=True,
            language_code="language_code",
            model_id="eleven_monolingual_v1",
            next_text="next_text",
            optimize_streaming_latency=0,
            output_format="mp3_44100_128",
            previous_text="previous_text",
            seed=0,
            voice_id="voice_id",
            voice_settings={
                "similarity_boost": 0,
                "stability": 0,
                "style": 0,
                "use_speaker_boost": True,
            },
        )
        assert speak.is_closed
        assert speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_stream(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        speak = client.voice.v1.speak.with_raw_response.stream(
            text="text",
        )

        assert speak.is_closed is True
        assert speak.http_request.headers.get("X-Stainless-Lang") == "python"
        assert speak.json() == {"foo": "bar"}
        assert isinstance(speak, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_stream(self, client: Casedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.voice.v1.speak.with_streaming_response.stream(
            text="text",
        ) as speak:
            assert not speak.is_closed
            assert speak.http_request.headers.get("X-Stainless-Lang") == "python"

            assert speak.json() == {"foo": "bar"}
            assert cast(Any, speak.is_closed) is True
            assert isinstance(speak, StreamedBinaryAPIResponse)

        assert cast(Any, speak.is_closed) is True


class TestAsyncSpeak:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = await async_client.voice.v1.speak.create(
            text="text",
        )
        assert speak.is_closed
        assert await speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create_with_all_params(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = await async_client.voice.v1.speak.create(
            text="text",
            apply_text_normalization=True,
            enable_logging=True,
            language_code="en",
            model_id="eleven_multilingual_v2",
            next_text="next_text",
            optimize_streaming_latency=0,
            output_format="mp3_44100_128",
            previous_text="previous_text",
            seed=0,
            voice_id="voice_id",
            voice_settings={
                "similarity_boost": 0,
                "stability": 0,
                "style": 0,
                "use_speaker_boost": True,
            },
        )
        assert speak.is_closed
        assert await speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        speak = await async_client.voice.v1.speak.with_raw_response.create(
            text="text",
        )

        assert speak.is_closed is True
        assert speak.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await speak.json() == {"foo": "bar"}
        assert isinstance(speak, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.voice.v1.speak.with_streaming_response.create(
            text="text",
        ) as speak:
            assert not speak.is_closed
            assert speak.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await speak.json() == {"foo": "bar"}
            assert cast(Any, speak.is_closed) is True
            assert isinstance(speak, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, speak.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_stream(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = await async_client.voice.v1.speak.stream(
            text="text",
        )
        assert speak.is_closed
        assert await speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_stream_with_all_params(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        speak = await async_client.voice.v1.speak.stream(
            text="text",
            apply_text_normalization=True,
            enable_logging=True,
            language_code="language_code",
            model_id="eleven_monolingual_v1",
            next_text="next_text",
            optimize_streaming_latency=0,
            output_format="mp3_44100_128",
            previous_text="previous_text",
            seed=0,
            voice_id="voice_id",
            voice_settings={
                "similarity_boost": 0,
                "stability": 0,
                "style": 0,
                "use_speaker_boost": True,
            },
        )
        assert speak.is_closed
        assert await speak.json() == {"foo": "bar"}
        assert cast(Any, speak.is_closed) is True
        assert isinstance(speak, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_stream(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        speak = await async_client.voice.v1.speak.with_raw_response.stream(
            text="text",
        )

        assert speak.is_closed is True
        assert speak.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await speak.json() == {"foo": "bar"}
        assert isinstance(speak, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_stream(self, async_client: AsyncCasedev, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice/v1/speak/stream").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.voice.v1.speak.with_streaming_response.stream(
            text="text",
        ) as speak:
            assert not speak.is_closed
            assert speak.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await speak.json() == {"foo": "bar"}
            assert cast(Any, speak.is_closed) is True
            assert isinstance(speak, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, speak.is_closed) is True
