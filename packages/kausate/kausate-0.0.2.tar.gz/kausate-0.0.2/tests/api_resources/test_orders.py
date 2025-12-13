# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from kausate import Kausate, AsyncKausate
from tests.utils import assert_matches_type
from kausate.types import OrderListResponse, OrderRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOrders:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Kausate) -> None:
        order = client.orders.retrieve(
            order_id="orderId",
        )
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Kausate) -> None:
        order = client.orders.retrieve(
            order_id="orderId",
            customer_partner_id="customerPartnerId",
        )
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Kausate) -> None:
        response = client.orders.with_raw_response.retrieve(
            order_id="orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Kausate) -> None:
        with client.orders.with_streaming_response.retrieve(
            order_id="orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderRetrieveResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Kausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.orders.with_raw_response.retrieve(
                order_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Kausate) -> None:
        order = client.orders.list()
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Kausate) -> None:
        order = client.orders.list(
            limit=1,
            workflow_type="DocumentRetrieval",
        )
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Kausate) -> None:
        response = client.orders.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Kausate) -> None:
        with client.orders.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderListResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOrders:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncKausate) -> None:
        order = await async_client.orders.retrieve(
            order_id="orderId",
        )
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncKausate) -> None:
        order = await async_client.orders.retrieve(
            order_id="orderId",
            customer_partner_id="customerPartnerId",
        )
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncKausate) -> None:
        response = await async_client.orders.with_raw_response.retrieve(
            order_id="orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncKausate) -> None:
        async with async_client.orders.with_streaming_response.retrieve(
            order_id="orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderRetrieveResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncKausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.orders.with_raw_response.retrieve(
                order_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncKausate) -> None:
        order = await async_client.orders.list()
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncKausate) -> None:
        order = await async_client.orders.list(
            limit=1,
            workflow_type="DocumentRetrieval",
        )
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncKausate) -> None:
        response = await async_client.orders.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncKausate) -> None:
        async with async_client.orders.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderListResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True
