# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Optional, cast

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
from ...types.companies import report_create_params
from ...types.companies.report_create_response import ReportCreateResponse

__all__ = ["ReportResource", "AsyncReportResource"]


class ReportResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ReportResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return ReportResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReportResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return ReportResourceWithStreamingResponse(self)

    def create(
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
    ) -> ReportCreateResponse:
        """
        Order a company report for a company (asynchronous or synchronous processing).

        Typical workflow:

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company and get its `kausateId`.
        2. Call this endpoint `POST /v2/companies/{kausateId}/report` with the required
           parameters.
        3. If sync=false (default): Use the returned `orderId` to poll
           `GET /v2/orders/{orderId}` for the result.
        4. If sync=true: The response will contain the complete company report directly
           (300s timeout).

        - **kausateId**: Company ID to order report for
        - **customerReference**: Optional reference for tracking
        - **sync**: Return result synchronously with 300s timeout (default: false)

        Returns order ID for tracking (async) or complete company report (sync).

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
            ReportCreateResponse,
            self._post(
                f"/v2/companies/{kausate_id}/report",
                body=maybe_transform(
                    {"customer_reference": customer_reference}, report_create_params.ReportCreateParams
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform({"sync": sync}, report_create_params.ReportCreateParams),
                ),
                cast_to=cast(
                    Any, ReportCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncReportResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncReportResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncReportResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReportResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncReportResourceWithStreamingResponse(self)

    async def create(
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
    ) -> ReportCreateResponse:
        """
        Order a company report for a company (asynchronous or synchronous processing).

        Typical workflow:

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=...` to find
           the company and get its `kausateId`.
        2. Call this endpoint `POST /v2/companies/{kausateId}/report` with the required
           parameters.
        3. If sync=false (default): Use the returned `orderId` to poll
           `GET /v2/orders/{orderId}` for the result.
        4. If sync=true: The response will contain the complete company report directly
           (300s timeout).

        - **kausateId**: Company ID to order report for
        - **customerReference**: Optional reference for tracking
        - **sync**: Return result synchronously with 300s timeout (default: false)

        Returns order ID for tracking (async) or complete company report (sync).

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
            ReportCreateResponse,
            await self._post(
                f"/v2/companies/{kausate_id}/report",
                body=await async_maybe_transform(
                    {"customer_reference": customer_reference}, report_create_params.ReportCreateParams
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform({"sync": sync}, report_create_params.ReportCreateParams),
                ),
                cast_to=cast(
                    Any, ReportCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class ReportResourceWithRawResponse:
    def __init__(self, report: ReportResource) -> None:
        self._report = report

        self.create = to_raw_response_wrapper(
            report.create,
        )


class AsyncReportResourceWithRawResponse:
    def __init__(self, report: AsyncReportResource) -> None:
        self._report = report

        self.create = async_to_raw_response_wrapper(
            report.create,
        )


class ReportResourceWithStreamingResponse:
    def __init__(self, report: ReportResource) -> None:
        self._report = report

        self.create = to_streamed_response_wrapper(
            report.create,
        )


class AsyncReportResourceWithStreamingResponse:
    def __init__(self, report: AsyncReportResource) -> None:
        self._report = report

        self.create = async_to_streamed_response_wrapper(
            report.create,
        )
