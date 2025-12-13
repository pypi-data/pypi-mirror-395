# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Optional, cast
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, strip_not_given, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.companies import product_order_params
from ...types.companies.product_order_response import ProductOrderResponse

__all__ = ["ProductsResource", "AsyncProductsResource"]


class ProductsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProductsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return ProductsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProductsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return ProductsResourceWithStreamingResponse(self)

    def order(
        self,
        kausate_id: str,
        *,
        sync: bool | Omit = omit,
        customer_reference: Optional[str] | Omit = omit,
        kausate_document_id: Optional[str] | Omit = omit,
        output_format: Literal["pdf", "raw"] | Omit = omit,
        sku: Optional[str] | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProductOrderResponse:
        """Order a real-time product (e.g.

        company document) for a company (asynchronous or
        synchronous processing).

        Typical workflow:

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company and get its `kausateId`.
        2. Call this endpoint `POST /v2/companies/{kausateId}/products/order` with the
           document type.
        3. If sync=false (default): Use the returned `orderId` to poll
           `GET /v2/orders/{orderId}` for the result.
        4. If sync=true: The response will contain the document data directly (300s
           timeout).

        Examples of currently supported SKUs for Germany (DE):

        - `DEHRAD` (Current Register Information)
        - `DEHRSL` (Shareholders List)
        - `DEHRCD` (Chronological Register Information)
        - `DEHRAA` (Articles of Association)
        - `DEHRSI` (Structured Information)
        - `DEHRMP` (Model Protocol)

        - **kausateId**: Company ID to order product for
        - **sku**: Product SKU code
        - **customerReference**: Optional reference for tracking
        - **sync**: Return result synchronously with 300s timeout (default: false)

        Returns order ID for tracking (async) or document data (sync).

        Args:
          kausate_id: Company ID

          sync: Return result synchronously with 300s timeout

          kausate_document_id: Document ID from /documents/list response (e.g., doc_deur_abc123). Required if
              sku not provided.

          output_format: Output format. 'pdf' converts TIFF files to PDF (default). 'raw' keeps original
              format.

          sku: Product SKU code (e.g., DEHRAD, DEHRSI). Required if kausateDocumentId not
              provided.

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not kausate_id:
            raise ValueError(f"Expected a non-empty value for `kausate_id` but received {kausate_id!r}")
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return cast(
            ProductOrderResponse,
            self._post(
                f"/v2/companies/{kausate_id}/products/order",
                body=maybe_transform(
                    {
                        "customer_reference": customer_reference,
                        "kausate_document_id": kausate_document_id,
                        "output_format": output_format,
                        "sku": sku,
                    },
                    product_order_params.ProductOrderParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform({"sync": sync}, product_order_params.ProductOrderParams),
                ),
                cast_to=cast(
                    Any, ProductOrderResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncProductsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProductsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProductsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProductsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncProductsResourceWithStreamingResponse(self)

    async def order(
        self,
        kausate_id: str,
        *,
        sync: bool | Omit = omit,
        customer_reference: Optional[str] | Omit = omit,
        kausate_document_id: Optional[str] | Omit = omit,
        output_format: Literal["pdf", "raw"] | Omit = omit,
        sku: Optional[str] | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProductOrderResponse:
        """Order a real-time product (e.g.

        company document) for a company (asynchronous or
        synchronous processing).

        Typical workflow:

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company and get its `kausateId`.
        2. Call this endpoint `POST /v2/companies/{kausateId}/products/order` with the
           document type.
        3. If sync=false (default): Use the returned `orderId` to poll
           `GET /v2/orders/{orderId}` for the result.
        4. If sync=true: The response will contain the document data directly (300s
           timeout).

        Examples of currently supported SKUs for Germany (DE):

        - `DEHRAD` (Current Register Information)
        - `DEHRSL` (Shareholders List)
        - `DEHRCD` (Chronological Register Information)
        - `DEHRAA` (Articles of Association)
        - `DEHRSI` (Structured Information)
        - `DEHRMP` (Model Protocol)

        - **kausateId**: Company ID to order product for
        - **sku**: Product SKU code
        - **customerReference**: Optional reference for tracking
        - **sync**: Return result synchronously with 300s timeout (default: false)

        Returns order ID for tracking (async) or document data (sync).

        Args:
          kausate_id: Company ID

          sync: Return result synchronously with 300s timeout

          kausate_document_id: Document ID from /documents/list response (e.g., doc_deur_abc123). Required if
              sku not provided.

          output_format: Output format. 'pdf' converts TIFF files to PDF (default). 'raw' keeps original
              format.

          sku: Product SKU code (e.g., DEHRAD, DEHRSI). Required if kausateDocumentId not
              provided.

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not kausate_id:
            raise ValueError(f"Expected a non-empty value for `kausate_id` but received {kausate_id!r}")
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return cast(
            ProductOrderResponse,
            await self._post(
                f"/v2/companies/{kausate_id}/products/order",
                body=await async_maybe_transform(
                    {
                        "customer_reference": customer_reference,
                        "kausate_document_id": kausate_document_id,
                        "output_format": output_format,
                        "sku": sku,
                    },
                    product_order_params.ProductOrderParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform({"sync": sync}, product_order_params.ProductOrderParams),
                ),
                cast_to=cast(
                    Any, ProductOrderResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class ProductsResourceWithRawResponse:
    def __init__(self, products: ProductsResource) -> None:
        self._products = products

        self.order = to_raw_response_wrapper(
            products.order,
        )


class AsyncProductsResourceWithRawResponse:
    def __init__(self, products: AsyncProductsResource) -> None:
        self._products = products

        self.order = async_to_raw_response_wrapper(
            products.order,
        )


class ProductsResourceWithStreamingResponse:
    def __init__(self, products: ProductsResource) -> None:
        self._products = products

        self.order = to_streamed_response_wrapper(
            products.order,
        )


class AsyncProductsResourceWithStreamingResponse:
    def __init__(self, products: AsyncProductsResource) -> None:
        self._products = products

        self.order = async_to_streamed_response_wrapper(
            products.order,
        )
