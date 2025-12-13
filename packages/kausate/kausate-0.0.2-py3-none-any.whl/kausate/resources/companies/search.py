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
from ...types.companies import search_index_params, search_real_time_params, search_autocomplete_params
from ...types.companies.search_index_response import SearchIndexResponse
from ...types.companies.search_real_time_response import SearchRealTimeResponse
from ...types.companies.search_autocomplete_response import SearchAutocompleteResponse

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return SearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return SearchResourceWithStreamingResponse(self)

    def autocomplete(
        self,
        *,
        query: str,
        jurisdiction_code: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchAutocompleteResponse:
        """
        Get autocomplete suggestions for company names as users type.

        This endpoint provides fast, type-ahead suggestions to help users find companies
        quickly. It's optimized for speed and returns matches based on company names and
        alternative names.

        **Features:**

        - Fast "starts with" matching for responsive UX
        - Searches both primary names and alternative names
        - No credit cost - free to use for better user experience
        - Returns up to 50 results (default: 10)

        **Typical usage:** Use this endpoint to provide autocomplete suggestions in a
        search input field. Once the user selects a company, use the returned
        `kausateId` to:

        - Get full company details
        - Order documents or reports
        - Extract shareholders

        **Parameters:**

        - **jurisdictionCode**: ISO country code (optional, e.g., 'de', 'uk')
        - **query**: Search query (minimum 2 characters)
        - **limit**: Number of results (default: 10, max: 50)

        **Returns:** List of matching companies with kausateId, name, and jurisdiction.

        **Note:** This endpoint does not consume credits.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v2/companies/search/autocomplete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "query": query,
                        "jurisdiction_code": jurisdiction_code,
                        "limit": limit,
                    },
                    search_autocomplete_params.SearchAutocompleteParams,
                ),
            ),
            cast_to=SearchAutocompleteResponse,
        )

    def index(
        self,
        *,
        advanced_query: Optional[search_index_params.AdvancedQuery] | Omit = omit,
        include_alternative_names: bool | Omit = omit,
        include_similar_names: bool | Omit = omit,
        jurisdiction_code: str | Omit = omit,
        limit: Optional[int] | Omit = omit,
        name: Optional[str] | Omit = omit,
        page: Optional[int] | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchIndexResponse:
        """
        Search companies to find the correct company before performing other actions
        (POST method).

        **Note:** This endpoint is free to use - no credit cost.

        **Search Methods:**

        1. **By Name**: Provide `name` field with company name to search
        2. **By Local Identifiers** (Advanced): Provide `advancedQuery` with identifier
           components:
           - **German (DE)**: `courtCity`, `courtId`, `registerType`, `registerNumber`,
             `registerSuffix`
           - **UK**: `companyNumber`

        **Typical workflow:**

        1. Use this endpoint to search for a company by name/identifiers and
           jurisdiction
        2. Select the correct company from the results (using the returned kausateId)
        3. Use the kausateId to:
           - Get company documents
           - Get a company report
           - Extract shareholders

        **Parameters (JSON body):**

        - **jurisdictionCode**: ISO country code (default: "de")
        - **name**: Company name to search (required if advancedQuery not provided)
        - **advancedQuery**: Local identifier components (required if name not provided)
          - For Germany: `courtCity` (e.g., "München"), `courtId` (e.g., "D2803"),
            `registerType` (e.g., "HRB"), `registerNumber` (e.g., "10364B"),
            `registerSuffix` (e.g., "B")
          - For UK: `companyNumber` (e.g., "09410276")
        - **limit**: Max results to return (default: 10, max: 1000)
        - **page**: Page number for pagination (default: 0, 0-based)

        Returns a paginated list of companies, ranked by relevance, with pagination
        metadata.

        Args:
          advanced_query: Jurisdiction-specific advanced search query. The structure varies based on the
              'jurisdiction' field.

          include_alternative_names: If true, searches alternative company names (more expensive). Default: false for
              optimal performance.

          include_similar_names: If true, falls back to trigram similarity search when no exact matches found
              (more expensive). Default: false for optimal performance.

          jurisdiction_code: ISO 3166-1 alpha-2 country code (e.g., 'de' for Germany, 'uk' for United
              Kingdom)

          name: Company name to search for. Either 'name' or 'advancedQuery' must be provided.

          page: Page number (0-based)

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return self._post(
            "/v2/companies/search/indexed",
            body=maybe_transform(
                {
                    "advanced_query": advanced_query,
                    "include_alternative_names": include_alternative_names,
                    "include_similar_names": include_similar_names,
                    "jurisdiction_code": jurisdiction_code,
                    "limit": limit,
                    "name": name,
                    "page": page,
                },
                search_index_params.SearchIndexParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchIndexResponse,
        )

    def real_time(
        self,
        *,
        sync: bool | Omit = omit,
        advanced_query: Optional[search_real_time_params.AdvancedQuery] | Omit = omit,
        company_name: Optional[str] | Omit = omit,
        customer_reference: Optional[str] | Omit = omit,
        jurisdiction_code: str | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchRealTimeResponse:
        """Search for companies in real-time.

        Returns results with generated Kausate IDs.

        Args:
          sync: If True, wait for results. If False, return workflow ID immediately

          advanced_query: Jurisdiction-specific advanced search query. The structure varies based on the
              'jurisdiction' field.

          company_name: Company name to search for. Either 'companyName' or 'advancedQuery' must be
              provided.

          customer_reference: Optional customer reference for tracking

          jurisdiction_code: ISO 3166-1 alpha-2 country code (e.g., 'de' for Germany, 'uk' for United
              Kingdom)

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return cast(
            SearchRealTimeResponse,
            self._post(
                "/v2/companies/search/live",
                body=maybe_transform(
                    {
                        "advanced_query": advanced_query,
                        "company_name": company_name,
                        "customer_reference": customer_reference,
                        "jurisdiction_code": jurisdiction_code,
                    },
                    search_real_time_params.SearchRealTimeParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform({"sync": sync}, search_real_time_params.SearchRealTimeParams),
                ),
                cast_to=cast(
                    Any, SearchRealTimeResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncSearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/kausate/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/kausate/sdk-python#with_streaming_response
        """
        return AsyncSearchResourceWithStreamingResponse(self)

    async def autocomplete(
        self,
        *,
        query: str,
        jurisdiction_code: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchAutocompleteResponse:
        """
        Get autocomplete suggestions for company names as users type.

        This endpoint provides fast, type-ahead suggestions to help users find companies
        quickly. It's optimized for speed and returns matches based on company names and
        alternative names.

        **Features:**

        - Fast "starts with" matching for responsive UX
        - Searches both primary names and alternative names
        - No credit cost - free to use for better user experience
        - Returns up to 50 results (default: 10)

        **Typical usage:** Use this endpoint to provide autocomplete suggestions in a
        search input field. Once the user selects a company, use the returned
        `kausateId` to:

        - Get full company details
        - Order documents or reports
        - Extract shareholders

        **Parameters:**

        - **jurisdictionCode**: ISO country code (optional, e.g., 'de', 'uk')
        - **query**: Search query (minimum 2 characters)
        - **limit**: Number of results (default: 10, max: 50)

        **Returns:** List of matching companies with kausateId, name, and jurisdiction.

        **Note:** This endpoint does not consume credits.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v2/companies/search/autocomplete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "query": query,
                        "jurisdiction_code": jurisdiction_code,
                        "limit": limit,
                    },
                    search_autocomplete_params.SearchAutocompleteParams,
                ),
            ),
            cast_to=SearchAutocompleteResponse,
        )

    async def index(
        self,
        *,
        advanced_query: Optional[search_index_params.AdvancedQuery] | Omit = omit,
        include_alternative_names: bool | Omit = omit,
        include_similar_names: bool | Omit = omit,
        jurisdiction_code: str | Omit = omit,
        limit: Optional[int] | Omit = omit,
        name: Optional[str] | Omit = omit,
        page: Optional[int] | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchIndexResponse:
        """
        Search companies to find the correct company before performing other actions
        (POST method).

        **Note:** This endpoint is free to use - no credit cost.

        **Search Methods:**

        1. **By Name**: Provide `name` field with company name to search
        2. **By Local Identifiers** (Advanced): Provide `advancedQuery` with identifier
           components:
           - **German (DE)**: `courtCity`, `courtId`, `registerType`, `registerNumber`,
             `registerSuffix`
           - **UK**: `companyNumber`

        **Typical workflow:**

        1. Use this endpoint to search for a company by name/identifiers and
           jurisdiction
        2. Select the correct company from the results (using the returned kausateId)
        3. Use the kausateId to:
           - Get company documents
           - Get a company report
           - Extract shareholders

        **Parameters (JSON body):**

        - **jurisdictionCode**: ISO country code (default: "de")
        - **name**: Company name to search (required if advancedQuery not provided)
        - **advancedQuery**: Local identifier components (required if name not provided)
          - For Germany: `courtCity` (e.g., "München"), `courtId` (e.g., "D2803"),
            `registerType` (e.g., "HRB"), `registerNumber` (e.g., "10364B"),
            `registerSuffix` (e.g., "B")
          - For UK: `companyNumber` (e.g., "09410276")
        - **limit**: Max results to return (default: 10, max: 1000)
        - **page**: Page number for pagination (default: 0, 0-based)

        Returns a paginated list of companies, ranked by relevance, with pagination
        metadata.

        Args:
          advanced_query: Jurisdiction-specific advanced search query. The structure varies based on the
              'jurisdiction' field.

          include_alternative_names: If true, searches alternative company names (more expensive). Default: false for
              optimal performance.

          include_similar_names: If true, falls back to trigram similarity search when no exact matches found
              (more expensive). Default: false for optimal performance.

          jurisdiction_code: ISO 3166-1 alpha-2 country code (e.g., 'de' for Germany, 'uk' for United
              Kingdom)

          name: Company name to search for. Either 'name' or 'advancedQuery' must be provided.

          page: Page number (0-based)

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return await self._post(
            "/v2/companies/search/indexed",
            body=await async_maybe_transform(
                {
                    "advanced_query": advanced_query,
                    "include_alternative_names": include_alternative_names,
                    "include_similar_names": include_similar_names,
                    "jurisdiction_code": jurisdiction_code,
                    "limit": limit,
                    "name": name,
                    "page": page,
                },
                search_index_params.SearchIndexParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchIndexResponse,
        )

    async def real_time(
        self,
        *,
        sync: bool | Omit = omit,
        advanced_query: Optional[search_real_time_params.AdvancedQuery] | Omit = omit,
        company_name: Optional[str] | Omit = omit,
        customer_reference: Optional[str] | Omit = omit,
        jurisdiction_code: str | Omit = omit,
        x_partner_customer_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchRealTimeResponse:
        """Search for companies in real-time.

        Returns results with generated Kausate IDs.

        Args:
          sync: If True, wait for results. If False, return workflow ID immediately

          advanced_query: Jurisdiction-specific advanced search query. The structure varies based on the
              'jurisdiction' field.

          company_name: Company name to search for. Either 'companyName' or 'advancedQuery' must be
              provided.

          customer_reference: Optional customer reference for tracking

          jurisdiction_code: ISO 3166-1 alpha-2 country code (e.g., 'de' for Germany, 'uk' for United
              Kingdom)

          x_partner_customer_id: Optional partner customer ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"X-Partner-Customer-Id": x_partner_customer_id}), **(extra_headers or {})}
        return cast(
            SearchRealTimeResponse,
            await self._post(
                "/v2/companies/search/live",
                body=await async_maybe_transform(
                    {
                        "advanced_query": advanced_query,
                        "company_name": company_name,
                        "customer_reference": customer_reference,
                        "jurisdiction_code": jurisdiction_code,
                    },
                    search_real_time_params.SearchRealTimeParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform({"sync": sync}, search_real_time_params.SearchRealTimeParams),
                ),
                cast_to=cast(
                    Any, SearchRealTimeResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.autocomplete = to_raw_response_wrapper(
            search.autocomplete,
        )
        self.index = to_raw_response_wrapper(
            search.index,
        )
        self.real_time = to_raw_response_wrapper(
            search.real_time,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.autocomplete = async_to_raw_response_wrapper(
            search.autocomplete,
        )
        self.index = async_to_raw_response_wrapper(
            search.index,
        )
        self.real_time = async_to_raw_response_wrapper(
            search.real_time,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.autocomplete = to_streamed_response_wrapper(
            search.autocomplete,
        )
        self.index = to_streamed_response_wrapper(
            search.index,
        )
        self.real_time = to_streamed_response_wrapper(
            search.real_time,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.autocomplete = async_to_streamed_response_wrapper(
            search.autocomplete,
        )
        self.index = async_to_streamed_response_wrapper(
            search.index,
        )
        self.real_time = async_to_streamed_response_wrapper(
            search.real_time,
        )
