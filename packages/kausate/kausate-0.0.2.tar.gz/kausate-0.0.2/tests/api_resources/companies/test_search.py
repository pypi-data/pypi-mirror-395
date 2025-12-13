# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from kausate import Kausate, AsyncKausate
from tests.utils import assert_matches_type
from kausate.types.companies import (
    SearchIndexResponse,
    SearchRealTimeResponse,
    SearchAutocompleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_autocomplete(self, client: Kausate) -> None:
        search = client.companies.search.autocomplete(
            query="xx",
        )
        assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_autocomplete_with_all_params(self, client: Kausate) -> None:
        search = client.companies.search.autocomplete(
            query="xx",
            jurisdiction_code="jurisdictionCode",
            limit=1,
        )
        assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_autocomplete(self, client: Kausate) -> None:
        response = client.companies.search.with_raw_response.autocomplete(
            query="xx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_autocomplete(self, client: Kausate) -> None:
        with client.companies.search.with_streaming_response.autocomplete(
            query="xx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_index(self, client: Kausate) -> None:
        search = client.companies.search.index()
        assert_matches_type(SearchIndexResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_index_with_all_params(self, client: Kausate) -> None:
        search = client.companies.search.index(
            advanced_query={
                "court_city": "München",
                "court_id": "D2803",
                "jurisdiction": "de",
                "name": "BMW AG",
                "register_number": "10364B",
                "register_suffix": "B",
                "register_type": "HRB",
            },
            include_alternative_names=True,
            include_similar_names=True,
            jurisdiction_code="jurisdictionCode",
            limit=1,
            name="x",
            page=0,
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(SearchIndexResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_index(self, client: Kausate) -> None:
        response = client.companies.search.with_raw_response.index()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchIndexResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_index(self, client: Kausate) -> None:
        with client.companies.search.with_streaming_response.index() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchIndexResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_real_time(self, client: Kausate) -> None:
        search = client.companies.search.real_time()
        assert_matches_type(SearchRealTimeResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_real_time_with_all_params(self, client: Kausate) -> None:
        search = client.companies.search.real_time(
            sync=True,
            advanced_query={
                "court_city": "München",
                "court_id": "D2803",
                "jurisdiction": "de",
                "name": "BMW AG",
                "register_number": "10364B",
                "register_suffix": "B",
                "register_type": "HRB",
            },
            company_name="x",
            customer_reference="customerReference",
            jurisdiction_code="jurisdictionCode",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(SearchRealTimeResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_real_time(self, client: Kausate) -> None:
        response = client.companies.search.with_raw_response.real_time()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchRealTimeResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_real_time(self, client: Kausate) -> None:
        with client.companies.search.with_streaming_response.real_time() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchRealTimeResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_autocomplete(self, async_client: AsyncKausate) -> None:
        search = await async_client.companies.search.autocomplete(
            query="xx",
        )
        assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_autocomplete_with_all_params(self, async_client: AsyncKausate) -> None:
        search = await async_client.companies.search.autocomplete(
            query="xx",
            jurisdiction_code="jurisdictionCode",
            limit=1,
        )
        assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_autocomplete(self, async_client: AsyncKausate) -> None:
        response = await async_client.companies.search.with_raw_response.autocomplete(
            query="xx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_autocomplete(self, async_client: AsyncKausate) -> None:
        async with async_client.companies.search.with_streaming_response.autocomplete(
            query="xx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchAutocompleteResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_index(self, async_client: AsyncKausate) -> None:
        search = await async_client.companies.search.index()
        assert_matches_type(SearchIndexResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_index_with_all_params(self, async_client: AsyncKausate) -> None:
        search = await async_client.companies.search.index(
            advanced_query={
                "court_city": "München",
                "court_id": "D2803",
                "jurisdiction": "de",
                "name": "BMW AG",
                "register_number": "10364B",
                "register_suffix": "B",
                "register_type": "HRB",
            },
            include_alternative_names=True,
            include_similar_names=True,
            jurisdiction_code="jurisdictionCode",
            limit=1,
            name="x",
            page=0,
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(SearchIndexResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_index(self, async_client: AsyncKausate) -> None:
        response = await async_client.companies.search.with_raw_response.index()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchIndexResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_index(self, async_client: AsyncKausate) -> None:
        async with async_client.companies.search.with_streaming_response.index() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchIndexResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_real_time(self, async_client: AsyncKausate) -> None:
        search = await async_client.companies.search.real_time()
        assert_matches_type(SearchRealTimeResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_real_time_with_all_params(self, async_client: AsyncKausate) -> None:
        search = await async_client.companies.search.real_time(
            sync=True,
            advanced_query={
                "court_city": "München",
                "court_id": "D2803",
                "jurisdiction": "de",
                "name": "BMW AG",
                "register_number": "10364B",
                "register_suffix": "B",
                "register_type": "HRB",
            },
            company_name="x",
            customer_reference="customerReference",
            jurisdiction_code="jurisdictionCode",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(SearchRealTimeResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_real_time(self, async_client: AsyncKausate) -> None:
        response = await async_client.companies.search.with_raw_response.real_time()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchRealTimeResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_real_time(self, async_client: AsyncKausate) -> None:
        async with async_client.companies.search.with_streaming_response.real_time() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchRealTimeResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True
