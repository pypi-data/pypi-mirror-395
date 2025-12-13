# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev
from tests.utils import assert_matches_type
from casedev.types import (
    VaultListResponse,
    VaultCreateResponse,
    VaultIngestResponse,
    VaultSearchResponse,
    VaultUploadResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVault:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Casedev) -> None:
        vault = client.vault.create(
            name="Contract Review Archive",
        )
        assert_matches_type(VaultCreateResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Casedev) -> None:
        vault = client.vault.create(
            name="Contract Review Archive",
            description="Repository for all client contract reviews and analysis",
            enable_graph=True,
        )
        assert_matches_type(VaultCreateResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Casedev) -> None:
        response = client.vault.with_raw_response.create(
            name="Contract Review Archive",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(VaultCreateResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Casedev) -> None:
        with client.vault.with_streaming_response.create(
            name="Contract Review Archive",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(VaultCreateResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Casedev) -> None:
        vault = client.vault.retrieve(
            "vault_abc123",
        )
        assert vault is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Casedev) -> None:
        response = client.vault.with_raw_response.retrieve(
            "vault_abc123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert vault is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Casedev) -> None:
        with client.vault.with_streaming_response.retrieve(
            "vault_abc123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert vault is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vault.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Casedev) -> None:
        vault = client.vault.list()
        assert_matches_type(VaultListResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Casedev) -> None:
        response = client.vault.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(VaultListResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Casedev) -> None:
        with client.vault.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(VaultListResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_ingest(self, client: Casedev) -> None:
        vault = client.vault.ingest(
            object_id="objectId",
            id="id",
        )
        assert_matches_type(VaultIngestResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_ingest(self, client: Casedev) -> None:
        response = client.vault.with_raw_response.ingest(
            object_id="objectId",
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(VaultIngestResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_ingest(self, client: Casedev) -> None:
        with client.vault.with_streaming_response.ingest(
            object_id="objectId",
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(VaultIngestResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_ingest(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vault.with_raw_response.ingest(
                object_id="objectId",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            client.vault.with_raw_response.ingest(
                object_id="",
                id="id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Casedev) -> None:
        vault = client.vault.search(
            id="id",
            query="query",
        )
        assert_matches_type(VaultSearchResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Casedev) -> None:
        vault = client.vault.search(
            id="id",
            query="query",
            filters={"foo": "bar"},
            method="vector",
            top_k=1,
        )
        assert_matches_type(VaultSearchResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Casedev) -> None:
        response = client.vault.with_raw_response.search(
            id="id",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(VaultSearchResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Casedev) -> None:
        with client.vault.with_streaming_response.search(
            id="id",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(VaultSearchResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_search(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vault.with_raw_response.search(
                id="",
                query="query",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_upload(self, client: Casedev) -> None:
        vault = client.vault.upload(
            id="id",
            content_type="contentType",
            filename="filename",
        )
        assert_matches_type(VaultUploadResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_upload_with_all_params(self, client: Casedev) -> None:
        vault = client.vault.upload(
            id="id",
            content_type="contentType",
            filename="filename",
            auto_index=True,
            metadata={},
            size_bytes=0,
        )
        assert_matches_type(VaultUploadResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_upload(self, client: Casedev) -> None:
        response = client.vault.with_raw_response.upload(
            id="id",
            content_type="contentType",
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(VaultUploadResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_upload(self, client: Casedev) -> None:
        with client.vault.with_streaming_response.upload(
            id="id",
            content_type="contentType",
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(VaultUploadResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_upload(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vault.with_raw_response.upload(
                id="",
                content_type="contentType",
                filename="filename",
            )


class TestAsyncVault:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.create(
            name="Contract Review Archive",
        )
        assert_matches_type(VaultCreateResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.create(
            name="Contract Review Archive",
            description="Repository for all client contract reviews and analysis",
            enable_graph=True,
        )
        assert_matches_type(VaultCreateResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCasedev) -> None:
        response = await async_client.vault.with_raw_response.create(
            name="Contract Review Archive",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(VaultCreateResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCasedev) -> None:
        async with async_client.vault.with_streaming_response.create(
            name="Contract Review Archive",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(VaultCreateResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.retrieve(
            "vault_abc123",
        )
        assert vault is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCasedev) -> None:
        response = await async_client.vault.with_raw_response.retrieve(
            "vault_abc123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = await response.parse()
        assert vault is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCasedev) -> None:
        async with async_client.vault.with_streaming_response.retrieve(
            "vault_abc123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert vault is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vault.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.list()
        assert_matches_type(VaultListResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCasedev) -> None:
        response = await async_client.vault.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(VaultListResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCasedev) -> None:
        async with async_client.vault.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(VaultListResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_ingest(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.ingest(
            object_id="objectId",
            id="id",
        )
        assert_matches_type(VaultIngestResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_ingest(self, async_client: AsyncCasedev) -> None:
        response = await async_client.vault.with_raw_response.ingest(
            object_id="objectId",
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(VaultIngestResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_ingest(self, async_client: AsyncCasedev) -> None:
        async with async_client.vault.with_streaming_response.ingest(
            object_id="objectId",
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(VaultIngestResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_ingest(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vault.with_raw_response.ingest(
                object_id="objectId",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            await async_client.vault.with_raw_response.ingest(
                object_id="",
                id="id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.search(
            id="id",
            query="query",
        )
        assert_matches_type(VaultSearchResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.search(
            id="id",
            query="query",
            filters={"foo": "bar"},
            method="vector",
            top_k=1,
        )
        assert_matches_type(VaultSearchResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncCasedev) -> None:
        response = await async_client.vault.with_raw_response.search(
            id="id",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(VaultSearchResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncCasedev) -> None:
        async with async_client.vault.with_streaming_response.search(
            id="id",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(VaultSearchResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_search(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vault.with_raw_response.search(
                id="",
                query="query",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_upload(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.upload(
            id="id",
            content_type="contentType",
            filename="filename",
        )
        assert_matches_type(VaultUploadResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_upload_with_all_params(self, async_client: AsyncCasedev) -> None:
        vault = await async_client.vault.upload(
            id="id",
            content_type="contentType",
            filename="filename",
            auto_index=True,
            metadata={},
            size_bytes=0,
        )
        assert_matches_type(VaultUploadResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_upload(self, async_client: AsyncCasedev) -> None:
        response = await async_client.vault.with_raw_response.upload(
            id="id",
            content_type="contentType",
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(VaultUploadResponse, vault, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_upload(self, async_client: AsyncCasedev) -> None:
        async with async_client.vault.with_streaming_response.upload(
            id="id",
            content_type="contentType",
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(VaultUploadResponse, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_upload(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vault.with_raw_response.upload(
                id="",
                content_type="contentType",
                filename="filename",
            )
