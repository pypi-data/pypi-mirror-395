# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal

import httpx

from ...types import vault_create_params, vault_search_params, vault_upload_params
from .objects import (
    ObjectsResource,
    AsyncObjectsResource,
    ObjectsResourceWithRawResponse,
    AsyncObjectsResourceWithRawResponse,
    ObjectsResourceWithStreamingResponse,
    AsyncObjectsResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from .graphrag import (
    GraphragResource,
    AsyncGraphragResource,
    GraphragResourceWithRawResponse,
    AsyncGraphragResourceWithRawResponse,
    GraphragResourceWithStreamingResponse,
    AsyncGraphragResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.vault_list_response import VaultListResponse
from ...types.vault_create_response import VaultCreateResponse
from ...types.vault_ingest_response import VaultIngestResponse
from ...types.vault_search_response import VaultSearchResponse
from ...types.vault_upload_response import VaultUploadResponse

__all__ = ["VaultResource", "AsyncVaultResource"]


class VaultResource(SyncAPIResource):
    @cached_property
    def graphrag(self) -> GraphragResource:
        return GraphragResource(self._client)

    @cached_property
    def objects(self) -> ObjectsResource:
        return ObjectsResource(self._client)

    @cached_property
    def with_raw_response(self) -> VaultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return VaultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VaultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return VaultResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        enable_graph: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultCreateResponse:
        """
        Creates a new secure vault with dedicated S3 storage and vector search
        capabilities. Each vault provides isolated document storage with semantic
        search, OCR processing, and optional knowledge graph features for legal document
        analysis and discovery.

        Args:
          name: Display name for the vault

          description: Optional description of the vault's purpose

          enable_graph: Enable knowledge graph for entity relationship mapping

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/vault",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "enable_graph": enable_graph,
                },
                vault_create_params.VaultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCreateResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Retrieve detailed information about a specific vault, including storage
        configuration, chunking strategy, and usage statistics. Returns vault metadata,
        bucket information, and vector storage details.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/vault/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultListResponse:
        """List all vaults for the authenticated organization.

        Returns vault metadata
        including storage configuration and usage statistics.
        """
        return self._get(
            "/vault",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultListResponse,
        )

    def ingest(
        self,
        object_id: str,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultIngestResponse:
        """
        Triggers OCR ingestion workflow for a vault object to extract text, generate
        chunks, and create embeddings. Processing happens asynchronously with GraphRAG
        support if enabled on the vault. Returns immediately with workflow tracking
        information.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._post(
            f"/vault/{id}/ingest/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultIngestResponse,
        )

    def search(
        self,
        id: str,
        *,
        query: str,
        filters: Dict[str, object] | Omit = omit,
        method: Literal["vector", "graph", "hybrid", "global", "local", "fast", "entity"] | Omit = omit,
        top_k: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultSearchResponse:
        """
        Search across vault documents using multiple methods including hybrid vector +
        graph search, GraphRAG global search, entity-based search, and fast similarity
        search. Returns relevant documents and contextual answers based on the search
        method.

        Args:
          query: Search query or question to find relevant documents

          filters: Additional filters to apply to search results

          method: Search method: 'global' for comprehensive questions, 'entity' for specific
              entities, 'fast' for quick similarity search, 'hybrid' for combined approach

          top_k: Maximum number of results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/vault/{id}/search",
            body=maybe_transform(
                {
                    "query": query,
                    "filters": filters,
                    "method": method,
                    "top_k": top_k,
                },
                vault_search_params.VaultSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultSearchResponse,
        )

    def upload(
        self,
        id: str,
        *,
        content_type: str,
        filename: str,
        auto_index: bool | Omit = omit,
        metadata: object | Omit = omit,
        size_bytes: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultUploadResponse:
        """
        Generate a presigned URL for uploading files directly to a vault's S3 storage.
        This endpoint creates a temporary upload URL that allows secure file uploads
        without exposing credentials. Files can be automatically indexed for semantic
        search or stored for manual processing.

        Args:
          content_type: MIME type of the file (e.g., application/pdf, image/jpeg)

          filename: Name of the file to upload

          auto_index: Whether to automatically process and index the file for search

          metadata: Additional metadata to associate with the file

          size_bytes: Estimated file size in bytes for cost calculation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/vault/{id}/upload",
            body=maybe_transform(
                {
                    "content_type": content_type,
                    "filename": filename,
                    "auto_index": auto_index,
                    "metadata": metadata,
                    "size_bytes": size_bytes,
                },
                vault_upload_params.VaultUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultUploadResponse,
        )


class AsyncVaultResource(AsyncAPIResource):
    @cached_property
    def graphrag(self) -> AsyncGraphragResource:
        return AsyncGraphragResource(self._client)

    @cached_property
    def objects(self) -> AsyncObjectsResource:
        return AsyncObjectsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVaultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVaultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVaultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncVaultResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        enable_graph: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultCreateResponse:
        """
        Creates a new secure vault with dedicated S3 storage and vector search
        capabilities. Each vault provides isolated document storage with semantic
        search, OCR processing, and optional knowledge graph features for legal document
        analysis and discovery.

        Args:
          name: Display name for the vault

          description: Optional description of the vault's purpose

          enable_graph: Enable knowledge graph for entity relationship mapping

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/vault",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "enable_graph": enable_graph,
                },
                vault_create_params.VaultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCreateResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Retrieve detailed information about a specific vault, including storage
        configuration, chunking strategy, and usage statistics. Returns vault metadata,
        bucket information, and vector storage details.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/vault/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultListResponse:
        """List all vaults for the authenticated organization.

        Returns vault metadata
        including storage configuration and usage statistics.
        """
        return await self._get(
            "/vault",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultListResponse,
        )

    async def ingest(
        self,
        object_id: str,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultIngestResponse:
        """
        Triggers OCR ingestion workflow for a vault object to extract text, generate
        chunks, and create embeddings. Processing happens asynchronously with GraphRAG
        support if enabled on the vault. Returns immediately with workflow tracking
        information.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._post(
            f"/vault/{id}/ingest/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultIngestResponse,
        )

    async def search(
        self,
        id: str,
        *,
        query: str,
        filters: Dict[str, object] | Omit = omit,
        method: Literal["vector", "graph", "hybrid", "global", "local", "fast", "entity"] | Omit = omit,
        top_k: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultSearchResponse:
        """
        Search across vault documents using multiple methods including hybrid vector +
        graph search, GraphRAG global search, entity-based search, and fast similarity
        search. Returns relevant documents and contextual answers based on the search
        method.

        Args:
          query: Search query or question to find relevant documents

          filters: Additional filters to apply to search results

          method: Search method: 'global' for comprehensive questions, 'entity' for specific
              entities, 'fast' for quick similarity search, 'hybrid' for combined approach

          top_k: Maximum number of results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/vault/{id}/search",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "filters": filters,
                    "method": method,
                    "top_k": top_k,
                },
                vault_search_params.VaultSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultSearchResponse,
        )

    async def upload(
        self,
        id: str,
        *,
        content_type: str,
        filename: str,
        auto_index: bool | Omit = omit,
        metadata: object | Omit = omit,
        size_bytes: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VaultUploadResponse:
        """
        Generate a presigned URL for uploading files directly to a vault's S3 storage.
        This endpoint creates a temporary upload URL that allows secure file uploads
        without exposing credentials. Files can be automatically indexed for semantic
        search or stored for manual processing.

        Args:
          content_type: MIME type of the file (e.g., application/pdf, image/jpeg)

          filename: Name of the file to upload

          auto_index: Whether to automatically process and index the file for search

          metadata: Additional metadata to associate with the file

          size_bytes: Estimated file size in bytes for cost calculation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/vault/{id}/upload",
            body=await async_maybe_transform(
                {
                    "content_type": content_type,
                    "filename": filename,
                    "auto_index": auto_index,
                    "metadata": metadata,
                    "size_bytes": size_bytes,
                },
                vault_upload_params.VaultUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultUploadResponse,
        )


class VaultResourceWithRawResponse:
    def __init__(self, vault: VaultResource) -> None:
        self._vault = vault

        self.create = to_raw_response_wrapper(
            vault.create,
        )
        self.retrieve = to_raw_response_wrapper(
            vault.retrieve,
        )
        self.list = to_raw_response_wrapper(
            vault.list,
        )
        self.ingest = to_raw_response_wrapper(
            vault.ingest,
        )
        self.search = to_raw_response_wrapper(
            vault.search,
        )
        self.upload = to_raw_response_wrapper(
            vault.upload,
        )

    @cached_property
    def graphrag(self) -> GraphragResourceWithRawResponse:
        return GraphragResourceWithRawResponse(self._vault.graphrag)

    @cached_property
    def objects(self) -> ObjectsResourceWithRawResponse:
        return ObjectsResourceWithRawResponse(self._vault.objects)


class AsyncVaultResourceWithRawResponse:
    def __init__(self, vault: AsyncVaultResource) -> None:
        self._vault = vault

        self.create = async_to_raw_response_wrapper(
            vault.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            vault.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            vault.list,
        )
        self.ingest = async_to_raw_response_wrapper(
            vault.ingest,
        )
        self.search = async_to_raw_response_wrapper(
            vault.search,
        )
        self.upload = async_to_raw_response_wrapper(
            vault.upload,
        )

    @cached_property
    def graphrag(self) -> AsyncGraphragResourceWithRawResponse:
        return AsyncGraphragResourceWithRawResponse(self._vault.graphrag)

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithRawResponse:
        return AsyncObjectsResourceWithRawResponse(self._vault.objects)


class VaultResourceWithStreamingResponse:
    def __init__(self, vault: VaultResource) -> None:
        self._vault = vault

        self.create = to_streamed_response_wrapper(
            vault.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            vault.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            vault.list,
        )
        self.ingest = to_streamed_response_wrapper(
            vault.ingest,
        )
        self.search = to_streamed_response_wrapper(
            vault.search,
        )
        self.upload = to_streamed_response_wrapper(
            vault.upload,
        )

    @cached_property
    def graphrag(self) -> GraphragResourceWithStreamingResponse:
        return GraphragResourceWithStreamingResponse(self._vault.graphrag)

    @cached_property
    def objects(self) -> ObjectsResourceWithStreamingResponse:
        return ObjectsResourceWithStreamingResponse(self._vault.objects)


class AsyncVaultResourceWithStreamingResponse:
    def __init__(self, vault: AsyncVaultResource) -> None:
        self._vault = vault

        self.create = async_to_streamed_response_wrapper(
            vault.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            vault.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            vault.list,
        )
        self.ingest = async_to_streamed_response_wrapper(
            vault.ingest,
        )
        self.search = async_to_streamed_response_wrapper(
            vault.search,
        )
        self.upload = async_to_streamed_response_wrapper(
            vault.upload,
        )

    @cached_property
    def graphrag(self) -> AsyncGraphragResourceWithStreamingResponse:
        return AsyncGraphragResourceWithStreamingResponse(self._vault.graphrag)

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithStreamingResponse:
        return AsyncObjectsResourceWithStreamingResponse(self._vault.objects)
