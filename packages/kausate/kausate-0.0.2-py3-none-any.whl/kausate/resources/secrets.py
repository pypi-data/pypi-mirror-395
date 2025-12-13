# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

import httpx

from ..types import secret_list_params, secret_create_params, secret_delete_params, secret_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.secret_list_response import SecretListResponse
from ..types.secret_response_public import SecretResponsePublic

__all__ = ["SecretsResource", "AsyncSecretsResource"]


class SecretsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SecretsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return SecretsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SecretsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return SecretsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        datasource_slug: str,
        secret_values: Dict[str, str],
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretResponsePublic:
        """Create a new API secret for accessing external data sources.

        Secrets are
        encrypted and stored securely.

        Args:
          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v2/secrets",
            body=maybe_transform(
                {
                    "datasource_slug": datasource_slug,
                    "secret_values": secret_values,
                },
                secret_create_params.SecretCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"partner_customer_id": partner_customer_id}, secret_create_params.SecretCreateParams
                ),
            ),
            cast_to=SecretResponsePublic,
        )

    def update(
        self,
        datasource_slug: str,
        *,
        secret_values: Dict[str, str],
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretResponsePublic:
        """Update an existing secret's value.

        The secret is re-encrypted with the new
        value.

        Args:
          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_slug:
            raise ValueError(f"Expected a non-empty value for `datasource_slug` but received {datasource_slug!r}")
        return self._put(
            f"/v2/secrets/{datasource_slug}",
            body=maybe_transform({"secret_values": secret_values}, secret_update_params.SecretUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"partner_customer_id": partner_customer_id}, secret_update_params.SecretUpdateParams
                ),
            ),
            cast_to=SecretResponsePublic,
        )

    def list(
        self,
        *,
        datasource_slug: Optional[str] | Omit = omit,
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretListResponse:
        """List all secret references for your organization.

        Secret values are never
        returned for security.

        Args:
          datasource_slug: Filter by datasource slug

          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v2/secrets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "datasource_slug": datasource_slug,
                        "partner_customer_id": partner_customer_id,
                    },
                    secret_list_params.SecretListParams,
                ),
            ),
            cast_to=SecretListResponse,
        )

    def delete(
        self,
        datasource_slug: str,
        *,
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Permanently delete a secret.

        This action cannot be undone.

        Args:
          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_slug:
            raise ValueError(f"Expected a non-empty value for `datasource_slug` but received {datasource_slug!r}")
        return self._delete(
            f"/v2/secrets/{datasource_slug}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"partner_customer_id": partner_customer_id}, secret_delete_params.SecretDeleteParams
                ),
            ),
            cast_to=object,
        )


class AsyncSecretsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSecretsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSecretsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSecretsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncSecretsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        datasource_slug: str,
        secret_values: Dict[str, str],
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretResponsePublic:
        """Create a new API secret for accessing external data sources.

        Secrets are
        encrypted and stored securely.

        Args:
          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v2/secrets",
            body=await async_maybe_transform(
                {
                    "datasource_slug": datasource_slug,
                    "secret_values": secret_values,
                },
                secret_create_params.SecretCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"partner_customer_id": partner_customer_id}, secret_create_params.SecretCreateParams
                ),
            ),
            cast_to=SecretResponsePublic,
        )

    async def update(
        self,
        datasource_slug: str,
        *,
        secret_values: Dict[str, str],
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretResponsePublic:
        """Update an existing secret's value.

        The secret is re-encrypted with the new
        value.

        Args:
          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_slug:
            raise ValueError(f"Expected a non-empty value for `datasource_slug` but received {datasource_slug!r}")
        return await self._put(
            f"/v2/secrets/{datasource_slug}",
            body=await async_maybe_transform({"secret_values": secret_values}, secret_update_params.SecretUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"partner_customer_id": partner_customer_id}, secret_update_params.SecretUpdateParams
                ),
            ),
            cast_to=SecretResponsePublic,
        )

    async def list(
        self,
        *,
        datasource_slug: Optional[str] | Omit = omit,
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretListResponse:
        """List all secret references for your organization.

        Secret values are never
        returned for security.

        Args:
          datasource_slug: Filter by datasource slug

          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v2/secrets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "datasource_slug": datasource_slug,
                        "partner_customer_id": partner_customer_id,
                    },
                    secret_list_params.SecretListParams,
                ),
            ),
            cast_to=SecretListResponse,
        )

    async def delete(
        self,
        datasource_slug: str,
        *,
        partner_customer_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Permanently delete a secret.

        This action cannot be undone.

        Args:
          partner_customer_id: Partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_slug:
            raise ValueError(f"Expected a non-empty value for `datasource_slug` but received {datasource_slug!r}")
        return await self._delete(
            f"/v2/secrets/{datasource_slug}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"partner_customer_id": partner_customer_id}, secret_delete_params.SecretDeleteParams
                ),
            ),
            cast_to=object,
        )


class SecretsResourceWithRawResponse:
    def __init__(self, secrets: SecretsResource) -> None:
        self._secrets = secrets

        self.create = to_raw_response_wrapper(
            secrets.create,
        )
        self.update = to_raw_response_wrapper(
            secrets.update,
        )
        self.list = to_raw_response_wrapper(
            secrets.list,
        )
        self.delete = to_raw_response_wrapper(
            secrets.delete,
        )


class AsyncSecretsResourceWithRawResponse:
    def __init__(self, secrets: AsyncSecretsResource) -> None:
        self._secrets = secrets

        self.create = async_to_raw_response_wrapper(
            secrets.create,
        )
        self.update = async_to_raw_response_wrapper(
            secrets.update,
        )
        self.list = async_to_raw_response_wrapper(
            secrets.list,
        )
        self.delete = async_to_raw_response_wrapper(
            secrets.delete,
        )


class SecretsResourceWithStreamingResponse:
    def __init__(self, secrets: SecretsResource) -> None:
        self._secrets = secrets

        self.create = to_streamed_response_wrapper(
            secrets.create,
        )
        self.update = to_streamed_response_wrapper(
            secrets.update,
        )
        self.list = to_streamed_response_wrapper(
            secrets.list,
        )
        self.delete = to_streamed_response_wrapper(
            secrets.delete,
        )


class AsyncSecretsResourceWithStreamingResponse:
    def __init__(self, secrets: AsyncSecretsResource) -> None:
        self._secrets = secrets

        self.create = async_to_streamed_response_wrapper(
            secrets.create,
        )
        self.update = async_to_streamed_response_wrapper(
            secrets.update,
        )
        self.list = async_to_streamed_response_wrapper(
            secrets.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            secrets.delete,
        )
