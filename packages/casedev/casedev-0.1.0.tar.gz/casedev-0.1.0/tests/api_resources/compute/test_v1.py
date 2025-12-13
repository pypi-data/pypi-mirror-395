# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev
from tests.utils import assert_matches_type
from casedev.types.compute import V1DeployResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_deploy(self, client: Casedev) -> None:
        v1 = client.compute.v1.deploy(
            entrypoint_name="entrypointName",
            type="task",
        )
        assert_matches_type(V1DeployResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_deploy_with_all_params(self, client: Casedev) -> None:
        v1 = client.compute.v1.deploy(
            entrypoint_name="entrypointName",
            type="task",
            code="code",
            config={
                "add_python": "addPython",
                "allow_network": True,
                "cmd": ["string"],
                "concurrency": 0,
                "cpu_count": 0,
                "cron_schedule": "cronSchedule",
                "dependencies": ["string"],
                "entrypoint": ["string"],
                "env": {"foo": "string"},
                "gpu_count": 0,
                "gpu_type": "cpu",
                "is_web_service": True,
                "memory_mb": 0,
                "pip_install": ["string"],
                "port": 0,
                "python_version": "pythonVersion",
                "retries": 0,
                "secret_groups": ["string"],
                "timeout_seconds": 0,
                "use_uv": True,
                "warm_instances": 0,
                "workdir": "workdir",
            },
            dockerfile="dockerfile",
            entrypoint_file="entrypointFile",
            environment="environment",
            image="image",
            runtime="python",
        )
        assert_matches_type(V1DeployResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_deploy(self, client: Casedev) -> None:
        response = client.compute.v1.with_raw_response.deploy(
            entrypoint_name="entrypointName",
            type="task",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1DeployResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_deploy(self, client: Casedev) -> None:
        with client.compute.v1.with_streaming_response.deploy(
            entrypoint_name="entrypointName",
            type="task",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1DeployResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_pricing(self, client: Casedev) -> None:
        v1 = client.compute.v1.get_pricing()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_pricing(self, client: Casedev) -> None:
        response = client.compute.v1.with_raw_response.get_pricing()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_pricing(self, client: Casedev) -> None:
        with client.compute.v1.with_streaming_response.get_pricing() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_usage(self, client: Casedev) -> None:
        v1 = client.compute.v1.get_usage()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_usage_with_all_params(self, client: Casedev) -> None:
        v1 = client.compute.v1.get_usage(
            month=3,
            year=2024,
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_usage(self, client: Casedev) -> None:
        response = client.compute.v1.with_raw_response.get_usage()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_usage(self, client: Casedev) -> None:
        with client.compute.v1.with_streaming_response.get_usage() as response:
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
    async def test_method_deploy(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.compute.v1.deploy(
            entrypoint_name="entrypointName",
            type="task",
        )
        assert_matches_type(V1DeployResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_deploy_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.compute.v1.deploy(
            entrypoint_name="entrypointName",
            type="task",
            code="code",
            config={
                "add_python": "addPython",
                "allow_network": True,
                "cmd": ["string"],
                "concurrency": 0,
                "cpu_count": 0,
                "cron_schedule": "cronSchedule",
                "dependencies": ["string"],
                "entrypoint": ["string"],
                "env": {"foo": "string"},
                "gpu_count": 0,
                "gpu_type": "cpu",
                "is_web_service": True,
                "memory_mb": 0,
                "pip_install": ["string"],
                "port": 0,
                "python_version": "pythonVersion",
                "retries": 0,
                "secret_groups": ["string"],
                "timeout_seconds": 0,
                "use_uv": True,
                "warm_instances": 0,
                "workdir": "workdir",
            },
            dockerfile="dockerfile",
            entrypoint_file="entrypointFile",
            environment="environment",
            image="image",
            runtime="python",
        )
        assert_matches_type(V1DeployResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_deploy(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.with_raw_response.deploy(
            entrypoint_name="entrypointName",
            type="task",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1DeployResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_deploy(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.with_streaming_response.deploy(
            entrypoint_name="entrypointName",
            type="task",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1DeployResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_pricing(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.compute.v1.get_pricing()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_pricing(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.with_raw_response.get_pricing()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_pricing(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.with_streaming_response.get_pricing() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_usage(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.compute.v1.get_usage()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_usage_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.compute.v1.get_usage(
            month=3,
            year=2024,
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_usage(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.with_raw_response.get_usage()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_usage(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.with_streaming_response.get_usage() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True
