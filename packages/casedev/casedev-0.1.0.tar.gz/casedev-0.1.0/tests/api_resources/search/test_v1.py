# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from casedev import Casedev, AsyncCasedev
from tests.utils import assert_matches_type
from casedev._utils import parse_date
from casedev.types.search import (
    V1AnswerResponse,
    V1SearchResponse,
    V1SimilarResponse,
    V1ContentsResponse,
    V1ResearchResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_answer(self, client: Casedev) -> None:
        v1 = client.search.v1.answer(
            query="query",
        )
        assert_matches_type(V1AnswerResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_answer_with_all_params(self, client: Casedev) -> None:
        v1 = client.search.v1.answer(
            query="query",
            exclude_domains=["string"],
            include_domains=["string"],
            max_tokens=0,
            model="model",
            num_results=1,
            search_type="auto",
            stream=True,
            temperature=0,
            text=True,
            use_custom_llm=True,
        )
        assert_matches_type(V1AnswerResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_answer(self, client: Casedev) -> None:
        response = client.search.v1.with_raw_response.answer(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1AnswerResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_answer(self, client: Casedev) -> None:
        with client.search.v1.with_streaming_response.answer(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1AnswerResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_contents(self, client: Casedev) -> None:
        v1 = client.search.v1.contents(
            urls=["https://example.com"],
        )
        assert_matches_type(V1ContentsResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_contents_with_all_params(self, client: Casedev) -> None:
        v1 = client.search.v1.contents(
            urls=["https://example.com"],
            context="context",
            extras={},
            highlights=True,
            livecrawl=True,
            livecrawl_timeout=0,
            subpages=True,
            subpage_target=0,
            summary=True,
            text=True,
        )
        assert_matches_type(V1ContentsResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_contents(self, client: Casedev) -> None:
        response = client.search.v1.with_raw_response.contents(
            urls=["https://example.com"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1ContentsResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_contents(self, client: Casedev) -> None:
        with client.search.v1.with_streaming_response.contents(
            urls=["https://example.com"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1ContentsResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_research(self, client: Casedev) -> None:
        v1 = client.search.v1.research(
            instructions="instructions",
        )
        assert_matches_type(V1ResearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_research_with_all_params(self, client: Casedev) -> None:
        v1 = client.search.v1.research(
            instructions="instructions",
            model="fast",
            output_schema={},
            query="query",
        )
        assert_matches_type(V1ResearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_research(self, client: Casedev) -> None:
        response = client.search.v1.with_raw_response.research(
            instructions="instructions",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1ResearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_research(self, client: Casedev) -> None:
        with client.search.v1.with_streaming_response.research(
            instructions="instructions",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1ResearchResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_research(self, client: Casedev) -> None:
        v1 = client.search.v1.retrieve_research(
            id="id",
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_research_with_all_params(self, client: Casedev) -> None:
        v1 = client.search.v1.retrieve_research(
            id="id",
            events="events",
            stream=True,
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_research(self, client: Casedev) -> None:
        response = client.search.v1.with_raw_response.retrieve_research(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_research(self, client: Casedev) -> None:
        with client.search.v1.with_streaming_response.retrieve_research(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve_research(self, client: Casedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.search.v1.with_raw_response.retrieve_research(
                id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Casedev) -> None:
        v1 = client.search.v1.search(
            query="query",
        )
        assert_matches_type(V1SearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Casedev) -> None:
        v1 = client.search.v1.search(
            query="query",
            additional_queries=["string"],
            category="category",
            contents="contents",
            end_crawl_date=parse_date("2019-12-27"),
            end_published_date=parse_date("2019-12-27"),
            exclude_domains=["string"],
            include_domains=["string"],
            include_text=True,
            num_results=1,
            start_crawl_date=parse_date("2019-12-27"),
            start_published_date=parse_date("2019-12-27"),
            type="auto",
            user_location="userLocation",
        )
        assert_matches_type(V1SearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Casedev) -> None:
        response = client.search.v1.with_raw_response.search(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1SearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Casedev) -> None:
        with client.search.v1.with_streaming_response.search(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1SearchResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_similar(self, client: Casedev) -> None:
        v1 = client.search.v1.similar(
            url="https://example.com",
        )
        assert_matches_type(V1SimilarResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_similar_with_all_params(self, client: Casedev) -> None:
        v1 = client.search.v1.similar(
            url="https://example.com",
            contents="contents",
            end_crawl_date=parse_date("2019-12-27"),
            end_published_date=parse_date("2019-12-27"),
            exclude_domains=["string"],
            include_domains=["string"],
            include_text=True,
            num_results=1,
            start_crawl_date=parse_date("2019-12-27"),
            start_published_date=parse_date("2019-12-27"),
        )
        assert_matches_type(V1SimilarResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_similar(self, client: Casedev) -> None:
        response = client.search.v1.with_raw_response.similar(
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1SimilarResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_similar(self, client: Casedev) -> None:
        with client.search.v1.with_streaming_response.similar(
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1SimilarResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncV1:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_answer(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.answer(
            query="query",
        )
        assert_matches_type(V1AnswerResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_answer_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.answer(
            query="query",
            exclude_domains=["string"],
            include_domains=["string"],
            max_tokens=0,
            model="model",
            num_results=1,
            search_type="auto",
            stream=True,
            temperature=0,
            text=True,
            use_custom_llm=True,
        )
        assert_matches_type(V1AnswerResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_answer(self, async_client: AsyncCasedev) -> None:
        response = await async_client.search.v1.with_raw_response.answer(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1AnswerResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_answer(self, async_client: AsyncCasedev) -> None:
        async with async_client.search.v1.with_streaming_response.answer(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1AnswerResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_contents(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.contents(
            urls=["https://example.com"],
        )
        assert_matches_type(V1ContentsResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_contents_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.contents(
            urls=["https://example.com"],
            context="context",
            extras={},
            highlights=True,
            livecrawl=True,
            livecrawl_timeout=0,
            subpages=True,
            subpage_target=0,
            summary=True,
            text=True,
        )
        assert_matches_type(V1ContentsResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_contents(self, async_client: AsyncCasedev) -> None:
        response = await async_client.search.v1.with_raw_response.contents(
            urls=["https://example.com"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1ContentsResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_contents(self, async_client: AsyncCasedev) -> None:
        async with async_client.search.v1.with_streaming_response.contents(
            urls=["https://example.com"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1ContentsResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_research(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.research(
            instructions="instructions",
        )
        assert_matches_type(V1ResearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_research_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.research(
            instructions="instructions",
            model="fast",
            output_schema={},
            query="query",
        )
        assert_matches_type(V1ResearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_research(self, async_client: AsyncCasedev) -> None:
        response = await async_client.search.v1.with_raw_response.research(
            instructions="instructions",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1ResearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_research(self, async_client: AsyncCasedev) -> None:
        async with async_client.search.v1.with_streaming_response.research(
            instructions="instructions",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1ResearchResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_research(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.retrieve_research(
            id="id",
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_research_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.retrieve_research(
            id="id",
            events="events",
            stream=True,
        )
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_research(self, async_client: AsyncCasedev) -> None:
        response = await async_client.search.v1.with_raw_response.retrieve_research(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert v1 is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_research(self, async_client: AsyncCasedev) -> None:
        async with async_client.search.v1.with_streaming_response.retrieve_research(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert v1 is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve_research(self, async_client: AsyncCasedev) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.search.v1.with_raw_response.retrieve_research(
                id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.search(
            query="query",
        )
        assert_matches_type(V1SearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.search(
            query="query",
            additional_queries=["string"],
            category="category",
            contents="contents",
            end_crawl_date=parse_date("2019-12-27"),
            end_published_date=parse_date("2019-12-27"),
            exclude_domains=["string"],
            include_domains=["string"],
            include_text=True,
            num_results=1,
            start_crawl_date=parse_date("2019-12-27"),
            start_published_date=parse_date("2019-12-27"),
            type="auto",
            user_location="userLocation",
        )
        assert_matches_type(V1SearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncCasedev) -> None:
        response = await async_client.search.v1.with_raw_response.search(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1SearchResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncCasedev) -> None:
        async with async_client.search.v1.with_streaming_response.search(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1SearchResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_similar(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.similar(
            url="https://example.com",
        )
        assert_matches_type(V1SimilarResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_similar_with_all_params(self, async_client: AsyncCasedev) -> None:
        v1 = await async_client.search.v1.similar(
            url="https://example.com",
            contents="contents",
            end_crawl_date=parse_date("2019-12-27"),
            end_published_date=parse_date("2019-12-27"),
            exclude_domains=["string"],
            include_domains=["string"],
            include_text=True,
            num_results=1,
            start_crawl_date=parse_date("2019-12-27"),
            start_published_date=parse_date("2019-12-27"),
        )
        assert_matches_type(V1SimilarResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_similar(self, async_client: AsyncCasedev) -> None:
        response = await async_client.search.v1.with_raw_response.similar(
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1SimilarResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_similar(self, async_client: AsyncCasedev) -> None:
        async with async_client.search.v1.with_streaming_response.similar(
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1SimilarResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True
