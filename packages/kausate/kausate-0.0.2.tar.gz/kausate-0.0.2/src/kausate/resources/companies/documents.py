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
from ...types.companies import document_list_params
from ...types.companies.document_list_response import DocumentListResponse

__all__ = ["DocumentsResource", "AsyncDocumentsResource"]


class DocumentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return DocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return DocumentsResourceWithStreamingResponse(self)

    def list(
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
    ) -> DocumentListResponse:
        """
        List all available documents for a company from their business registry.

        **Supported Jurisdictions:**

        - **Germany (DE):** Documents from Unternehmensregister (annual accounts, board
          changes, register announcements, etc.)
        - **Austria (AT):** Documents from Austrian Firmenbuch (Jahresabschluss,
          Lagebericht, Gesellschaftsvertrag, etc.)

        The document list is cached for 24 hours.

        **This endpoint is FREE** - no credits are consumed.

        **Typical workflow:**

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=de` to find
           the company
        2. Call this endpoint to get the list of available documents
        3. Use the returned `kausateDocumentId` with
           `POST /v2/companies/{kausateId}/products/order` (pass `kausateDocumentId` in
           the request body) to download a specific document (costs credits)

        **Parameters:**

        - **kausateId**: Company ID (DE or AT jurisdiction)
        - **customerReference**: Optional reference for tracking
        - **sync**: If True (default), wait for results. If False, return workflow ID
          immediately

        **Returns:**

        - If sync=True: List of available documents with their kausateDocumentIds
        - If sync=False: Workflow information for async tracking

        **Note:** Document IDs are cached for 24 hours. After expiration, you'll need to
        call this endpoint again to get fresh document IDs.

        Args:
          kausate_id: Company ID

          sync: Return result synchronously (default: true)

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
            DocumentListResponse,
            self._post(
                f"/v2/companies/{kausate_id}/documents/list",
                body=maybe_transform(
                    {"customer_reference": customer_reference}, document_list_params.DocumentListParams
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform({"sync": sync}, document_list_params.DocumentListParams),
                ),
                cast_to=cast(
                    Any, DocumentListResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncDocumentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncDocumentsResourceWithStreamingResponse(self)

    async def list(
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
    ) -> DocumentListResponse:
        """
        List all available documents for a company from their business registry.

        **Supported Jurisdictions:**

        - **Germany (DE):** Documents from Unternehmensregister (annual accounts, board
          changes, register announcements, etc.)
        - **Austria (AT):** Documents from Austrian Firmenbuch (Jahresabschluss,
          Lagebericht, Gesellschaftsvertrag, etc.)

        The document list is cached for 24 hours.

        **This endpoint is FREE** - no credits are consumed.

        **Typical workflow:**

        1. Use `GET /v2/companies/search/indexed?name=...&jurisdictionCode=de` to find
           the company
        2. Call this endpoint to get the list of available documents
        3. Use the returned `kausateDocumentId` with
           `POST /v2/companies/{kausateId}/products/order` (pass `kausateDocumentId` in
           the request body) to download a specific document (costs credits)

        **Parameters:**

        - **kausateId**: Company ID (DE or AT jurisdiction)
        - **customerReference**: Optional reference for tracking
        - **sync**: If True (default), wait for results. If False, return workflow ID
          immediately

        **Returns:**

        - If sync=True: List of available documents with their kausateDocumentIds
        - If sync=False: Workflow information for async tracking

        **Note:** Document IDs are cached for 24 hours. After expiration, you'll need to
        call this endpoint again to get fresh document IDs.

        Args:
          kausate_id: Company ID

          sync: Return result synchronously (default: true)

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
            DocumentListResponse,
            await self._post(
                f"/v2/companies/{kausate_id}/documents/list",
                body=await async_maybe_transform(
                    {"customer_reference": customer_reference}, document_list_params.DocumentListParams
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform({"sync": sync}, document_list_params.DocumentListParams),
                ),
                cast_to=cast(
                    Any, DocumentListResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class DocumentsResourceWithRawResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.list = to_raw_response_wrapper(
            documents.list,
        )


class AsyncDocumentsResourceWithRawResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.list = async_to_raw_response_wrapper(
            documents.list,
        )


class DocumentsResourceWithStreamingResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.list = to_streamed_response_wrapper(
            documents.list,
        )


class AsyncDocumentsResourceWithStreamingResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.list = async_to_streamed_response_wrapper(
            documents.list,
        )
