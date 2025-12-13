# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev
from tests.utils import assert_matches_type
from casedev.types.compute.v1 import (
    SecretCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSecrets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.create(
            name="name",
        )
        assert_matches_type(SecretCreateResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.create(
            name="name",
            description="description",
            env="env",
        )
        assert_matches_type(SecretCreateResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Casedev) -> None:
        response = client.compute.v1.secrets.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(SecretCreateResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Casedev) -> None:
        with client.compute.v1.secrets.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(SecretCreateResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.list()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.list(
            env="env",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Casedev) -> None:
        response = client.compute.v1.secrets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Casedev) -> None:
        with client.compute.v1.secrets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_group(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.delete_group(
            group="group",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_group_with_all_params(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.delete_group(
            group="group",
            env="env",
            key="key",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete_group(self, client: Casedev) -> None:
        response = client.compute.v1.secrets.with_raw_response.delete_group(
            group="group",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete_group(self, client: Casedev) -> None:
        with client.compute.v1.secrets.with_streaming_response.delete_group(
            group="group",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete_group(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group` but received ''"):
            client.compute.v1.secrets.with_raw_response.delete_group(
                group="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_group(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.retrieve_group(
            group="group",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_group_with_all_params(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.retrieve_group(
            group="group",
            env="env",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_group(self, client: Casedev) -> None:
        response = client.compute.v1.secrets.with_raw_response.retrieve_group(
            group="group",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_group(self, client: Casedev) -> None:
        with client.compute.v1.secrets.with_streaming_response.retrieve_group(
            group="group",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve_group(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group` but received ''"):
            client.compute.v1.secrets.with_raw_response.retrieve_group(
                group="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_group(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_group_with_all_params(self, client: Casedev) -> None:
        secret = client.compute.v1.secrets.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
            env="env",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update_group(self, client: Casedev) -> None:
        response = client.compute.v1.secrets.with_raw_response.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update_group(self, client: Casedev) -> None:
        with client.compute.v1.secrets.with_streaming_response.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update_group(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group` but received ''"):
            client.compute.v1.secrets.with_raw_response.update_group(
                group="",
                secrets={"foo": "string"},
            )


class TestAsyncSecrets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.create(
            name="name",
        )
        assert_matches_type(SecretCreateResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.create(
            name="name",
            description="description",
            env="env",
        )
        assert_matches_type(SecretCreateResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.secrets.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(SecretCreateResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.secrets.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(SecretCreateResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.list()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.list(
            env="env",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.secrets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.secrets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_group(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.delete_group(
            group="group",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_group_with_all_params(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.delete_group(
            group="group",
            env="env",
            key="key",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete_group(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.secrets.with_raw_response.delete_group(
            group="group",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete_group(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.secrets.with_streaming_response.delete_group(
            group="group",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete_group(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group` but received ''"):
            await async_client.compute.v1.secrets.with_raw_response.delete_group(
                group="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_group(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.retrieve_group(
            group="group",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_group_with_all_params(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.retrieve_group(
            group="group",
            env="env",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_group(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.secrets.with_raw_response.retrieve_group(
            group="group",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_group(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.secrets.with_streaming_response.retrieve_group(
            group="group",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve_group(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group` but received ''"):
            await async_client.compute.v1.secrets.with_raw_response.retrieve_group(
                group="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_group(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_group_with_all_params(self, async_client: AsyncCasedev) -> None:
        secret = await async_client.compute.v1.secrets.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
            env="env",
        )
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update_group(self, async_client: AsyncCasedev) -> None:
        response = await async_client.compute.v1.secrets.with_raw_response.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert secret is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update_group(self, async_client: AsyncCasedev) -> None:
        async with async_client.compute.v1.secrets.with_streaming_response.update_group(
            group="litigation-apis",
            secrets={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert secret is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update_group(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group` but received ''"):
            await async_client.compute.v1.secrets.with_raw_response.update_group(
                group="",
                secrets={"foo": "string"},
            )
