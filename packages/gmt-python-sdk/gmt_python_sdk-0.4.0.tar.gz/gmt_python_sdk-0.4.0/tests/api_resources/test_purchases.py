# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gmt import Gmt, AsyncGmt
from gmt.types import (
    PurchaseListResponse,
    PurchaseCreateResponse,
    PurchaseRetrieveResponse,
    PurchaseRequestVerificationCodeResponse,
)
from tests.utils import assert_matches_type
from gmt.pagination import SyncPageNumber, AsyncPageNumber

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPurchases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Gmt) -> None:
        purchase = client.purchases.create(
            country_code="US",
        )
        assert_matches_type(PurchaseCreateResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Gmt) -> None:
        response = client.purchases.with_raw_response.create(
            country_code="US",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = response.parse()
        assert_matches_type(PurchaseCreateResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Gmt) -> None:
        with client.purchases.with_streaming_response.create(
            country_code="US",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = response.parse()
            assert_matches_type(PurchaseCreateResponse, purchase, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Gmt) -> None:
        purchase = client.purchases.retrieve(
            12345,
        )
        assert_matches_type(PurchaseRetrieveResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Gmt) -> None:
        response = client.purchases.with_raw_response.retrieve(
            12345,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = response.parse()
        assert_matches_type(PurchaseRetrieveResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Gmt) -> None:
        with client.purchases.with_streaming_response.retrieve(
            12345,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = response.parse()
            assert_matches_type(PurchaseRetrieveResponse, purchase, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Gmt) -> None:
        purchase = client.purchases.list(
            page=1,
            page_size=50,
        )
        assert_matches_type(SyncPageNumber[PurchaseListResponse], purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Gmt) -> None:
        purchase = client.purchases.list(
            page=1,
            page_size=50,
            status="SUCCESS",
        )
        assert_matches_type(SyncPageNumber[PurchaseListResponse], purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Gmt) -> None:
        response = client.purchases.with_raw_response.list(
            page=1,
            page_size=50,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = response.parse()
        assert_matches_type(SyncPageNumber[PurchaseListResponse], purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Gmt) -> None:
        with client.purchases.with_streaming_response.list(
            page=1,
            page_size=50,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = response.parse()
            assert_matches_type(SyncPageNumber[PurchaseListResponse], purchase, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_request_verification_code(self, client: Gmt) -> None:
        purchase = client.purchases.request_verification_code(
            purchase_id=12345,
        )
        assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_request_verification_code_with_all_params(self, client: Gmt) -> None:
        purchase = client.purchases.request_verification_code(
            purchase_id=12345,
            callback_url="https://example.com/webhooks/code-received",
        )
        assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_request_verification_code(self, client: Gmt) -> None:
        response = client.purchases.with_raw_response.request_verification_code(
            purchase_id=12345,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = response.parse()
        assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_request_verification_code(self, client: Gmt) -> None:
        with client.purchases.with_streaming_response.request_verification_code(
            purchase_id=12345,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = response.parse()
            assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPurchases:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncGmt) -> None:
        purchase = await async_client.purchases.create(
            country_code="US",
        )
        assert_matches_type(PurchaseCreateResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGmt) -> None:
        response = await async_client.purchases.with_raw_response.create(
            country_code="US",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = await response.parse()
        assert_matches_type(PurchaseCreateResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGmt) -> None:
        async with async_client.purchases.with_streaming_response.create(
            country_code="US",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = await response.parse()
            assert_matches_type(PurchaseCreateResponse, purchase, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGmt) -> None:
        purchase = await async_client.purchases.retrieve(
            12345,
        )
        assert_matches_type(PurchaseRetrieveResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGmt) -> None:
        response = await async_client.purchases.with_raw_response.retrieve(
            12345,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = await response.parse()
        assert_matches_type(PurchaseRetrieveResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGmt) -> None:
        async with async_client.purchases.with_streaming_response.retrieve(
            12345,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = await response.parse()
            assert_matches_type(PurchaseRetrieveResponse, purchase, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncGmt) -> None:
        purchase = await async_client.purchases.list(
            page=1,
            page_size=50,
        )
        assert_matches_type(AsyncPageNumber[PurchaseListResponse], purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGmt) -> None:
        purchase = await async_client.purchases.list(
            page=1,
            page_size=50,
            status="SUCCESS",
        )
        assert_matches_type(AsyncPageNumber[PurchaseListResponse], purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGmt) -> None:
        response = await async_client.purchases.with_raw_response.list(
            page=1,
            page_size=50,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = await response.parse()
        assert_matches_type(AsyncPageNumber[PurchaseListResponse], purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGmt) -> None:
        async with async_client.purchases.with_streaming_response.list(
            page=1,
            page_size=50,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = await response.parse()
            assert_matches_type(AsyncPageNumber[PurchaseListResponse], purchase, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_request_verification_code(self, async_client: AsyncGmt) -> None:
        purchase = await async_client.purchases.request_verification_code(
            purchase_id=12345,
        )
        assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_request_verification_code_with_all_params(self, async_client: AsyncGmt) -> None:
        purchase = await async_client.purchases.request_verification_code(
            purchase_id=12345,
            callback_url="https://example.com/webhooks/code-received",
        )
        assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_request_verification_code(self, async_client: AsyncGmt) -> None:
        response = await async_client.purchases.with_raw_response.request_verification_code(
            purchase_id=12345,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        purchase = await response.parse()
        assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_request_verification_code(self, async_client: AsyncGmt) -> None:
        async with async_client.purchases.with_streaming_response.request_verification_code(
            purchase_id=12345,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            purchase = await response.parse()
            assert_matches_type(PurchaseRequestVerificationCodeResponse, purchase, path=["response"])

        assert cast(Any, response.is_closed) is True
