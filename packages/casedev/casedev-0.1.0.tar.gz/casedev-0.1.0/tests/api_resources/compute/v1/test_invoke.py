# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev
from tests.utils import assert_matches_type
from casedev.types.compute.v1 import InvokeRunResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInvoke:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_run(self, client: Casedev) -> None:
        invoke = client.compute.v1.invoke.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
        )
        assert_matches_type(InvokeRunResponse, invoke, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_run_with_all_params(self, client: Casedev) -> None:
        invoke = client.compute.v1.invoke.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
            async_=True,
            function_suffix="_modal",
        )
        assert_matches_type(InvokeRunResponse, invoke, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_run(self, client: Casedev) -> None:
        response = client.compute.v1.invoke.with_raw_response.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invoke = response.parse()
        assert_matches_type(InvokeRunResponse, invoke, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_run(self, client: Casedev) -> None:
        with client.compute.v1.invoke.with_streaming_response.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invoke = response.parse()
            assert_matches_type(InvokeRunResponse, invoke, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_run(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_id` but received ''"):
            client.compute.v1.invoke.with_raw_response.run(
                function_id="",
                input={"foo": "bar"},
            )


class TestAsyncInvoke:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_run(self, async_client: AsyncCasedev) -> None:
        invoke = await async_client.compute.v1.invoke.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
        )
        assert_matches_type(InvokeRunResponse, invoke, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_run_with_all_params(self, async_client: AsyncCasedev) -> None:
        invoke = await async_client.compute.v1.invoke.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
            async_=True,
            function_suffix="_modal",
        )
        assert_matches_type(InvokeRunResponse, invoke, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_run(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.invoke.with_raw_response.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invoke = await response.parse()
        assert_matches_type(InvokeRunResponse, invoke, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_run(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.invoke.with_streaming_response.run(
            function_id="func_abc123 or document-analyzer",
            input={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invoke = await response.parse()
            assert_matches_type(InvokeRunResponse, invoke, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_run(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_id` but received ''"):
            await async_client.compute.v1.invoke.with_raw_response.run(
                function_id="",
                input={"foo": "bar"},
            )
