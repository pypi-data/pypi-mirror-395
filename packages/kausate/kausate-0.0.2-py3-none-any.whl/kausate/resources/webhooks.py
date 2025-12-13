# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

import httpx

from ..types import WebhookStatus, webhook_create_params, webhook_update_params
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
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
from ..types.webhook_status import WebhookStatus
from ..types.webhook_response import WebhookResponse
from ..types.webhook_list_response import WebhookListResponse

__all__ = ["WebhooksResource", "AsyncWebhooksResource"]


class WebhooksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return WebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return WebhooksResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        url: str,
        api_version: str | Omit = omit,
        custom_headers: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        partner_customer_id: Optional[str] | Omit = omit,
        status: WebhookStatus | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WebhookResponse:
        """
        Create a new webhook for the organization

        Args:
          name: Name of the webhook

          url: URL to receive webhook notifications

          api_version: API version for the webhook

          custom_headers: Custom request headers to include in webhook requests

          description: Optional description

          partner_customer_id: Optional partner customer ID

          status: Webhook status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v2/webhooks",
            body=maybe_transform(
                {
                    "name": name,
                    "url": url,
                    "api_version": api_version,
                    "custom_headers": custom_headers,
                    "description": description,
                    "partner_customer_id": partner_customer_id,
                    "status": status,
                },
                webhook_create_params.WebhookCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookResponse,
        )

    def retrieve(
        self,
        webhook_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WebhookResponse:
        """
        Get a specific webhook

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        return self._get(
            f"/v2/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookResponse,
        )

    def update(
        self,
        webhook_id: str,
        *,
        api_version: Optional[str] | Omit = omit,
        custom_headers: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        partner_customer_id: Optional[str] | Omit = omit,
        status: Optional[WebhookStatus] | Omit = omit,
        url: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WebhookResponse:
        """
        Update a webhook

        Args:
          api_version: API version for the webhook

          custom_headers: Custom request headers to include in webhook requests

          description: Optional description

          name: Name of the webhook

          partner_customer_id: Optional partner customer ID

          status: Status of a webhook configuration.

          url: URL to receive webhook notifications

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        return self._put(
            f"/v2/webhooks/{webhook_id}",
            body=maybe_transform(
                {
                    "api_version": api_version,
                    "custom_headers": custom_headers,
                    "description": description,
                    "name": name,
                    "partner_customer_id": partner_customer_id,
                    "status": status,
                    "url": url,
                },
                webhook_update_params.WebhookUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookResponse,
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
    ) -> WebhookListResponse:
        """List all webhooks for the organization"""
        return self._get(
            "/v2/webhooks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookListResponse,
        )

    def delete(
        self,
        webhook_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a webhook

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/v2/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncWebhooksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncWebhooksResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        url: str,
        api_version: str | Omit = omit,
        custom_headers: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        partner_customer_id: Optional[str] | Omit = omit,
        status: WebhookStatus | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WebhookResponse:
        """
        Create a new webhook for the organization

        Args:
          name: Name of the webhook

          url: URL to receive webhook notifications

          api_version: API version for the webhook

          custom_headers: Custom request headers to include in webhook requests

          description: Optional description

          partner_customer_id: Optional partner customer ID

          status: Webhook status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v2/webhooks",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "url": url,
                    "api_version": api_version,
                    "custom_headers": custom_headers,
                    "description": description,
                    "partner_customer_id": partner_customer_id,
                    "status": status,
                },
                webhook_create_params.WebhookCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookResponse,
        )

    async def retrieve(
        self,
        webhook_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WebhookResponse:
        """
        Get a specific webhook

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        return await self._get(
            f"/v2/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookResponse,
        )

    async def update(
        self,
        webhook_id: str,
        *,
        api_version: Optional[str] | Omit = omit,
        custom_headers: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        partner_customer_id: Optional[str] | Omit = omit,
        status: Optional[WebhookStatus] | Omit = omit,
        url: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WebhookResponse:
        """
        Update a webhook

        Args:
          api_version: API version for the webhook

          custom_headers: Custom request headers to include in webhook requests

          description: Optional description

          name: Name of the webhook

          partner_customer_id: Optional partner customer ID

          status: Status of a webhook configuration.

          url: URL to receive webhook notifications

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        return await self._put(
            f"/v2/webhooks/{webhook_id}",
            body=await async_maybe_transform(
                {
                    "api_version": api_version,
                    "custom_headers": custom_headers,
                    "description": description,
                    "name": name,
                    "partner_customer_id": partner_customer_id,
                    "status": status,
                    "url": url,
                },
                webhook_update_params.WebhookUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookResponse,
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
    ) -> WebhookListResponse:
        """List all webhooks for the organization"""
        return await self._get(
            "/v2/webhooks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookListResponse,
        )

    async def delete(
        self,
        webhook_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a webhook

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/v2/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class WebhooksResourceWithRawResponse:
    def __init__(self, webhooks: WebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = to_raw_response_wrapper(
            webhooks.create,
        )
        self.retrieve = to_raw_response_wrapper(
            webhooks.retrieve,
        )
        self.update = to_raw_response_wrapper(
            webhooks.update,
        )
        self.list = to_raw_response_wrapper(
            webhooks.list,
        )
        self.delete = to_raw_response_wrapper(
            webhooks.delete,
        )


class AsyncWebhooksResourceWithRawResponse:
    def __init__(self, webhooks: AsyncWebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = async_to_raw_response_wrapper(
            webhooks.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            webhooks.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            webhooks.update,
        )
        self.list = async_to_raw_response_wrapper(
            webhooks.list,
        )
        self.delete = async_to_raw_response_wrapper(
            webhooks.delete,
        )


class WebhooksResourceWithStreamingResponse:
    def __init__(self, webhooks: WebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = to_streamed_response_wrapper(
            webhooks.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            webhooks.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            webhooks.update,
        )
        self.list = to_streamed_response_wrapper(
            webhooks.list,
        )
        self.delete = to_streamed_response_wrapper(
            webhooks.delete,
        )


class AsyncWebhooksResourceWithStreamingResponse:
    def __init__(self, webhooks: AsyncWebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = async_to_streamed_response_wrapper(
            webhooks.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            webhooks.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            webhooks.update,
        )
        self.list = async_to_streamed_response_wrapper(
            webhooks.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            webhooks.delete,
        )
