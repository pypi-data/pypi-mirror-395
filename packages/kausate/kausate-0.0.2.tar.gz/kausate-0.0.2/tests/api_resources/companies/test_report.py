# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from kausate import Kausate, AsyncKausate
from tests.utils import assert_matches_type
from kausate.types.companies import ReportCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReport:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Kausate) -> None:
        report = client.companies.report.create(
            kausate_id="kausateId",
        )
        assert_matches_type(ReportCreateResponse, report, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Kausate) -> None:
        report = client.companies.report.create(
            kausate_id="kausateId",
            sync=True,
            customer_reference="customerReference",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(ReportCreateResponse, report, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Kausate) -> None:
        response = client.companies.report.with_raw_response.create(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        report = response.parse()
        assert_matches_type(ReportCreateResponse, report, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Kausate) -> None:
        with client.companies.report.with_streaming_response.create(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            report = response.parse()
            assert_matches_type(ReportCreateResponse, report, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_create(self, client: Kausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            client.companies.report.with_raw_response.create(
                kausate_id="",
            )


class TestAsyncReport:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncKausate) -> None:
        report = await async_client.companies.report.create(
            kausate_id="kausateId",
        )
        assert_matches_type(ReportCreateResponse, report, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncKausate) -> None:
        report = await async_client.companies.report.create(
            kausate_id="kausateId",
            sync=True,
            customer_reference="customerReference",
            x_partner_customer_id="X-Partner-Customer-Id",
        )
        assert_matches_type(ReportCreateResponse, report, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncKausate) -> None:
        response = await async_client.companies.report.with_raw_response.create(
            kausate_id="kausateId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        report = await response.parse()
        assert_matches_type(ReportCreateResponse, report, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncKausate) -> None:
        async with async_client.companies.report.with_streaming_response.create(
            kausate_id="kausateId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            report = await response.parse()
            assert_matches_type(ReportCreateResponse, report, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_create(self, async_client: AsyncKausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kausate_id` but received ''"):
            await async_client.companies.report.with_raw_response.create(
                kausate_id="",
            )
