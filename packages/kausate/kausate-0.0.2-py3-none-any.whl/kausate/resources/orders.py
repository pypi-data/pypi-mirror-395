# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ..types import order_list_params, order_retrieve_params
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
from ..types.order_list_response import OrderListResponse
from ..types.order_retrieve_response import OrderRetrieveResponse

__all__ = ["OrdersResource", "AsyncOrdersResource"]


class OrdersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OrdersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return OrdersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrdersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return OrdersResourceWithStreamingResponse(self)

    def retrieve(
        self,
        order_id: str,
        *,
        customer_partner_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderRetrieveResponse:
        """
        Retrieve detailed information about a specific order.

        Args:
          order_id: Order ID to retrieve details for

          customer_partner_id: Optional customer partner ID for validation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return self._get(
            f"/v2/orders/{order_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"customer_partner_id": customer_partner_id}, order_retrieve_params.OrderRetrieveParams
                ),
            ),
            cast_to=OrderRetrieveResponse,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        workflow_type: Optional[Literal["DocumentRetrieval", "CompanyReport", "ShareholderGraph", "UBOExtraction"]]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderListResponse:
        """
        Retrieve a list of orders for your organization.

        Args:
          limit: Maximum number of orders to return

          workflow_type: Available workflow types for filtering orders.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v2/orders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "workflow_type": workflow_type,
                    },
                    order_list_params.OrderListParams,
                ),
            ),
            cast_to=OrderListResponse,
        )


class AsyncOrdersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOrdersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOrdersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrdersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncOrdersResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        order_id: str,
        *,
        customer_partner_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderRetrieveResponse:
        """
        Retrieve detailed information about a specific order.

        Args:
          order_id: Order ID to retrieve details for

          customer_partner_id: Optional customer partner ID for validation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return await self._get(
            f"/v2/orders/{order_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"customer_partner_id": customer_partner_id}, order_retrieve_params.OrderRetrieveParams
                ),
            ),
            cast_to=OrderRetrieveResponse,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        workflow_type: Optional[Literal["DocumentRetrieval", "CompanyReport", "ShareholderGraph", "UBOExtraction"]]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderListResponse:
        """
        Retrieve a list of orders for your organization.

        Args:
          limit: Maximum number of orders to return

          workflow_type: Available workflow types for filtering orders.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v2/orders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "workflow_type": workflow_type,
                    },
                    order_list_params.OrderListParams,
                ),
            ),
            cast_to=OrderListResponse,
        )


class OrdersResourceWithRawResponse:
    def __init__(self, orders: OrdersResource) -> None:
        self._orders = orders

        self.retrieve = to_raw_response_wrapper(
            orders.retrieve,
        )
        self.list = to_raw_response_wrapper(
            orders.list,
        )


class AsyncOrdersResourceWithRawResponse:
    def __init__(self, orders: AsyncOrdersResource) -> None:
        self._orders = orders

        self.retrieve = async_to_raw_response_wrapper(
            orders.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            orders.list,
        )


class OrdersResourceWithStreamingResponse:
    def __init__(self, orders: OrdersResource) -> None:
        self._orders = orders

        self.retrieve = to_streamed_response_wrapper(
            orders.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            orders.list,
        )


class AsyncOrdersResourceWithStreamingResponse:
    def __init__(self, orders: AsyncOrdersResource) -> None:
        self._orders = orders

        self.retrieve = async_to_streamed_response_wrapper(
            orders.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            orders.list,
        )
