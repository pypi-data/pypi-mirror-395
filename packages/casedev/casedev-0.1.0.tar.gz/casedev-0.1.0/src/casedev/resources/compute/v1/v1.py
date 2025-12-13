# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .runs import (
    RunsResource,
    AsyncRunsResource,
    RunsResourceWithRawResponse,
    AsyncRunsResourceWithRawResponse,
    RunsResourceWithStreamingResponse,
    AsyncRunsResourceWithStreamingResponse,
)
from .invoke import (
    InvokeResource,
    AsyncInvokeResource,
    InvokeResourceWithRawResponse,
    AsyncInvokeResourceWithRawResponse,
    InvokeResourceWithStreamingResponse,
    AsyncInvokeResourceWithStreamingResponse,
)
from .secrets import (
    SecretsResource,
    AsyncSecretsResource,
    SecretsResourceWithRawResponse,
    AsyncSecretsResourceWithRawResponse,
    SecretsResourceWithStreamingResponse,
    AsyncSecretsResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from .functions import (
    FunctionsResource,
    AsyncFunctionsResource,
    FunctionsResourceWithRawResponse,
    AsyncFunctionsResourceWithRawResponse,
    FunctionsResourceWithStreamingResponse,
    AsyncFunctionsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .environments import (
    EnvironmentsResource,
    AsyncEnvironmentsResource,
    EnvironmentsResourceWithRawResponse,
    AsyncEnvironmentsResourceWithRawResponse,
    EnvironmentsResourceWithStreamingResponse,
    AsyncEnvironmentsResourceWithStreamingResponse,
)
from ...._base_client import make_request_options
from ....types.compute import v1_deploy_params, v1_get_usage_params
from ....types.compute.v1_deploy_response import V1DeployResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def environments(self) -> EnvironmentsResource:
        return EnvironmentsResource(self._client)

    @cached_property
    def functions(self) -> FunctionsResource:
        return FunctionsResource(self._client)

    @cached_property
    def invoke(self) -> InvokeResource:
        return InvokeResource(self._client)

    @cached_property
    def runs(self) -> RunsResource:
        return RunsResource(self._client)

    @cached_property
    def secrets(self) -> SecretsResource:
        return SecretsResource(self._client)

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

    def deploy(
        self,
        *,
        entrypoint_name: str,
        type: Literal["task", "service"],
        code: str | Omit = omit,
        config: v1_deploy_params.Config | Omit = omit,
        dockerfile: str | Omit = omit,
        entrypoint_file: str | Omit = omit,
        environment: str | Omit = omit,
        image: str | Omit = omit,
        runtime: Literal["python", "dockerfile", "image"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1DeployResponse:
        """
        Deploy code to Case.dev's serverless compute infrastructure powered by Modal.
        Supports Python, Dockerfile, and container image runtimes with GPU acceleration
        for AI/ML workloads. Code is deployed as tasks (batch jobs) or services (web
        endpoints) with automatic scaling.

        Args:
          entrypoint_name: Function/app name (used for domain: hello → hello.org.case.systems)

          type: Deployment type: task for batch jobs, service for web endpoints

          code: Python code (required for python runtime)

          config: Runtime and resource configuration

          dockerfile: Dockerfile content (required for dockerfile runtime)

          entrypoint_file: Python entrypoint file name

          environment: Environment name (uses default if not specified)

          image: Container image name (required for image runtime, e.g.,
              'nvidia/cuda:12.8.1-devel-ubuntu22.04')

          runtime: Runtime environment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/deploy",
            body=maybe_transform(
                {
                    "entrypoint_name": entrypoint_name,
                    "type": type,
                    "code": code,
                    "config": config,
                    "dockerfile": dockerfile,
                    "entrypoint_file": entrypoint_file,
                    "environment": environment,
                    "image": image,
                    "runtime": runtime,
                },
                v1_deploy_params.V1DeployParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeployResponse,
        )

    def get_pricing(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Returns current pricing for GPU and CPU compute resources.

        This public endpoint
        provides detailed pricing information for all available compute types, including
        GPU instances and CPU cores, with billing model details.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/compute/v1/pricing",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_usage(
        self,
        *,
        month: int | Omit = omit,
        year: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Returns detailed compute usage statistics and billing information for your
        organization. Includes GPU and CPU hours, total runs, costs, and breakdowns by
        environment. Use optional query parameters to filter by specific year and month.

        Args:
          month: Month to filter usage data (1-12, defaults to current month)

          year: Year to filter usage data (defaults to current year)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/compute/v1/usage",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "month": month,
                        "year": year,
                    },
                    v1_get_usage_params.V1GetUsageParams,
                ),
            ),
            cast_to=NoneType,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def environments(self) -> AsyncEnvironmentsResource:
        return AsyncEnvironmentsResource(self._client)

    @cached_property
    def functions(self) -> AsyncFunctionsResource:
        return AsyncFunctionsResource(self._client)

    @cached_property
    def invoke(self) -> AsyncInvokeResource:
        return AsyncInvokeResource(self._client)

    @cached_property
    def runs(self) -> AsyncRunsResource:
        return AsyncRunsResource(self._client)

    @cached_property
    def secrets(self) -> AsyncSecretsResource:
        return AsyncSecretsResource(self._client)

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

    async def deploy(
        self,
        *,
        entrypoint_name: str,
        type: Literal["task", "service"],
        code: str | Omit = omit,
        config: v1_deploy_params.Config | Omit = omit,
        dockerfile: str | Omit = omit,
        entrypoint_file: str | Omit = omit,
        environment: str | Omit = omit,
        image: str | Omit = omit,
        runtime: Literal["python", "dockerfile", "image"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> V1DeployResponse:
        """
        Deploy code to Case.dev's serverless compute infrastructure powered by Modal.
        Supports Python, Dockerfile, and container image runtimes with GPU acceleration
        for AI/ML workloads. Code is deployed as tasks (batch jobs) or services (web
        endpoints) with automatic scaling.

        Args:
          entrypoint_name: Function/app name (used for domain: hello → hello.org.case.systems)

          type: Deployment type: task for batch jobs, service for web endpoints

          code: Python code (required for python runtime)

          config: Runtime and resource configuration

          dockerfile: Dockerfile content (required for dockerfile runtime)

          entrypoint_file: Python entrypoint file name

          environment: Environment name (uses default if not specified)

          image: Container image name (required for image runtime, e.g.,
              'nvidia/cuda:12.8.1-devel-ubuntu22.04')

          runtime: Runtime environment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/deploy",
            body=await async_maybe_transform(
                {
                    "entrypoint_name": entrypoint_name,
                    "type": type,
                    "code": code,
                    "config": config,
                    "dockerfile": dockerfile,
                    "entrypoint_file": entrypoint_file,
                    "environment": environment,
                    "image": image,
                    "runtime": runtime,
                },
                v1_deploy_params.V1DeployParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeployResponse,
        )

    async def get_pricing(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Returns current pricing for GPU and CPU compute resources.

        This public endpoint
        provides detailed pricing information for all available compute types, including
        GPU instances and CPU cores, with billing model details.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/compute/v1/pricing",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_usage(
        self,
        *,
        month: int | Omit = omit,
        year: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Returns detailed compute usage statistics and billing information for your
        organization. Includes GPU and CPU hours, total runs, costs, and breakdowns by
        environment. Use optional query parameters to filter by specific year and month.

        Args:
          month: Month to filter usage data (1-12, defaults to current month)

          year: Year to filter usage data (defaults to current year)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/compute/v1/usage",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "month": month,
                        "year": year,
                    },
                    v1_get_usage_params.V1GetUsageParams,
                ),
            ),
            cast_to=NoneType,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.deploy = to_raw_response_wrapper(
            v1.deploy,
        )
        self.get_pricing = to_raw_response_wrapper(
            v1.get_pricing,
        )
        self.get_usage = to_raw_response_wrapper(
            v1.get_usage,
        )

    @cached_property
    def environments(self) -> EnvironmentsResourceWithRawResponse:
        return EnvironmentsResourceWithRawResponse(self._v1.environments)

    @cached_property
    def functions(self) -> FunctionsResourceWithRawResponse:
        return FunctionsResourceWithRawResponse(self._v1.functions)

    @cached_property
    def invoke(self) -> InvokeResourceWithRawResponse:
        return InvokeResourceWithRawResponse(self._v1.invoke)

    @cached_property
    def runs(self) -> RunsResourceWithRawResponse:
        return RunsResourceWithRawResponse(self._v1.runs)

    @cached_property
    def secrets(self) -> SecretsResourceWithRawResponse:
        return SecretsResourceWithRawResponse(self._v1.secrets)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.deploy = async_to_raw_response_wrapper(
            v1.deploy,
        )
        self.get_pricing = async_to_raw_response_wrapper(
            v1.get_pricing,
        )
        self.get_usage = async_to_raw_response_wrapper(
            v1.get_usage,
        )

    @cached_property
    def environments(self) -> AsyncEnvironmentsResourceWithRawResponse:
        return AsyncEnvironmentsResourceWithRawResponse(self._v1.environments)

    @cached_property
    def functions(self) -> AsyncFunctionsResourceWithRawResponse:
        return AsyncFunctionsResourceWithRawResponse(self._v1.functions)

    @cached_property
    def invoke(self) -> AsyncInvokeResourceWithRawResponse:
        return AsyncInvokeResourceWithRawResponse(self._v1.invoke)

    @cached_property
    def runs(self) -> AsyncRunsResourceWithRawResponse:
        return AsyncRunsResourceWithRawResponse(self._v1.runs)

    @cached_property
    def secrets(self) -> AsyncSecretsResourceWithRawResponse:
        return AsyncSecretsResourceWithRawResponse(self._v1.secrets)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.deploy = to_streamed_response_wrapper(
            v1.deploy,
        )
        self.get_pricing = to_streamed_response_wrapper(
            v1.get_pricing,
        )
        self.get_usage = to_streamed_response_wrapper(
            v1.get_usage,
        )

    @cached_property
    def environments(self) -> EnvironmentsResourceWithStreamingResponse:
        return EnvironmentsResourceWithStreamingResponse(self._v1.environments)

    @cached_property
    def functions(self) -> FunctionsResourceWithStreamingResponse:
        return FunctionsResourceWithStreamingResponse(self._v1.functions)

    @cached_property
    def invoke(self) -> InvokeResourceWithStreamingResponse:
        return InvokeResourceWithStreamingResponse(self._v1.invoke)

    @cached_property
    def runs(self) -> RunsResourceWithStreamingResponse:
        return RunsResourceWithStreamingResponse(self._v1.runs)

    @cached_property
    def secrets(self) -> SecretsResourceWithStreamingResponse:
        return SecretsResourceWithStreamingResponse(self._v1.secrets)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.deploy = async_to_streamed_response_wrapper(
            v1.deploy,
        )
        self.get_pricing = async_to_streamed_response_wrapper(
            v1.get_pricing,
        )
        self.get_usage = async_to_streamed_response_wrapper(
            v1.get_usage,
        )

    @cached_property
    def environments(self) -> AsyncEnvironmentsResourceWithStreamingResponse:
        return AsyncEnvironmentsResourceWithStreamingResponse(self._v1.environments)

    @cached_property
    def functions(self) -> AsyncFunctionsResourceWithStreamingResponse:
        return AsyncFunctionsResourceWithStreamingResponse(self._v1.functions)

    @cached_property
    def invoke(self) -> AsyncInvokeResourceWithStreamingResponse:
        return AsyncInvokeResourceWithStreamingResponse(self._v1.invoke)

    @cached_property
    def runs(self) -> AsyncRunsResourceWithStreamingResponse:
        return AsyncRunsResourceWithStreamingResponse(self._v1.runs)

    @cached_property
    def secrets(self) -> AsyncSecretsResourceWithStreamingResponse:
        return AsyncSecretsResourceWithStreamingResponse(self._v1.secrets)
