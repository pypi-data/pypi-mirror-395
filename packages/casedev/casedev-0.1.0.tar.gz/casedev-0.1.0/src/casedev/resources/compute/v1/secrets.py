# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.compute.v1 import (
    secret_list_params,
    secret_create_params,
    secret_delete_group_params,
    secret_update_group_params,
    secret_retrieve_group_params,
)
from ....types.compute.v1.secret_create_response import SecretCreateResponse

__all__ = ["SecretsResource", "AsyncSecretsResource"]


class SecretsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SecretsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return SecretsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SecretsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return SecretsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretCreateResponse:
        """Creates a new secret group in a compute environment.

        Secret groups organize
        related secrets for use in serverless functions and workflows. If no environment
        is specified, the group is created in the default environment.

        **Features:**

        - Organize secrets by logical groups (e.g., database, APIs, third-party
          services)
        - Environment-based isolation
        - Validation of group names
        - Conflict detection for existing groups

        Args:
          name: Unique name for the secret group. Must contain only letters, numbers, hyphens,
              and underscores.

          description: Optional description of the secret group's purpose

          env: Environment name where the secret group will be created. Uses default
              environment if not specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/secrets",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "env": env,
                },
                secret_create_params.SecretCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SecretCreateResponse,
        )

    def list(
        self,
        *,
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Retrieve all secret groups for a compute environment.

        Secret groups organize
        related secrets (API keys, credentials, etc.) that can be securely accessed by
        compute jobs during execution.

        Args:
          env: Environment name to list secret groups for. If not specified, uses the default
              environment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/compute/v1/secrets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"env": env}, secret_list_params.SecretListParams),
            ),
            cast_to=NoneType,
        )

    def delete_group(
        self,
        group: str,
        *,
        env: str | Omit = omit,
        key: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete an entire secret group or a specific key within a secret group.
        Automatically syncs the deletion to Modal compute infrastructure. When deleting
        a specific key, the remaining secrets in the group are re-synced. When deleting
        the entire group, all secrets and the group itself are removed from both the
        database and Modal.

        Args:
          env: Environment name. If not provided, uses the default environment

          key: Specific key to delete within the group. If not provided, the entire group is
              deleted

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group:
            raise ValueError(f"Expected a non-empty value for `group` but received {group!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/compute/v1/secrets/{group}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "env": env,
                        "key": key,
                    },
                    secret_delete_group_params.SecretDeleteGroupParams,
                ),
            ),
            cast_to=NoneType,
        )

    def retrieve_group(
        self,
        group: str,
        *,
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Retrieve the keys (names) of secrets in a specified group within a compute
        environment. For security reasons, actual secret values are not returned - only
        the keys and metadata.

        Args:
          env: Environment name. If not specified, uses the default environment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group:
            raise ValueError(f"Expected a non-empty value for `group` but received {group!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/compute/v1/secrets/{group}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"env": env}, secret_retrieve_group_params.SecretRetrieveGroupParams),
            ),
            cast_to=NoneType,
        )

    def update_group(
        self,
        group: str,
        *,
        secrets: Dict[str, str],
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Set or update secrets in a compute secret group.

        Secrets are encrypted with
        AES-256-GCM and synced to compute infrastructure in real-time. Use this to
        manage environment variables and API keys for your compute workloads.

        Args:
          secrets: Key-value pairs of secrets to set

          env: Environment name (optional, uses default if not specified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group:
            raise ValueError(f"Expected a non-empty value for `group` but received {group!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/compute/v1/secrets/{group}",
            body=maybe_transform(
                {
                    "secrets": secrets,
                    "env": env,
                },
                secret_update_group_params.SecretUpdateGroupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSecretsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSecretsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CaseMark/casedev-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSecretsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSecretsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CaseMark/casedev-python#with_streaming_response
        """
        return AsyncSecretsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretCreateResponse:
        """Creates a new secret group in a compute environment.

        Secret groups organize
        related secrets for use in serverless functions and workflows. If no environment
        is specified, the group is created in the default environment.

        **Features:**

        - Organize secrets by logical groups (e.g., database, APIs, third-party
          services)
        - Environment-based isolation
        - Validation of group names
        - Conflict detection for existing groups

        Args:
          name: Unique name for the secret group. Must contain only letters, numbers, hyphens,
              and underscores.

          description: Optional description of the secret group's purpose

          env: Environment name where the secret group will be created. Uses default
              environment if not specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/secrets",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "env": env,
                },
                secret_create_params.SecretCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SecretCreateResponse,
        )

    async def list(
        self,
        *,
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Retrieve all secret groups for a compute environment.

        Secret groups organize
        related secrets (API keys, credentials, etc.) that can be securely accessed by
        compute jobs during execution.

        Args:
          env: Environment name to list secret groups for. If not specified, uses the default
              environment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/compute/v1/secrets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"env": env}, secret_list_params.SecretListParams),
            ),
            cast_to=NoneType,
        )

    async def delete_group(
        self,
        group: str,
        *,
        env: str | Omit = omit,
        key: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete an entire secret group or a specific key within a secret group.
        Automatically syncs the deletion to Modal compute infrastructure. When deleting
        a specific key, the remaining secrets in the group are re-synced. When deleting
        the entire group, all secrets and the group itself are removed from both the
        database and Modal.

        Args:
          env: Environment name. If not provided, uses the default environment

          key: Specific key to delete within the group. If not provided, the entire group is
              deleted

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group:
            raise ValueError(f"Expected a non-empty value for `group` but received {group!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/compute/v1/secrets/{group}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "env": env,
                        "key": key,
                    },
                    secret_delete_group_params.SecretDeleteGroupParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def retrieve_group(
        self,
        group: str,
        *,
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Retrieve the keys (names) of secrets in a specified group within a compute
        environment. For security reasons, actual secret values are not returned - only
        the keys and metadata.

        Args:
          env: Environment name. If not specified, uses the default environment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group:
            raise ValueError(f"Expected a non-empty value for `group` but received {group!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/compute/v1/secrets/{group}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"env": env}, secret_retrieve_group_params.SecretRetrieveGroupParams),
            ),
            cast_to=NoneType,
        )

    async def update_group(
        self,
        group: str,
        *,
        secrets: Dict[str, str],
        env: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Set or update secrets in a compute secret group.

        Secrets are encrypted with
        AES-256-GCM and synced to compute infrastructure in real-time. Use this to
        manage environment variables and API keys for your compute workloads.

        Args:
          secrets: Key-value pairs of secrets to set

          env: Environment name (optional, uses default if not specified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group:
            raise ValueError(f"Expected a non-empty value for `group` but received {group!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/compute/v1/secrets/{group}",
            body=await async_maybe_transform(
                {
                    "secrets": secrets,
                    "env": env,
                },
                secret_update_group_params.SecretUpdateGroupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SecretsResourceWithRawResponse:
    def __init__(self, secrets: SecretsResource) -> None:
        self._secrets = secrets

        self.create = to_raw_response_wrapper(
            secrets.create,
        )
        self.list = to_raw_response_wrapper(
            secrets.list,
        )
        self.delete_group = to_raw_response_wrapper(
            secrets.delete_group,
        )
        self.retrieve_group = to_raw_response_wrapper(
            secrets.retrieve_group,
        )
        self.update_group = to_raw_response_wrapper(
            secrets.update_group,
        )


class AsyncSecretsResourceWithRawResponse:
    def __init__(self, secrets: AsyncSecretsResource) -> None:
        self._secrets = secrets

        self.create = async_to_raw_response_wrapper(
            secrets.create,
        )
        self.list = async_to_raw_response_wrapper(
            secrets.list,
        )
        self.delete_group = async_to_raw_response_wrapper(
            secrets.delete_group,
        )
        self.retrieve_group = async_to_raw_response_wrapper(
            secrets.retrieve_group,
        )
        self.update_group = async_to_raw_response_wrapper(
            secrets.update_group,
        )


class SecretsResourceWithStreamingResponse:
    def __init__(self, secrets: SecretsResource) -> None:
        self._secrets = secrets

        self.create = to_streamed_response_wrapper(
            secrets.create,
        )
        self.list = to_streamed_response_wrapper(
            secrets.list,
        )
        self.delete_group = to_streamed_response_wrapper(
            secrets.delete_group,
        )
        self.retrieve_group = to_streamed_response_wrapper(
            secrets.retrieve_group,
        )
        self.update_group = to_streamed_response_wrapper(
            secrets.update_group,
        )


class AsyncSecretsResourceWithStreamingResponse:
    def __init__(self, secrets: AsyncSecretsResource) -> None:
        self._secrets = secrets

        self.create = async_to_streamed_response_wrapper(
            secrets.create,
        )
        self.list = async_to_streamed_response_wrapper(
            secrets.list,
        )
        self.delete_group = async_to_streamed_response_wrapper(
            secrets.delete_group,
        )
        self.retrieve_group = async_to_streamed_response_wrapper(
            secrets.retrieve_group,
        )
        self.update_group = async_to_streamed_response_wrapper(
            secrets.update_group,
        )
