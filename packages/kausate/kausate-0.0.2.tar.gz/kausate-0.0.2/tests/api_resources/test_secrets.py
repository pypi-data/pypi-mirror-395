# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from kausate import Kausate, AsyncKausate
from tests.utils import assert_matches_type
from kausate.types import (
    SecretListResponse,
    SecretResponsePublic,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSecrets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Kausate) -> None:
        secret = client.secrets.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Kausate) -> None:
        secret = client.secrets.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Kausate) -> None:
        response = client.secrets.with_raw_response.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Kausate) -> None:
        with client.secrets.with_streaming_response.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(SecretResponsePublic, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: Kausate) -> None:
        secret = client.secrets.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Kausate) -> None:
        secret = client.secrets.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Kausate) -> None:
        response = client.secrets.with_raw_response.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Kausate) -> None:
        with client.secrets.with_streaming_response.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(SecretResponsePublic, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Kausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_slug` but received ''"):
            client.secrets.with_raw_response.update(
                datasource_slug="",
                secret_values={"foo": "string"},
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Kausate) -> None:
        secret = client.secrets.list()
        assert_matches_type(SecretListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Kausate) -> None:
        secret = client.secrets.list(
            datasource_slug="datasourceSlug",
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(SecretListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Kausate) -> None:
        response = client.secrets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(SecretListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Kausate) -> None:
        with client.secrets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(SecretListResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Kausate) -> None:
        secret = client.secrets.delete(
            datasource_slug="datasourceSlug",
        )
        assert_matches_type(object, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_with_all_params(self, client: Kausate) -> None:
        secret = client.secrets.delete(
            datasource_slug="datasourceSlug",
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(object, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Kausate) -> None:
        response = client.secrets.with_raw_response.delete(
            datasource_slug="datasourceSlug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(object, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Kausate) -> None:
        with client.secrets.with_streaming_response.delete(
            datasource_slug="datasourceSlug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(object, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Kausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_slug` but received ''"):
            client.secrets.with_raw_response.delete(
                datasource_slug="",
            )


class TestAsyncSecrets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncKausate) -> None:
        response = await async_client.secrets.with_raw_response.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncKausate) -> None:
        async with async_client.secrets.with_streaming_response.create(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(SecretResponsePublic, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncKausate) -> None:
        response = await async_client.secrets.with_raw_response.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(SecretResponsePublic, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncKausate) -> None:
        async with async_client.secrets.with_streaming_response.update(
            datasource_slug="datasourceSlug",
            secret_values={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(SecretResponsePublic, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncKausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_slug` but received ''"):
            await async_client.secrets.with_raw_response.update(
                datasource_slug="",
                secret_values={"foo": "string"},
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.list()
        assert_matches_type(SecretListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.list(
            datasource_slug="datasourceSlug",
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(SecretListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncKausate) -> None:
        response = await async_client.secrets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(SecretListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncKausate) -> None:
        async with async_client.secrets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(SecretListResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.delete(
            datasource_slug="datasourceSlug",
        )
        assert_matches_type(object, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncKausate) -> None:
        secret = await async_client.secrets.delete(
            datasource_slug="datasourceSlug",
            partner_customer_id="partnerCustomerId",
        )
        assert_matches_type(object, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncKausate) -> None:
        response = await async_client.secrets.with_raw_response.delete(
            datasource_slug="datasourceSlug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(object, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncKausate) -> None:
        async with async_client.secrets.with_streaming_response.delete(
            datasource_slug="datasourceSlug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(object, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncKausate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_slug` but received ''"):
            await async_client.secrets.with_raw_response.delete(
                datasource_slug="",
            )
