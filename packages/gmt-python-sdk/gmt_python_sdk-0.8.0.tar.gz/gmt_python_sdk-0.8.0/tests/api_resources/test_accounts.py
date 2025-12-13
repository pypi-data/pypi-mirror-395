# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gmt import Gmt, AsyncGmt
from gmt.types import (
    AccountListResponse,
    AccountRetrieveResponse,
    AccountListCountriesResponse,
)
from tests.utils import assert_matches_type
from gmt.pagination import SyncPageNumber, AsyncPageNumber

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Gmt) -> None:
        account = client.accounts.retrieve(
            "US",
        )
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Gmt) -> None:
        response = client.accounts.with_raw_response.retrieve(
            "US",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Gmt) -> None:
        with client.accounts.with_streaming_response.retrieve(
            "US",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrieveResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Gmt) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `country_code` but received ''"):
            client.accounts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Gmt) -> None:
        account = client.accounts.list(
            page=1,
            page_size=50,
            sort="price_asc",
        )
        assert_matches_type(SyncPageNumber[AccountListResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Gmt) -> None:
        account = client.accounts.list(
            page=1,
            page_size=50,
            sort="price_asc",
            country_codes="US,RU,GB",
        )
        assert_matches_type(SyncPageNumber[AccountListResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Gmt) -> None:
        response = client.accounts.with_raw_response.list(
            page=1,
            page_size=50,
            sort="price_asc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(SyncPageNumber[AccountListResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Gmt) -> None:
        with client.accounts.with_streaming_response.list(
            page=1,
            page_size=50,
            sort="price_asc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(SyncPageNumber[AccountListResponse], account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_countries(self, client: Gmt) -> None:
        account = client.accounts.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
        )
        assert_matches_type(SyncPageNumber[AccountListCountriesResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_countries_with_all_params(self, client: Gmt) -> None:
        account = client.accounts.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
            country_codes="US,RU,GB",
        )
        assert_matches_type(SyncPageNumber[AccountListCountriesResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_countries(self, client: Gmt) -> None:
        response = client.accounts.with_raw_response.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(SyncPageNumber[AccountListCountriesResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_countries(self, client: Gmt) -> None:
        with client.accounts.with_streaming_response.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(SyncPageNumber[AccountListCountriesResponse], account, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAccounts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGmt) -> None:
        account = await async_client.accounts.retrieve(
            "US",
        )
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGmt) -> None:
        response = await async_client.accounts.with_raw_response.retrieve(
            "US",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGmt) -> None:
        async with async_client.accounts.with_streaming_response.retrieve(
            "US",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrieveResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncGmt) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `country_code` but received ''"):
            await async_client.accounts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncGmt) -> None:
        account = await async_client.accounts.list(
            page=1,
            page_size=50,
            sort="price_asc",
        )
        assert_matches_type(AsyncPageNumber[AccountListResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGmt) -> None:
        account = await async_client.accounts.list(
            page=1,
            page_size=50,
            sort="price_asc",
            country_codes="US,RU,GB",
        )
        assert_matches_type(AsyncPageNumber[AccountListResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGmt) -> None:
        response = await async_client.accounts.with_raw_response.list(
            page=1,
            page_size=50,
            sort="price_asc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AsyncPageNumber[AccountListResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGmt) -> None:
        async with async_client.accounts.with_streaming_response.list(
            page=1,
            page_size=50,
            sort="price_asc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AsyncPageNumber[AccountListResponse], account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_countries(self, async_client: AsyncGmt) -> None:
        account = await async_client.accounts.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
        )
        assert_matches_type(AsyncPageNumber[AccountListCountriesResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_countries_with_all_params(self, async_client: AsyncGmt) -> None:
        account = await async_client.accounts.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
            country_codes="US,RU,GB",
        )
        assert_matches_type(AsyncPageNumber[AccountListCountriesResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_countries(self, async_client: AsyncGmt) -> None:
        response = await async_client.accounts.with_raw_response.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AsyncPageNumber[AccountListCountriesResponse], account, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_countries(self, async_client: AsyncGmt) -> None:
        async with async_client.accounts.with_streaming_response.list_countries(
            page=1,
            page_size=50,
            sort="price_asc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AsyncPageNumber[AccountListCountriesResponse], account, path=["response"])

        assert cast(Any, response.is_closed) is True
