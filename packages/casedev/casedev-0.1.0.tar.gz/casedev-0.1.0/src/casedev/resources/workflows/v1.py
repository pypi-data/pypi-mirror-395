# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.workflows import (
    v1_list_params,
    v1_create_params,
    v1_update_params,
    v1_execute_params,
    v1_list_executions_params,
)
from ...types.workflows.v1_list_response import V1ListResponse
from ...types.workflows.v1_create_response import V1CreateResponse
from ...types.workflows.v1_delete_response import V1DeleteResponse
from ...types.workflows.v1_deploy_response import V1DeployResponse
from ...types.workflows.v1_update_response import V1UpdateResponse
from ...types.workflows.v1_execute_response import V1ExecuteResponse
from ...types.workflows.v1_retrieve_response import V1RetrieveResponse
from ...types.workflows.v1_undeploy_response import V1UndeployResponse
from ...types.workflows.v1_list_executions_response import V1ListExecutionsResponse
from ...types.workflows.v1_retrieve_execution_response import V1RetrieveExecutionResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> V1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return V1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return V1ResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        edges: Iterable[object] | Omit = omit,
        nodes: Iterable[object] | Omit = omit,
        trigger_config: object | Omit = omit,
        trigger_type: Literal["manual", "webhook", "schedule", "vault_upload"] | Omit = omit,
        visibility: Literal["private", "org", "public"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1CreateResponse:
        """
        Create a new visual workflow with nodes, edges, and trigger configuration.

        Args:
          name: Workflow name

          description: Workflow description

          edges: React Flow edges

          nodes: React Flow nodes

          trigger_config: Trigger configuration

          visibility: Workflow visibility

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/workflows/v1",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "edges": edges,
                    "nodes": nodes,
                    "trigger_config": trigger_config,
                    "trigger_type": trigger_type,
                    "visibility": visibility,
                },
                v1_create_params.V1CreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1CreateResponse,
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
    ) -> V1RetrieveResponse:
        """
        Get a specific workflow by ID with full configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/workflows/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1RetrieveResponse,
        )

    def update(
        self,
        id: str,
        *,
        description: str | Omit = omit,
        edges: Iterable[object] | Omit = omit,
        name: str | Omit = omit,
        nodes: Iterable[object] | Omit = omit,
        trigger_config: object | Omit = omit,
        trigger_type: Literal["manual", "webhook", "schedule", "vault_upload"] | Omit = omit,
        visibility: Literal["private", "org", "public"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1UpdateResponse:
        """
        Update an existing workflow's configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            f"/workflows/v1/{id}",
            body=maybe_transform(
                {
                    "description": description,
                    "edges": edges,
                    "name": name,
                    "nodes": nodes,
                    "trigger_config": trigger_config,
                    "trigger_type": trigger_type,
                    "visibility": visibility,
                },
                v1_update_params.V1UpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1UpdateResponse,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        visibility: Literal["private", "org", "public"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ListResponse:
        """
        List all workflows for the authenticated organization.

        Args:
          limit: Maximum number of results

          offset: Offset for pagination

          visibility: Filter by visibility

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/workflows/v1",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "visibility": visibility,
                    },
                    v1_list_params.V1ListParams,
                ),
            ),
            cast_to=V1ListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1DeleteResponse:
        """
        Delete a workflow and all associated data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            f"/workflows/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeleteResponse,
        )

    def deploy(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1DeployResponse:
        """Deploy a workflow to Modal compute.

        Returns a webhook URL and secret for
        triggering the workflow.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/workflows/v1/{id}/deploy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeployResponse,
        )

    def execute(
        self,
        id: str,
        *,
        body: object | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ExecuteResponse:
        """Execute a workflow for testing.

        This runs the workflow synchronously without
        deployment.

        Args:
          body: Input data to pass to the workflow trigger

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/workflows/v1/{id}/execute",
            body=maybe_transform(body, v1_execute_params.V1ExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ExecuteResponse,
        )

    def list_executions(
        self,
        id: str,
        *,
        limit: int | Omit = omit,
        status: Literal["pending", "running", "completed", "failed", "cancelled"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ListExecutionsResponse:
        """
        List all executions for a specific workflow.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/workflows/v1/{id}/executions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "status": status,
                    },
                    v1_list_executions_params.V1ListExecutionsParams,
                ),
            ),
            cast_to=V1ListExecutionsResponse,
        )

    def retrieve_execution(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1RetrieveExecutionResponse:
        """
        Get detailed information about a workflow execution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/workflows/v1/executions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1RetrieveExecutionResponse,
        )

    def undeploy(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1UndeployResponse:
        """
        Stop a deployed workflow and release its webhook URL.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            f"/workflows/v1/{id}/deploy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1UndeployResponse,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncV1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncV1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncV1ResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        edges: Iterable[object] | Omit = omit,
        nodes: Iterable[object] | Omit = omit,
        trigger_config: object | Omit = omit,
        trigger_type: Literal["manual", "webhook", "schedule", "vault_upload"] | Omit = omit,
        visibility: Literal["private", "org", "public"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1CreateResponse:
        """
        Create a new visual workflow with nodes, edges, and trigger configuration.

        Args:
          name: Workflow name

          description: Workflow description

          edges: React Flow edges

          nodes: React Flow nodes

          trigger_config: Trigger configuration

          visibility: Workflow visibility

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/workflows/v1",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "edges": edges,
                    "nodes": nodes,
                    "trigger_config": trigger_config,
                    "trigger_type": trigger_type,
                    "visibility": visibility,
                },
                v1_create_params.V1CreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1CreateResponse,
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
    ) -> V1RetrieveResponse:
        """
        Get a specific workflow by ID with full configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/workflows/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1RetrieveResponse,
        )

    async def update(
        self,
        id: str,
        *,
        description: str | Omit = omit,
        edges: Iterable[object] | Omit = omit,
        name: str | Omit = omit,
        nodes: Iterable[object] | Omit = omit,
        trigger_config: object | Omit = omit,
        trigger_type: Literal["manual", "webhook", "schedule", "vault_upload"] | Omit = omit,
        visibility: Literal["private", "org", "public"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1UpdateResponse:
        """
        Update an existing workflow's configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            f"/workflows/v1/{id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "edges": edges,
                    "name": name,
                    "nodes": nodes,
                    "trigger_config": trigger_config,
                    "trigger_type": trigger_type,
                    "visibility": visibility,
                },
                v1_update_params.V1UpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1UpdateResponse,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        visibility: Literal["private", "org", "public"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ListResponse:
        """
        List all workflows for the authenticated organization.

        Args:
          limit: Maximum number of results

          offset: Offset for pagination

          visibility: Filter by visibility

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/workflows/v1",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "visibility": visibility,
                    },
                    v1_list_params.V1ListParams,
                ),
            ),
            cast_to=V1ListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1DeleteResponse:
        """
        Delete a workflow and all associated data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            f"/workflows/v1/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeleteResponse,
        )

    async def deploy(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1DeployResponse:
        """Deploy a workflow to Modal compute.

        Returns a webhook URL and secret for
        triggering the workflow.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/workflows/v1/{id}/deploy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeployResponse,
        )

    async def execute(
        self,
        id: str,
        *,
        body: object | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ExecuteResponse:
        """Execute a workflow for testing.

        This runs the workflow synchronously without
        deployment.

        Args:
          body: Input data to pass to the workflow trigger

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/workflows/v1/{id}/execute",
            body=await async_maybe_transform(body, v1_execute_params.V1ExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1ExecuteResponse,
        )

    async def list_executions(
        self,
        id: str,
        *,
        limit: int | Omit = omit,
        status: Literal["pending", "running", "completed", "failed", "cancelled"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1ListExecutionsResponse:
        """
        List all executions for a specific workflow.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/workflows/v1/{id}/executions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "status": status,
                    },
                    v1_list_executions_params.V1ListExecutionsParams,
                ),
            ),
            cast_to=V1ListExecutionsResponse,
        )

    async def retrieve_execution(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1RetrieveExecutionResponse:
        """
        Get detailed information about a workflow execution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/workflows/v1/executions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1RetrieveExecutionResponse,
        )

    async def undeploy(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1UndeployResponse:
        """
        Stop a deployed workflow and release its webhook URL.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            f"/workflows/v1/{id}/deploy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1UndeployResponse,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create = to_raw_response_wrapper(
            v1.create,
        )
        self.retrieve = to_raw_response_wrapper(
            v1.retrieve,
        )
        self.update = to_raw_response_wrapper(
            v1.update,
        )
        self.list = to_raw_response_wrapper(
            v1.list,
        )
        self.delete = to_raw_response_wrapper(
            v1.delete,
        )
        self.deploy = to_raw_response_wrapper(
            v1.deploy,
        )
        self.execute = to_raw_response_wrapper(
            v1.execute,
        )
        self.list_executions = to_raw_response_wrapper(
            v1.list_executions,
        )
        self.retrieve_execution = to_raw_response_wrapper(
            v1.retrieve_execution,
        )
        self.undeploy = to_raw_response_wrapper(
            v1.undeploy,
        )


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create = async_to_raw_response_wrapper(
            v1.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            v1.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            v1.update,
        )
        self.list = async_to_raw_response_wrapper(
            v1.list,
        )
        self.delete = async_to_raw_response_wrapper(
            v1.delete,
        )
        self.deploy = async_to_raw_response_wrapper(
            v1.deploy,
        )
        self.execute = async_to_raw_response_wrapper(
            v1.execute,
        )
        self.list_executions = async_to_raw_response_wrapper(
            v1.list_executions,
        )
        self.retrieve_execution = async_to_raw_response_wrapper(
            v1.retrieve_execution,
        )
        self.undeploy = async_to_raw_response_wrapper(
            v1.undeploy,
        )


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create = to_streamed_response_wrapper(
            v1.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            v1.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            v1.update,
        )
        self.list = to_streamed_response_wrapper(
            v1.list,
        )
        self.delete = to_streamed_response_wrapper(
            v1.delete,
        )
        self.deploy = to_streamed_response_wrapper(
            v1.deploy,
        )
        self.execute = to_streamed_response_wrapper(
            v1.execute,
        )
        self.list_executions = to_streamed_response_wrapper(
            v1.list_executions,
        )
        self.retrieve_execution = to_streamed_response_wrapper(
            v1.retrieve_execution,
        )
        self.undeploy = to_streamed_response_wrapper(
            v1.undeploy,
        )


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create = async_to_streamed_response_wrapper(
            v1.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            v1.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            v1.update,
        )
        self.list = async_to_streamed_response_wrapper(
            v1.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            v1.delete,
        )
        self.deploy = async_to_streamed_response_wrapper(
            v1.deploy,
        )
        self.execute = async_to_streamed_response_wrapper(
            v1.execute,
        )
        self.list_executions = async_to_streamed_response_wrapper(
            v1.list_executions,
        )
        self.retrieve_execution = async_to_streamed_response_wrapper(
            v1.retrieve_execution,
        )
        self.undeploy = async_to_streamed_response_wrapper(
            v1.undeploy,
        )
