# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from kausate import Kausate, AsyncKausate
from tests.utils import assert_matches_type
from kausate.types import (
    ProductOrderResponse,
    CompanyExtractUboResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompanies:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_extract_shareholder_graph(self, client: Kausate) -> None:
        company = client.companies.extract_shareholder_graph(
            kausate_id="kausateId",
        )
        assert_matches_type(ProductOrderResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_extract_shareholder_graph_with_all_params(self, client: Kausate) -> None:
        company = client.companies.extract_shareholder_graph(
            kausate_id="kausateId",
            customer_reference="customerReference",
            max_depth=1,
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(ProductOrderResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_extract_shareholder_graph(self, client: Kausate) -> None:
        response = client.companies.with_raw_response.extract_shareholder_graph(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company = response.parse()
        assert_matches_type(ProductOrderResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_extract_shareholder_graph(self, client: Kausate) -> None:
        with client.companies.with_streaming_response.extract_shareholder_graph(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company = response.parse()
            assert_matches_type(ProductOrderResponse, company, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_extract_shareholder_graph(self, client: Kausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            client.companies.with_raw_response.extract_shareholder_graph(
                kausate_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_extract_ubo(self, client: Kausate) -> None:
        company = client.companies.extract_ubo(
            kausate_id="kausateId",
        )
        assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_extract_ubo_with_all_params(self, client: Kausate) -> None:
        company = client.companies.extract_ubo(
            kausate_id="kausateId",
            sync=True,
            customer_reference="customerReference",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_extract_ubo(self, client: Kausate) -> None:
        response = client.companies.with_raw_response.extract_ubo(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company = response.parse()
        assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_extract_ubo(self, client: Kausate) -> None:
        with client.companies.with_streaming_response.extract_ubo(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company = response.parse()
            assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_extract_ubo(self, client: Kausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            client.companies.with_raw_response.extract_ubo(
                kausate_id="",
            )


class TestAsyncCompanies:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_extract_shareholder_graph(self, async_client: AsyncKausate) -> None:
        company = await async_client.companies.extract_shareholder_graph(
            kausate_id="kausateId",
        )
        assert_matches_type(ProductOrderResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_extract_shareholder_graph_with_all_params(self, async_client: AsyncKausate) -> None:
        company = await async_client.companies.extract_shareholder_graph(
            kausate_id="kausateId",
            customer_reference="customerReference",
            max_depth=1,
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(ProductOrderResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_extract_shareholder_graph(self, async_client: AsyncKausate) -> None:
        response = await async_client.companies.with_raw_response.extract_shareholder_graph(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company = await response.parse()
        assert_matches_type(ProductOrderResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_extract_shareholder_graph(self, async_client: AsyncKausate) -> None:
        async with async_client.companies.with_streaming_response.extract_shareholder_graph(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company = await response.parse()
            assert_matches_type(ProductOrderResponse, company, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_extract_shareholder_graph(self, async_client: AsyncKausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            await async_client.companies.with_raw_response.extract_shareholder_graph(
                kausate_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_extract_ubo(self, async_client: AsyncKausate) -> None:
        company = await async_client.companies.extract_ubo(
            kausate_id="kausateId",
        )
        assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_extract_ubo_with_all_params(self, async_client: AsyncKausate) -> None:
        company = await async_client.companies.extract_ubo(
            kausate_id="kausateId",
            sync=True,
            customer_reference="customerReference",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_extract_ubo(self, async_client: AsyncKausate) -> None:
        response = await async_client.companies.with_raw_response.extract_ubo(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company = await response.parse()
        assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_extract_ubo(self, async_client: AsyncKausate) -> None:
        async with async_client.companies.with_streaming_response.extract_ubo(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company = await response.parse()
            assert_matches_type(CompanyExtractUboResponse, company, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_extract_ubo(self, async_client: AsyncKausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            await async_client.companies.with_raw_response.extract_ubo(
                kausate_id="",
            )
