# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from kausate import Kausate, AsyncKausate
from tests.utils import assert_matches_type
from kausate.types.companies import ProductOrderResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProducts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_order(self, client: Kausate) -> None:
        product = client.companies.products.order(
            kausate_id="kausateId",
        )
        assert_matches_type(ProductOrderResponse, product, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_order_with_all_params(self, client: Kausate) -> None:
        product = client.companies.products.order(
            kausate_id="kausateId",
            sync=True,
            customer_reference="customerReference",
            kausate_document_id="kausateDocumentId",
            output_format="pdf",
            sku="sku",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(ProductOrderResponse, product, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_order(self, client: Kausate) -> None:
        response = client.companies.products.with_raw_response.order(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        product = response.parse()
        assert_matches_type(ProductOrderResponse, product, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_order(self, client: Kausate) -> None:
        with client.companies.products.with_streaming_response.order(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            product = response.parse()
            assert_matches_type(ProductOrderResponse, product, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_order(self, client: Kausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            client.companies.products.with_raw_response.order(
                kausate_id="",
            )


class TestAsyncProducts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_order(self, async_client: AsyncKausate) -> None:
        product = await async_client.companies.products.order(
            kausate_id="kausateId",
        )
        assert_matches_type(ProductOrderResponse, product, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_order_with_all_params(self, async_client: AsyncKausate) -> None:
        product = await async_client.companies.products.order(
            kausate_id="kausateId",
            sync=True,
            customer_reference="customerReference",
            kausate_document_id="kausateDocumentId",
            output_format="pdf",
            sku="sku",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(ProductOrderResponse, product, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_order(self, async_client: AsyncKausate) -> None:
        response = await async_client.companies.products.with_raw_response.order(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        product = await response.parse()
        assert_matches_type(ProductOrderResponse, product, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_order(self, async_client: AsyncKausate) -> None:
        async with async_client.companies.products.with_streaming_response.order(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            product = await response.parse()
            assert_matches_type(ProductOrderResponse, product, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_order(self, async_client: AsyncKausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            await async_client.companies.products.with_raw_response.order(
                kausate_id="",
            )
