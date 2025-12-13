# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Optional, cast

import httpx

from .report import (
    ReportResource,
    AsyncReportResource,
    ReportResourceWithRawResponse,
    AsyncReportResourceWithRawResponse,
    ReportResourceWithStreamingResponse,
    AsyncReportResourceWithStreamingResponse,
)
from .search import (
    SearchResource,
    AsyncSearchResource,
    SearchResourceWithRawResponse,
    AsyncSearchResourceWithRawResponse,
    SearchResourceWithStreamingResponse,
    AsyncSearchResourceWithStreamingResponse,
)
from ...types import company_extract_ubo_params, company_extract_shareholder_graph_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, strip_not_given, async_maybe_transform
from .products import (
    ProductsResource,
    AsyncProductsResource,
    ProductsResourceWithRawResponse,
    AsyncProductsResourceWithRawResponse,
    ProductsResourceWithStreamingResponse,
    AsyncProductsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .documents import (
    DocumentsResource,
    AsyncDocumentsResource,
    DocumentsResourceWithRawResponse,
    AsyncDocumentsResourceWithRawResponse,
    DocumentsResourceWithStreamingResponse,
    AsyncDocumentsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.product_order_response import ProductOrderResponse
from ...types.company_extract_ubo_response import CompanyExtractUboResponse

__all__ = ["CompaniesResource", "AsyncCompaniesResource"]


class CompaniesResource(SyncAPIResource):
    @cached_property
    def search(self) -> SearchResource:
        return SearchResource(self._client)

    @cached_property
    def products(self) -> ProductsResource:
        return ProductsResource(self._client)

    @cached_property
    def report(self) -> ReportResource:
        return ReportResource(self._client)

    @cached_property
    def documents(self) -> DocumentsResource:
        return DocumentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> CompaniesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return CompaniesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompaniesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return CompaniesResourceWithStreamingResponse(self)

    def extract_shareholder_graph(
        self,
        kausate_id: str,
        *,
        customer_reference: Optional[str] | Omit = omit,
        max_depth: int | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProductOrderResponse:
        """
        Extract multi-level shareholder graph showing shareholders and their
        shareholders.

        This endpoint builds a complete shareholder graph by recursively extracting
        shareholders at multiple levels.

        **Key Features:**

        - Extracts shareholders up to the specified depth (max 5 levels)
        - Returns a graph of nodes and edges

        **Typical workflow:**

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company
        2. Call this endpoint `POST /v2/companies/{kausateId}/shareholder-graph` with
           depth settings
        3. Poll `GET /v2/orders/{orderId}` for the complete graph result

        **Parameters:**

        - **kausateId**: Root company ID to start extraction from
        - **maxDepth**: Maximum levels to extract (1-5, default: 3)
        - **customerReference**: Optional reference for tracking

        **Returns:** Order ID for tracking the extraction (poll for results)

        **Note:** This is a compute-intensive operation and highly depends on the
        availability of underlying data sources.

        Args:
          kausate_id: Company ID

          max_depth: Maximum depth of ownership levels to extract (1-7)

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not kausate_id:
            raise ValueError(f"Expected a non-empty value for `kausate_id` but received {kausate_id!r}")
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return self._post(
            f"/v2/companies/{kausate_id}/shareholder-graph",
            body=maybe_transform(
                {
                    "customer_reference": customer_reference,
                    "max_depth": max_depth,
                },
                company_extract_shareholder_graph_params.CompanyExtractShareholderGraphParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProductOrderResponse,
        )

    def extract_ubo(
        self,
        kausate_id: str,
        *,
        sync: bool | Omit = omit,
        customer_reference: Optional[str] | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompanyExtractUboResponse:
        """
        Retrieve UBOs from beneficial ownership registers (asynchronous or synchronous
        processing).

        This operation retrieves UBO information from official beneficial ownership
        registers.

        Typical workflow:

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company and get its `kausateId`.
        2. Call this endpoint `POST /v2/companies/{kausateId}/ubo` with the required
           request body.
        3. If sync=false (default): Use the returned `orderId` to poll
           `GET /v2/orders/{orderId}` for the extraction result.
        4. If sync=true: The response will contain the UBO data directly (300s timeout).

        - **kausateId**: Company ID to extract UBOs for
        - **customerReference**: Optional reference for tracking
        - **sync**: Return result synchronously with 300s timeout (default: false)

        Returns order ID for tracking (async) or UBO data (sync).

        Note: This endpoint costs 10 credits per request.

        Args:
          kausate_id: Company ID

          sync: Return result synchronously with 300s timeout

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
            CompanyExtractUboResponse,
            self._post(
                f"/v2/companies/{kausate_id}/ubo",
                body=maybe_transform(
                    {"customer_reference": customer_reference}, company_extract_ubo_params.CompanyExtractUboParams
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform({"sync": sync}, company_extract_ubo_params.CompanyExtractUboParams),
                ),
                cast_to=cast(
                    Any, CompanyExtractUboResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncCompaniesResource(AsyncAPIResource):
    @cached_property
    def search(self) -> AsyncSearchResource:
        return AsyncSearchResource(self._client)

    @cached_property
    def products(self) -> AsyncProductsResource:
        return AsyncProductsResource(self._client)

    @cached_property
    def report(self) -> AsyncReportResource:
        return AsyncReportResource(self._client)

    @cached_property
    def documents(self) -> AsyncDocumentsResource:
        return AsyncDocumentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCompaniesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCompaniesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompaniesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncCompaniesResourceWithStreamingResponse(self)

    async def extract_shareholder_graph(
        self,
        kausate_id: str,
        *,
        customer_reference: Optional[str] | Omit = omit,
        max_depth: int | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProductOrderResponse:
        """
        Extract multi-level shareholder graph showing shareholders and their
        shareholders.

        This endpoint builds a complete shareholder graph by recursively extracting
        shareholders at multiple levels.

        **Key Features:**

        - Extracts shareholders up to the specified depth (max 5 levels)
        - Returns a graph of nodes and edges

        **Typical workflow:**

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company
        2. Call this endpoint `POST /v2/companies/{kausateId}/shareholder-graph` with
           depth settings
        3. Poll `GET /v2/orders/{orderId}` for the complete graph result

        **Parameters:**

        - **kausateId**: Root company ID to start extraction from
        - **maxDepth**: Maximum levels to extract (1-5, default: 3)
        - **customerReference**: Optional reference for tracking

        **Returns:** Order ID for tracking the extraction (poll for results)

        **Note:** This is a compute-intensive operation and highly depends on the
        availability of underlying data sources.

        Args:
          kausate_id: Company ID

          max_depth: Maximum depth of ownership levels to extract (1-7)

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not kausate_id:
            raise ValueError(f"Expected a non-empty value for `kausate_id` but received {kausate_id!r}")
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return await self._post(
            f"/v2/companies/{kausate_id}/shareholder-graph",
            body=await async_maybe_transform(
                {
                    "customer_reference": customer_reference,
                    "max_depth": max_depth,
                },
                company_extract_shareholder_graph_params.CompanyExtractShareholderGraphParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProductOrderResponse,
        )

    async def extract_ubo(
        self,
        kausate_id: str,
        *,
        sync: bool | Omit = omit,
        customer_reference: Optional[str] | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompanyExtractUboResponse:
        """
        Retrieve UBOs from beneficial ownership registers (asynchronous or synchronous
        processing).

        This operation retrieves UBO information from official beneficial ownership
        registers.

        Typical workflow:

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company and get its `kausateId`.
        2. Call this endpoint `POST /v2/companies/{kausateId}/ubo` with the required
           request body.
        3. If sync=false (default): Use the returned `orderId` to poll
           `GET /v2/orders/{orderId}` for the extraction result.
        4. If sync=true: The response will contain the UBO data directly (300s timeout).

        - **kausateId**: Company ID to extract UBOs for
        - **customerReference**: Optional reference for tracking
        - **sync**: Return result synchronously with 300s timeout (default: false)

        Returns order ID for tracking (async) or UBO data (sync).

        Note: This endpoint costs 10 credits per request.

        Args:
          kausate_id: Company ID

          sync: Return result synchronously with 300s timeout

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
            CompanyExtractUboResponse,
            await self._post(
                f"/v2/companies/{kausate_id}/ubo",
                body=await async_maybe_transform(
                    {"customer_reference": customer_reference}, company_extract_ubo_params.CompanyExtractUboParams
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {"sync": sync}, company_extract_ubo_params.CompanyExtractUboParams
                    ),
                ),
                cast_to=cast(
                    Any, CompanyExtractUboResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class CompaniesResourceWithRawResponse:
    def __init__(self, companies: CompaniesResource) -> None:
        self._companies = companies

        self.extract_shareholder_graph = to_raw_response_wrapper(
            companies.extract_shareholder_graph,
        )
        self.extract_ubo = to_raw_response_wrapper(
            companies.extract_ubo,
        )

    @cached_property
    def search(self) -> SearchResourceWithRawResponse:
        return SearchResourceWithRawResponse(self._companies.search)

    @cached_property
    def products(self) -> ProductsResourceWithRawResponse:
        return ProductsResourceWithRawResponse(self._companies.products)

    @cached_property
    def report(self) -> ReportResourceWithRawResponse:
        return ReportResourceWithRawResponse(self._companies.report)

    @cached_property
    def documents(self) -> DocumentsResourceWithRawResponse:
        return DocumentsResourceWithRawResponse(self._companies.documents)


class AsyncCompaniesResourceWithRawResponse:
    def __init__(self, companies: AsyncCompaniesResource) -> None:
        self._companies = companies

        self.extract_shareholder_graph = async_to_raw_response_wrapper(
            companies.extract_shareholder_graph,
        )
        self.extract_ubo = async_to_raw_response_wrapper(
            companies.extract_ubo,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithRawResponse:
        return AsyncSearchResourceWithRawResponse(self._companies.search)

    @cached_property
    def products(self) -> AsyncProductsResourceWithRawResponse:
        return AsyncProductsResourceWithRawResponse(self._companies.products)

    @cached_property
    def report(self) -> AsyncReportResourceWithRawResponse:
        return AsyncReportResourceWithRawResponse(self._companies.report)

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithRawResponse:
        return AsyncDocumentsResourceWithRawResponse(self._companies.documents)


class CompaniesResourceWithStreamingResponse:
    def __init__(self, companies: CompaniesResource) -> None:
        self._companies = companies

        self.extract_shareholder_graph = to_streamed_response_wrapper(
            companies.extract_shareholder_graph,
        )
        self.extract_ubo = to_streamed_response_wrapper(
            companies.extract_ubo,
        )

    @cached_property
    def search(self) -> SearchResourceWithStreamingResponse:
        return SearchResourceWithStreamingResponse(self._companies.search)

    @cached_property
    def products(self) -> ProductsResourceWithStreamingResponse:
        return ProductsResourceWithStreamingResponse(self._companies.products)

    @cached_property
    def report(self) -> ReportResourceWithStreamingResponse:
        return ReportResourceWithStreamingResponse(self._companies.report)

    @cached_property
    def documents(self) -> DocumentsResourceWithStreamingResponse:
        return DocumentsResourceWithStreamingResponse(self._companies.documents)


class AsyncCompaniesResourceWithStreamingResponse:
    def __init__(self, companies: AsyncCompaniesResource) -> None:
        self._companies = companies

        self.extract_shareholder_graph = async_to_streamed_response_wrapper(
            companies.extract_shareholder_graph,
        )
        self.extract_ubo = async_to_streamed_response_wrapper(
            companies.extract_ubo,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithStreamingResponse:
        return AsyncSearchResourceWithStreamingResponse(self._companies.search)

    @cached_property
    def products(self) -> AsyncProductsResourceWithStreamingResponse:
        return AsyncProductsResourceWithStreamingResponse(self._companies.products)

    @cached_property
    def report(self) -> AsyncReportResourceWithStreamingResponse:
        return AsyncReportResourceWithStreamingResponse(self._companies.report)

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithStreamingResponse:
        return AsyncDocumentsResourceWithStreamingResponse(self._companies.documents)
