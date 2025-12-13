# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gmt import Gmt, AsyncGmt
from gmt.types import ServiceHealthCheckResponse, ServiceGetServerTimeResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestService:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_server_time(self, client: Gmt) -> None:
        service = client.service.get_server_time()
        assert_matches_type(ServiceGetServerTimeResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_server_time(self, client: Gmt) -> None:
        response = client.service.with_raw_response.get_server_time()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service = response.parse()
        assert_matches_type(ServiceGetServerTimeResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_server_time(self, client: Gmt) -> None:
        with client.service.with_streaming_response.get_server_time() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service = response.parse()
            assert_matches_type(ServiceGetServerTimeResponse, service, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_health_check(self, client: Gmt) -> None:
        service = client.service.health_check()
        assert_matches_type(ServiceHealthCheckResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_health_check(self, client: Gmt) -> None:
        response = client.service.with_raw_response.health_check()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service = response.parse()
        assert_matches_type(ServiceHealthCheckResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_health_check(self, client: Gmt) -> None:
        with client.service.with_streaming_response.health_check() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service = response.parse()
            assert_matches_type(ServiceHealthCheckResponse, service, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncService:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_server_time(self, async_client: AsyncGmt) -> None:
        service = await async_client.service.get_server_time()
        assert_matches_type(ServiceGetServerTimeResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_server_time(self, async_client: AsyncGmt) -> None:
        response = await async_client.service.with_raw_response.get_server_time()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service = await response.parse()
        assert_matches_type(ServiceGetServerTimeResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_server_time(self, async_client: AsyncGmt) -> None:
        async with async_client.service.with_streaming_response.get_server_time() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service = await response.parse()
            assert_matches_type(ServiceGetServerTimeResponse, service, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_health_check(self, async_client: AsyncGmt) -> None:
        service = await async_client.service.health_check()
        assert_matches_type(ServiceHealthCheckResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_health_check(self, async_client: AsyncGmt) -> None:
        response = await async_client.service.with_raw_response.health_check()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service = await response.parse()
        assert_matches_type(ServiceHealthCheckResponse, service, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_health_check(self, async_client: AsyncGmt) -> None:
        async with async_client.service.with_streaming_response.health_check() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service = await response.parse()
            assert_matches_type(ServiceHealthCheckResponse, service, path=["response"])

        assert cast(Any, response.is_closed) is True
